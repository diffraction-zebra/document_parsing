FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04
RUN apt -y update && apt -y upgrade && apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa && apt install -y python3.10 && apt install -y python3-pip

RUN apt install -y ffmpeg libsm6 libxext6

RUN mkdir ocr

COPY requirements.txt ocr/requirements.txt
RUN pip3 install -r ocr/requirements.txt

COPY . ocr/

ENTRYPOINT uvicorn ocr.endpoints:app --host 0.0.0.0 --port 5000