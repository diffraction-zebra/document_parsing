import os
import os
import pathlib
import tempfile
import warnings
from typing import Union, List, Dict

from pydantic import BaseModel

from converters.archive_extractors.extractor import extract_files_from_archive
from converters.specified_converters.doc_converter import extract_text_tables_from_doc
from converters.specified_converters.docx_converter import extract_text_tables_from_docx
from converters.specified_converters.excel_converter import extract_tables_from_excel
from converters.specified_converters.pdf_converter import extract_text_tables_from_pdf
from converters.specified_converters.image_converter import extract_tables_from_image


class DocumentIntro(BaseModel):
    text: str | None = None
    tables: List[str] = []


def add_prefix(dir_name: str, tables: Dict[str, DocumentIntro]):
    return {dir_name + '/' + file_name: tables for file_name, tables in tables.items()}


def remove_prefix(tables: Dict[str, DocumentIntro]):
    return {'/'.join(path.split('/')[1:]): doc_tables
            for path, doc_tables in tables.items()}


async def convert_document_to_text_tables(document_path: Union[str, pathlib.Path], level: int = 0) \
        -> Dict[str, DocumentIntro]:
    if level >= 5:
        return {document_path.name: DocumentIntro()}

    extension = get_extension(document_path)

    if extension in ['zip', 'rar', '7z']:
        with tempfile.TemporaryDirectory() as out_dir:
            out_dir = pathlib.Path(out_dir)
            await extract_files_from_archive(document_path, out_dir)
            intro = await extract_text_tables_from_directory(out_dir, level=level+1)
            # remove 'tmp_dir' prefix
            intro = remove_prefix(intro)
            return add_prefix(document_path.name, intro)

    if extension in ['jpeg', 'jpg', 'png']:
        tables = await extract_tables_from_image(document_path)
        return {document_path.name: DocumentIntro(tables=tables)}

    if extension in ['xls', 'xlsx', 'xlsb']:
        tables = await extract_tables_from_excel(document_path)
        return {document_path.name: DocumentIntro(tables=tables)}

    extractor = None
    if extension in ['docx']:
        extractor = extract_text_tables_from_docx
    elif extension in ['pdf']:
        extractor = extract_text_tables_from_pdf
    elif extension in ['doc']:
        extractor = extract_text_tables_from_doc

    if extractor is None:
        # unsupported document extension
        return {}

    text, tables = await extractor(document_path)
    return {document_path.name: DocumentIntro(text=text, tables=tables)}


async def extract_text_tables_from_directory(dir_path: pathlib.Path, level: int) -> Dict[str, DocumentIntro]:
    if level >= 5:
        return {}
    all_docs = {}
    for file in dir_path.iterdir():
        if file.is_dir():
            all_docs.update(await extract_text_tables_from_directory(file, level+1))
        else:
            try:
                all_docs.update(await convert_document_to_text_tables(file, level+1))
            except Exception as e:
                warnings.warn(f"extraction tables from document {file.name} failed with error {e}")
    return add_prefix(dir_path.name, all_docs)


def get_extension(file: Union[str, pathlib.Path]) -> str:
    return os.path.splitext(str(file))[-1][1:].lower()
