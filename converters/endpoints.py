import os
import pathlib
import tempfile
import warnings

import fastapi
from fastapi import FastAPI, UploadFile

from converters.manager import convert_document_to_text_tables

app = FastAPI(default_response_class=fastapi.responses.ORJSONResponse)


@app.post("/converter/")
async def convert_documents(file: UploadFile):
    # temporary directory for safety
    with tempfile.TemporaryDirectory() as temp_dir:
        # put file in directory
        temp_dir = pathlib.Path(temp_dir)
        # limit filename to 256 symbols, save extension
        filename = pathlib.Path(file.filename).stem[:256] + pathlib.Path(file.filename).suffix
        document_path = temp_dir / filename
        with open(document_path, "wb") as buffer:
            buffer.write(await file.read())

        # convert
        try:
            text_tables = await convert_document_to_text_tables(document_path)
        except Exception as e:
            warnings.warn(f"extraction tables from document {file.filename} failed with error {e}")
            text_tables = {}

        if os.getenv('MODE') == 'TABLES':
            text_tables = {filename: document_intro.tables
                           for filename, document_intro in text_tables.items()}

        return {file.filename: text_tables}
