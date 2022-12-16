# Training an MNIST model and serving with Triton using ONNX, then using the Triton API to expose a simple website interafce

## Train the model
In the devcontainer, train the model for a couple of epochs, e.g. `python3 train.py --epochs 2` which generates the ONNX file `model_repository/mnist/1/model.onnx`.

## Serve the model
On the host, run `./serve.sh` to start the Triton container which serves models from `model_repository/`. Triton exposes an HTTP and gRPC API, which are not very straightforward to use.
Instead, we serve an interface using FastAPI through Hypercorn, `hypercorn --bind 0.0.0.0:8080 serve:app`. For development, you can add `--reload` to live-reload code changes to the server.

## Try the model
To use the Triton API directly, `./client.sh` starts an interactive Triton SDK container. In this container, you can query the model like `./install/bin/image_client -m mnist <path_to_image>`.

Alternatively, the website is served on port `8080`, which serves a static HTML file `static/index.html`. This page uses a bit of Javascript to communicate with the exposed FastAPI to run queries and retrieve responses.

## Serving with HTTP/2 and TLS
Hypercorn will use HTTP/2 and TLS if you give it a private key and certificate
`hypercorn --keyfile tls/key.pem --certfile tls/cert.pem serve:app`.

You can generate a self-signed RSA key and certificate valid for 365 days with the command
`openssl req -x509 -newkey rsa:4096 -keyout tls/key.pem -out tls/cert.pem -days 365 -nodes`.
For production, obtain a certificate from Let's Encrypt.