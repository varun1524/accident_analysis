#!/usr/bin/env bash

docker rm dev-accident_analysis --force || true
docker rmi accident_analysis:1.0.0 --force || true

docker build -t accident_analysis:1.0.0 .
docker run -d --name dev-accident_analysis -p 5000:5000 accident_analysis:1.0.0
