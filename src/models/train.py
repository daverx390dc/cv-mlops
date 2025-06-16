import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.models import resnet50
from features.featurization import get_transforms
from utils.logger import setup_logger

logger = setup_logger('train')

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dataset = ImageFolder(os.environ['TRAIN_DATA'], transform=get_transforms(True))
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = resnet50(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(1, 6):
        model.train()
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            preds = model(imgs)
            loss = criterion(preds, labels)
            optimizer.zero_grad(); loss.backward(); optimizer.step()
        logger.info(f"Epoch {epoch} loss: {loss.item()}")

    torch.save(model.state_dict(), os.path.join(os.environ['MODEL_OUTPUT'],'model.pth'))

if __name__ == '__main__':
    train()