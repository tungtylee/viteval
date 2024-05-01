#!/bin/bash

# 獲取主板信息
echo "Motherboard Info:"
sudo dmidecode -t baseboard | grep -E 'Manufacturer|Product Name|Version|Serial Number'
echo ""

# 獲取CPU信息
echo "CPU Info:"
cat /proc/cpuinfo | grep -E 'model name|vendor_id|cpu MHz|cache size|cpu cores|processor'
echo ""

# 獲取GPU信息
echo "GPU Info:"
lspci | grep -i vga
echo ""

# 內存信息
echo "Memory Info:"
# 使用free命令獲得內存使用情況，顯示的單位為MB
free -m
echo ""

# 如果安裝了NVIDIA驅動，可以使用nvidia-smi獲取更詳細的GPU信息
if command -v nvidia-smi &> /dev/null
then
    nvidia-smi
    echo ""
fi

echo "All information has been displayed above."
