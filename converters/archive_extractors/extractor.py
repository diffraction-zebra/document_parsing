import os
import pathlib

import pyunpack


def fix_path_coding(path: pathlib.Path) -> pathlib.Path:
    try:
        new_path_name = path.name.encode('IBM437').decode('IBM866')
        new_path = path.parent / new_path_name
        os.rename(path, new_path)
        return new_path
    except (UnicodeDecodeError, UnicodeEncodeError):
        return path


def fix_dir_coding(path: pathlib.Path) -> pathlib.Path:
    fixed_path = fix_path_coding(path)
    if fixed_path.is_dir():
        for subpath in fixed_path.iterdir():
            fix_dir_coding(subpath)
    return fixed_path


async def extract_files_from_archive(archive: str | pathlib.Path, extract_path: str | pathlib.Path) -> None:
    pyunpack.Archive(str(archive)).extractall(str(extract_path))
    fix_dir_coding(extract_path)

    # limit filename with 256 symbols
    for file in extract_path.iterdir():
        new_name = file.stem[:256] + file.suffix
        file.rename(extract_path / new_name)
