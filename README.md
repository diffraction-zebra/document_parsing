# Document Parsing Project

## Overview

The Document Parsing Project is designed to streamline the process of extracting structured information from a variety of document types. This project provides tools and methods to process, analyze, and extract data from documents in an automated fashion.

Supports parsing from multiple document formats including pdf, docx/doc, xls/xlsx, png/jpg/jpeg.
Recursive work with zip/rar/7z archives.
OCR for images support (with available gpu only)

## Installation
### Clone the repository:
    git clone https://github.com/diffraction-zebra/document_parsing.git
    

## Running with Docker Compose

### Build and start the services:
    docker-compose up --build

## Usage
```python
import pathlib

file_path = pathlib.Path('my_file.supported_extension')

url = 'http://localhost/converter'
response = requests.post(url,
                         data={
                           'filename': file_path.name,
                           "type": "multipart/form-data"
                         },
                         files={
                           file_path.name: open(file_path, 'rb')
                         },
                         timeout=300)  # 5 minutes for large pdf and images
return response.json()
```
## Configuration

- The `docker-compose.yaml` contains 'MODE' part.
Use 'ALL' for text and tables extraction, 'TABLES' for tables only

## Contributing

We welcome contributions to the Document Parsing Project. If you have any ideas, suggestions, or issues, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any inquiries or support, please contact the project maintainer at [diffraction.zebra@gmail.com](diffraction.zebra@gmail.com).
