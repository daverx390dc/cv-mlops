import os
import uvicorn
import torch
import numpy as np
from fastapi import FastAPI, File, UploadFile
from torchvision.models import resnet50
from features.featurization import get_transforms

app = FastAPI()
model = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

@app.on_event("startup")
async def load_model():
    global model
    model = resnet50()
    model.fc = torch.nn.Linear(model.fc.in_features, int(os.environ['NUM_CLASSES']))
    model.load_state_dict(torch.load(os.environ['MODEL_PATH'], map_location=device))
    model.eval()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    img = await file.read()
    from PIL import Image
    import io
    image = Image.open(io.BytesIO(img)).convert('RGB')
    tensor = get_transforms(False)(image).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
    return {"predictions": probs.tolist()}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)