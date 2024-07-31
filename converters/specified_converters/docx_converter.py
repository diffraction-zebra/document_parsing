import os
from typing import Union, List, Tuple

import docx
import pathlib
import pandas as pd

from converters.specified_converters.dataframe_handlers import clear_dataframe, dataframe_to_string


async def extract_text_tables_from_docx(document_path: Union[str, pathlib.Path]) \
        -> Tuple[str | None, List[str]]:
    document_path = str(pathlib.Path(document_path))
    doc = docx.Document(document_path)
    # extract text
    if os.getenv('MODE') == 'ALL':
        text_result = []
        for i, element in enumerate(doc.element.body):
            if isinstance(element, docx.oxml.text.paragraph.CT_P):
                # save text
                paragraph = docx.text.paragraph.Paragraph(element, doc)
                text_result.append(paragraph.text)

        text = '\n'.join(text_result)
    else:
        text = None

    # extract tables
    tables = doc.tables
    dataframes = [doc_table_to_dataframe(table) for table in tables]
    clean_dataframes = [clear_dataframe(table) for table in dataframes]
    string_tables = [dataframe_to_string(table) for table in clean_dataframes]

    return text, string_tables


def doc_table_to_dataframe(table: docx.table.Table) -> pd.DataFrame:
    return pd.DataFrame([[cell.text for cell in row.cells] for row in table.rows])
