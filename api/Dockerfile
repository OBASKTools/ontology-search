FROM python:3.9.10-slim

LABEL info.authors="Ugur Bayindir ugur@ebi.ac.uk" \
  info.service="obask-ontology-search" \
  info.version="1.0.0"

WORKDIR /app

RUN apt-get update && \
  apt-get install -y bash curl gnupg && \
  ## extra dependencies for scipy
  apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran bash lsb-release jq && \ 
  apt-get clean -y && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

RUN apt-get update

COPY requirements.txt requirements.txt

RUN python3 -m venv /venv/

RUN /venv/bin/python3 -m pip install --upgrade pip && \
  /venv/bin/python3 -m pip install -r ./requirements.txt && \
  /venv/bin/python3 --version && \
  /venv/bin/pip3 --version && /venv/bin/pip3 cache purge

COPY src src
COPY service.sh service.sh

CMD ./service.sh
