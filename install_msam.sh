#!/bin/bash

# 檢查環境是否已存在
source $HOME/anaconda3/etc/profile.d/conda.sh
tar_env=viteval
env_exists=$(conda env list | grep $tar_env)

if [[ -z $env_exists ]]; then
    echo "Environment $tar_env does not exist. Creating now..."
    conda create -n $tar_env python=3.11 -y
    conda activate $tar_env

    # special for N97
    pip install opencv-python-headless
    sudo apt-get update
    sudo apt-get install libgl1 -y

    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip install transformers
    pip install Pillow
    pip install opencv-python
    pip install timm
    pip install matplotlib
    # Check MobileSAM
    if [ ! -d "MobileSAM" ]; then
        echo "MobileSAM directory does not exist. Cloning now..."
        # 如果不存在，則克隆git倉庫
        git clone https://github.com/ChaoningZhang/MobileSAM
    else
        echo "MobileSAM directory already exists. No action taken."
    fi
    cd MobileSAM; pip install -e .
    cd ..

    # pip install xformers
    pip install psutil
else
    echo "Environment $tar_env already exists. No action taken."
    conda activate $tar_env
fi

echo "Check cuda in torch"
python -c "import torch; print(torch.cuda.is_available())" 



