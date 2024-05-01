from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import numpy as np
import os
import requests
import sys

imgfn = "000000039769.jpg"
if os.path.exists(imgfn) is False:
    url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
    image = Image.open(requests.get(url, stream=True).raw)
    image.save(imgfn)
else:
    image = Image.open(imgfn)

# I have used large model, & suggest the large or gaint model.
import torch
print(torch.hub.list('facebookresearch/dinov2'))

import requests
from PIL import Image
from torchvision import transforms
transform = transforms.Compose([
                                transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize(
                                mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225]
                                )])


transform1 = transforms.Compose([
                                transforms.Resize(520),
                                transforms.CenterCrop(518), #should be multiple of model patch_size
                                transforms.ToTensor(),
                                transforms.Normalize(mean=0.5, std=0.2)
                                ])



device = "cuda" if torch.cuda.is_available() else "cpu"
if len(sys.argv) > 1:
    device = sys.argv[1]

modelver = "dinov2_vits14"
if len(sys.argv) > 2:
    modelver = sys.argv[2]

if modelver == "dinov2_vits14":
    totest = (384, torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14'))
elif modelver == "dinov2_vitb14":
    totest = (768, torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14'))
elif modelver == "dinov2_vitl14":
    totest = (1024, torch.hub.load('facebookresearch/dinov2', 'dinov2_vitl14'))
elif modelver == "dinov2_vitg14":
    totest = (1536, torch.hub.load('facebookresearch/dinov2', 'dinov2_vitg14'))

embd = []

feat_dim, dinov2_vit = totest
dinov2_vit = dinov2_vit.to(device)
patch_size = dinov2_vit.patch_size

def run_imgfeatures():
    total_features  = []
    with torch.no_grad():
        for i in range(1):
            img_t = transform1(image).to(device)

            features_dict = dinov2_vit.forward_features(img_t.unsqueeze(0))
            features = features_dict['x_norm_patchtokens']
            total_features.append(features)

        total_features = torch.cat(total_features, dim=0)
        total_features.shape
        return total_features

import time
for i in range(11):
    t1 = time.perf_counter()
    total_features = run_imgfeatures()
    t2 = time.perf_counter()
    embd.append(t2-t1)

print(device, modelver)
print("elasped_time", "avg10", "first")
print("dinov2", np.mean(embd[1:]), embd[0])

import psutil
import os

# 獲取當前進程
process = psutil.Process(os.getpid())
# 使用單位為MB的內存使用量
memory_use = process.memory_info().rss / 1024 / 1024
print(f"Memory used: {memory_use} MB")

import subprocess

# 執行nvidia-smi命令
result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE)
print(result.stdout.decode('utf-8'))
