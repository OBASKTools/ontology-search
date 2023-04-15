#!/usr/bin/env bash

set -e
docker build -t ghcr.io/obasktools/ontology-search:latest -f Dockerfile .
docker run -d -p 8007:8007 --network obask_default --name obask-search -it ghcr.io/obasktools/ontology-search:latest
