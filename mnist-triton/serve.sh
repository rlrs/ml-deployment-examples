#!/usr/bin/env bash
docker run --gpus 1 --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  --shm-size=1g --ulimit   memlock=-1 --ulimit stack=67108864 \
  -v $PWD/model_repository:/models nvcr.io/nvidia/tritonserver:22.10-py3 tritonserver --model-repository=/models
  