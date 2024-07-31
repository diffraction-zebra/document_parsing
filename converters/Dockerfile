FROM ubuntu:22.04
RUN apt -y update && apt -y upgrade && apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa && apt install -y python3.10 && apt install -y python3-pip

RUN apt install -y antiword libreoffice ghostscript
RUN apt install -y unrar
RUN apt install -y p7zip-full

RUN mkdir converters

COPY requirements.txt converters/requirements.txt
RUN pip3 install -r converters/requirements.txt

COPY . converters/.

ENTRYPOINT uvicorn converters.endpoints:app --host 0.0.0.0 --port 5000