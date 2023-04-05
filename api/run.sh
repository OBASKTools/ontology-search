#!/usr/bin/env bash

set -e
docker build -t obasktools/ontologysearch -f docker/Dockerfile .
docker run -d -p 8081:8081 --network obask_default --name cap-search -it obasktools/ontologysearch
