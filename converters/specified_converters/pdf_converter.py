import os
from typing import Union, List, Dict, Tuple

import pypdf
import camelot
import pathlib
import PyPDF2

from converters.specified_converters.dataframe_handlers import clear_dataframe, dataframe_to_string


async def extract_tables_from_page(document_path: Union[str, pathlib.Path], page: int,
                                   camelot_args: Dict | None = None) \
        -> List[str]:
    if camelot_args is None:
        camelot_args = dict()
    tables = camelot.read_pdf(str(document_path), pages=str(page), **camelot_args)
    tables = [table.df for table in tables]
    tables = [clear_dataframe(table) for table in tables]
    tables = [dataframe_to_string(table) for table in tables]
    return tables


async def extract_text_tables_from_pdf(document_path: Union[str, pathlib.Path], camelot_args: Dict | None = None) \
        -> Tuple[str | None, List[str]]:

    if camelot_args is None:
        camelot_args = dict()

    # extract text
    if os.getenv('MODE') == 'ALL':
        text = ''
        with open(document_path, 'rb') as f:
            pdf = pypdf.PdfReader(f)
            for i, page in enumerate(pdf.pages):
                text += page.extract_text()
    else:
        text = None

    with open(document_path, 'rb') as f:
        pages_num = PyPDF2.PdfFileReader(f).getNumPages()
    max_pages = os.getenv('PDF_MAX_PAGES')
    if max_pages is None:
        max_pages = 15

    tables = []
    for page in range(min(pages_num, max_pages)):
        out = await extract_tables_from_page(document_path, page + 1, camelot_args)
        tables.extend(out)
    return text, tables
