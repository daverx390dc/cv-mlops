import os
import torch
from models.train import train

def test_train_runs(tmp_path, monkeypatch):
    # setup fake env
    monkeypatch.setenv('TRAIN_DATA', str(tmp_path))
    monkeypatch.setenv('MODEL_OUTPUT', str(tmp_path))
    # create dummy data
    (tmp_path / '0').mkdir();
    dummy = torch.zeros((3,224,224), dtype=torch.uint8).numpy()
    import cv2
    cv2.imwrite(str(tmp_path/'0'/'img.jpg'), dummy)
    # run train should not error
    train()
    assert os.path.exists(str(tmp_path/'model.pth'))