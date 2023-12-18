#!/bin/bash

image_path=$1
image_name=$(basename -- "$image_path")
image_name="${image_name%.*}"
image_name="${image_name%_rgba}"

echo "$image_path"
echo "$image_name"

python main1.py --config configs/image.yaml input="$image_path" save_path="${image_name}"
python main2.py --config configs/image.yaml input="$image_path" save_path="${image_name}"
python -m kiui.render "logs/${image_name}.obj" --save_video "logs/${image_name}.mp4" --wogui

