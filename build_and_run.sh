#!/usr/bin/env bash

docker rm dev-accident_analysis --force || true
docker rmi accident_analysis:1.0.1 --force || true

docker build -t accident_analysis:1.0.1 .
docker run -itd --name dev-accident_analysis -p 80:5000 accident_analysis:1.0.1
