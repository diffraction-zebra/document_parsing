import pathlib
from typing import List

import requests


async def extract_tables_from_image(image_path: pathlib.Path) -> List[str]:
    url = 'http://ocr:5000/'
    r = requests.post(url,
                      data={
                          'filename': image_path.name,
                          "type": "multipart/form-data"},
                      files={
                          "file": open(image_path, 'rb')
                      })
    return r.json()['tables']
