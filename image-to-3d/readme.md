# Image-to-3D

**This folder contains two parts:**
- Background removal  
- Image-to-3D  

Note that the environment(packages) of the two parts are incompatible.  
Therefore we need to create an individual virtual environment for each part.

## Step 1. Background removal
Reference: https://github.com/OPHoperHPO/image-background-remove-tool

### Install environment
```bash
pip install carvekit --extra-index-url https://download.pytorch.org/whl/cu113
```

### Implementation
```bash
python preprocess_image.py <image_path>
```
For example: `python preprocess_image.py data/mona_lisa.png`  
This will output a preprocessed image -> `data/mona_lisa_rgba.png`


## Step 2. Image-to-3D
Reference: https://github.com/dreamgaussian/dreamgaussian

### Install environment

```bash
pip install -r requirements.txt

# a modified gaussian splatting (+ depth, alpha rendering)
git clone --recursive https://github.com/ashawkey/diff-gaussian-rasterization
pip install ./diff-gaussian-rasterization

# simple-knn
pip install ./simple-knn

# nvdiffrast
pip install git+https://github.com/NVlabs/nvdiffrast/

# kiuikit
pip install git+https://github.com/ashawkey/kiuikit

# To use MVdream, also install:
pip install git+https://github.com/bytedance/MVDream
```

### Implementation

```bash
bash run_pipeline.sh <path_to_the_preprocessed_image>
```
For example: `bash run_pipeline.sh data/mona_lisa_rgba.png`.  
This will start DreamGaussian training step, and output 3d objects with textures and videos in the `log` folder.


## Citation

```
@article{tang2023dreamgaussian,
  title={DreamGaussian: Generative Gaussian Splatting for Efficient 3D Content Creation},
  author={Tang, Jiaxiang and Ren, Jiawei and Zhou, Hang and Liu, Ziwei and Zeng, Gang},
  journal={arXiv preprint arXiv:2309.16653},
  year={2023}
}
```
