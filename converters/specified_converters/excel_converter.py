from typing import Union, List

import pathlib
import pandas as pd

from converters.specified_converters.dataframe_handlers import clear_dataframe, dataframe_to_string


async def extract_tables_from_excel(document_path: Union[str, pathlib.Path]) -> List[str]:
    excel_file = pd.ExcelFile(document_path)
    dataframes = list()
    for name in excel_file.sheet_names:
        dataframes.append(pd.read_excel(excel_file, name))

    dataframes = [df.dropna(axis=0, how='all').dropna(axis=1, how='all')
                  for df in dataframes]
    tables = [clear_dataframe(df) for df in dataframes if len(df) > 0]
    tables = [dataframe_to_string(df) for df in dataframes if len(df) > 0]
    return tables
