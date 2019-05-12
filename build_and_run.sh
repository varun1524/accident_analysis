#!/usr/bin/env bash

docker build -t accident_analysis:1.0.0 .

docker rm dev-accident_analysis --force || true

docker run -itd --name dev-accident_analysis -p 5001:5001 accident_analysis:1.0.0
