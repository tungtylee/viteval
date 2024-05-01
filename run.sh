#!/bin/bash

bash install_anaconda.sh | tee install_a.txt
bash install_msam.sh | tee install_m.txt

bash get_info.sh | tee info.txt

source $HOME/anaconda3/etc/profile.d/conda.sh
tar_env=viteval
conda activate $tar_env
echo "Check cuda in torch"
python -c "import torch; print(torch.cuda.is_available())" 

python test_msam.py cpu | tee msam_cpu.txt
python test_msam.py cuda | tee msam_cuda.txt
python test_dinov2.py cpu  dinov2_vits14 | tee dinov2_vits14_cpu.txt
python test_dinov2.py cuda dinov2_vits14 | tee dinov2_vits14_cuda.txt
python test_dinov2.py cpu  dinov2_vitb14 | tee dinov2_vitb14_cpu.txt
python test_dinov2.py cuda dinov2_vitb14 | tee dinov2_vitb14_cuda.txt
python test_dinov2.py cpu  dinov2_vitl14 | tee dinov2_vitl14_cpu.txt
python test_dinov2.py cuda dinov2_vitl14 | tee dinov2_vitl14_cuda.txt
python test_dinov2.py cpu  dinov2_vitg14 | tee dinov2_vitg14_cpu.txt
python test_dinov2.py cuda dinov2_vitg14 | tee dinov2_vitg14_cuda.txt
