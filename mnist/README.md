# Training an MNIST model and serving with Triton using ONNX

## Train the model
In the devcontainer, run
`python3 train.py --save-model --epochs 2`
which generates the ONNX file `model_repository/mnist/1/model.onnx`.

## Serve the model
On the host, run `./serve.sh` to start the Triton container which serves models from `model_repository/`.

## Try the model
On the host, run `./client.sh` to start an interactive Triton SDK container. Download an example image from somewhere and query the model like `./install/bin/image_client -m mnist <path_to_image>`.