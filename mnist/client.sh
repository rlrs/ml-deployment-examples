#!/usr/bin/env bash
docker run --rm -it --entrypoint bash \
  --shm-size=1g --ulimit   memlock=-1 --ulimit stack=67108864 \
  -v $PWD:/project \
  --net host \
  nvcr.io/nvidia/tritonserver:22.10-py3-sdk
  