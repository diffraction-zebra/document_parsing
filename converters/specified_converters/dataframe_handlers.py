import re

import pandas as pd


def dataframe_to_string(table: pd.DataFrame) -> str:
    str_repr = table.to_string(header=False, na_rep='')

    # replace all whitespaces with one space
    str_repr = re.sub(r'[ \t\r\f\v]+', ' ', str_repr)
    str_repr = re.sub(r'\n+', '\n', str_repr)
    return str_repr


def clear_dataframe(table: pd.DataFrame) -> pd.DataFrame:
    # if rows have a similar long text in the different cells, remove similar, keep only one
    for i, row in table.iterrows():
        for idx, (j, cell) in enumerate(row.items()):
            if cell in row.iloc[:idx].values:
                table.at[i, j] = ''
    return table
