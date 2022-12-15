from fastapi import FastAPI
from fastapi.responses import FileResponse
import tritonclient.grpc as grpcclient
from tritonclient.utils import InferenceServerException
from PIL import Image
from numpy import asarray
from torchvision import transforms
import io
from starlette.responses import PlainTextResponse, JSONResponse
import numpy as np

app = FastAPI()
triton_client = grpcclient.InferenceServerClient(url='localhost:8001', verbose=True)

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.route("/query", methods=['POST'])
async def query(request):
  if request.method == 'POST':
    form = await request.form()
    filename = form["file"].filename
    contents = await form["file"].read()
    img = Image.open(io.BytesIO(contents)).convert('L')
    img = img.resize((28, 28))
    img = asarray(img) #.transpose(2, 0, 1)
    print(img.shape)

    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    img = asarray(transform(img))

    inputs = []
    inputs.append(grpcclient.InferInput('modelInput', [1, 28, 28], "FP32"))
    inputs[0].set_data_from_numpy(img)

    outputs = []
    outputs.append(grpcclient.InferRequestedOutput('modelOutput'))

    results = triton_client.infer('mnist', inputs, outputs=outputs)
    res = results.as_numpy('modelOutput')
    if res is not None:
      probs = np.exp(res) / np.sum(np.exp(res))
      js = {i: float(p) for i, p in enumerate(probs[0].tolist())}
      return JSONResponse(js, status_code=200)
    else:
      return JSONResponse("No result", status_code=500)