import os
import warnings
import platform
from typing import Union, List, Tuple

import pathlib
import pandas as pd
import xml.etree.ElementTree as ET

from converters.specified_converters.docx_converter import extract_text_tables_from_docx
from converters.specified_converters.dataframe_handlers import clear_dataframe, dataframe_to_string


def change_path_extension(document_path: pathlib.Path, old_extension: str, new_extension: str) -> pathlib.Path:
    no_extension = str(document_path)[:-len(old_extension)]
    docx_extension = no_extension + new_extension
    return pathlib.Path(docx_extension)


async def extract_text_tables_from_doc(document_path: Union[str, pathlib.Path], fast=True) \
        -> Tuple[str | None, List[str]]:
    """
    :param fast: if true:
                    use antiword doc2xml converter, no images handling, some tables may be missed or restructured
                 else:
                    use libreoffice doc2docx converter, then perfectly handle docx file
    """
    doc_path = pathlib.Path(document_path)
    if fast:
        xml_path = change_path_extension(doc_path, 'doc', 'xml')
        # create xml file
        res = os.system(f"antiword -x db '{str(doc_path)}'  > '{str(xml_path)}'")
        if res != 0:
            raise OSError(res, 'error while calling antiword', str(doc_path))

        tree = ET.parse(xml_path)
        root = tree.getroot()

        if os.getenv('MODE') == 'ALL':
            text = ET.tostring(root, encoding='utf8', method='text').decode('utf8')
        else:
            text = None

        tables = []
        for table in root.findall('.//informaltable'):
            table_data = []

            for row in table.findall('.//row'):
                row_data = []
                for cell in row.findall('.//entry'):
                    part = ''.join(cell.itertext()).strip()
                    row_data.append(part)
                if row_data:
                    table_data.append(row_data)
            if table_data:
                tables.append(table_data)
        tables = [pd.DataFrame(table) for table in tables]
        tables = [clear_dataframe(table) for table in tables]
        tables = [dataframe_to_string(table) for table in tables]
        xml_path.unlink()
        return text, tables
    else:
        docx_path = change_path_extension(doc_path, 'doc', 'docx')

        # for local tests
        command = None
        system = platform.system()
        if system == 'Linux':
            command = 'libreoffice'
        elif system == 'Darwin':
            command = 'soffice'

        if command is None:
            warnings.warn('unsupported platform for fast=False extraction from doc, change for fast=True')
            return await extract_text_tables_from_doc(document_path, True)

        res = os.system(f"{command} --headless --convert-to docx '{str(doc_path)}' --outdir '{str(docx_path.parent)}'")
        if res != 0:
            raise OSError(res, 'error while calling libreoffice', str(doc_path))

        out = extract_text_tables_from_docx(docx_path)
        docx_path.unlink()
        return await out
