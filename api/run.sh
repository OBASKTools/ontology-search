#!/usr/bin/env bash

# Deprecation warning! Install Bazel and use "./sandbox/bazel.sh run //api:service" command instaed!

set -e
docker build -t cap/search-service -f docker/Dockerfile .
docker run -d -p 8081:8081 --network cap-pipeline-config_default --name cap-search -it cap/search-service
