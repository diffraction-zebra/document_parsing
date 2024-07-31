import tempfile
import pathlib
import warnings

from fastapi import FastAPI, UploadFile

from ocr.extractor import extract_tables_from_image, load_models

app = FastAPI()


@app.on_event("startup")
def prepare_environment():
    load_models()


@app.post("/")
async def convert_documents(file: UploadFile):
    # temporary directory for safety
    with tempfile.TemporaryDirectory() as temp_dir:
        # put file in directory
        temp_dir = pathlib.Path(temp_dir)
        document_path = temp_dir / file.filename
        with open(document_path, "wb") as buffer:
            buffer.write(await file.read())

        # convert
        try:
            tables = extract_tables_from_image(document_path)
        except Exception as e:
            warnings.warn(f"extraction tables from image {file.filename} failed with error {e}")
            tables = []
        return {"tables": tables}
