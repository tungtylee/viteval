import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from mobile_sam import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import sys
import time

model_type = "vit_t"
sam_checkpoint = "MobileSAM/weights/mobile_sam.pt"

device = "cuda" if torch.cuda.is_available() else "cpu"
if len(sys.argv) > 1:
    device = sys.argv[1]

mobile_sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
mobile_sam.to(device=device)
mobile_sam.eval()

std1024 = "std1024.jpg"
image = cv2.imread(std1024)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# input_prompts = "toy cat"
input_point = np.zeros((3,2))
input_point[0, 0] = 1000
input_point[0, 1] = 880
input_point[1, 0] = 996
input_point[1, 1] = 996
input_point[2, 0] = 120
input_point[2, 1] = 700
input_label  = np.array([1, 1, 0])

predictor = SamPredictor(mobile_sam)


embd = [0] * 51
pred = [0] * 51

# Segment with Prompts
for i in range(51):
    s = time.time()
    c = np.random.rand(*image.shape).astype(image.dtype)
    predictor.set_image(c)
    e = time.time()
    embd[i] = e-s

    s = time.time()
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    e = time.time()
    pred[i] = e-s

print("elasped_time", "avg", "first")
print("embd", np.mean(embd[1:]), embd[0])
print("pred", np.mean(pred[1:]), pred[0])


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
