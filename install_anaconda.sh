#!/bin/bash

# 檢查Anaconda是否已安裝
if [ ! -d "${HOME}/anaconda3" ]; then
    echo "Anaconda3 is not installed. Installing now..."

    # 下載Anaconda安裝腳本
    # wget -c https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh -O ${HOME}/anaconda3.sh
    wget -c https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh -O ${HOME}/anaconda3.sh


    # 自動執行安裝腳本
    bash ${HOME}/anaconda3.sh -b -p ${HOME}/anaconda3

    # 刪除安裝腳本
    rm ${HOME}/anaconda3.sh

    # 更新.bashrc以添加Anaconda到PATH
    echo 'export PATH="${HOME}/anaconda3/bin:$PATH"' >> ${HOME}/.bashrc

    # 重新讀取.bashrc，使設置立即生效
    source ${HOME}/.bashrc

    echo "Anaconda3 installation complete!"
else
    echo "Anaconda3 is already installed."
fi
