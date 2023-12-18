import os
import sys
import cv2
import argparse
import numpy as np

import torch
from PIL import Image


class BackgroundRemoval:
    def __init__(self, device="cuda"):
        from carvekit.api.high import HiInterface

        self.interface = HiInterface(
            object_type="object",  # Can be "object" or "hairs-like".
            batch_size_seg=5,
            batch_size_matting=1,
            device=device,
            seg_mask_size=640,  # Use 640 for Tracer B7 and 320 for U2Net
            matting_mask_size=2048,
            trimap_prob_threshold=231,
            trimap_dilation=30,
            trimap_erosion_iters=5,
            fp16=True,
        )

    @torch.no_grad()
    def __call__(self, image):
        # image: [H, W, 3] array in [0, 255].
        image = Image.fromarray(image)

        image = self.interface([image])[0]
        image = np.array(image)

        return image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="path to image (png, jpeg, etc.)")
    parser.add_argument("--size", default=256, type=int, help="output resolution")
    parser.add_argument(
        "--border_ratio", default=0.2, type=float, help="output border ratio"
    )
    parser.add_argument(
        "--recenter",
        type=bool,
        default=True,
        help="recenter, potentially not helpful for multiview zero123",
    )
    parser.add_argument("--dont_recenter", dest="recenter", action="store_false")
    opt = parser.parse_args()

    out_dir = os.path.dirname(opt.path)
    out_rgba = os.path.join(
        out_dir, os.path.basename(opt.path).split(".")[0] + "_rgba.png"
    )
    out_depth = os.path.join(
        out_dir, os.path.basename(opt.path).split(".")[0] + "_depth.png"
    )
    out_normal = os.path.join(
        out_dir, os.path.basename(opt.path).split(".")[0] + "_normal.png"
    )
    out_caption = os.path.join(
        out_dir, os.path.basename(opt.path).split(".")[0] + "_caption.txt"
    )

    # load image
    print(f"[INFO] loading image...")
    image = cv2.imread(opt.path, cv2.IMREAD_UNCHANGED)
    if image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # carve background
    print(f"[INFO] background removal...")
    carved_image = BackgroundRemoval()(image)  # [H, W, 4]
    mask = carved_image[..., -1] > 0

    # recenter
    if opt.recenter:
        print(f"[INFO] recenter...")
        final_rgba = np.zeros((opt.size, opt.size, 4), dtype=np.uint8)
        final_depth = np.zeros((opt.size, opt.size), dtype=np.uint8)
        final_normal = np.zeros((opt.size, opt.size, 3), dtype=np.uint8)

        coords = np.nonzero(mask)
        x_min, x_max = coords[0].min(), coords[0].max()
        y_min, y_max = coords[1].min(), coords[1].max()
        h = x_max - x_min
        w = y_max - y_min
        desired_size = int(opt.size * (1 - opt.border_ratio))
        scale = desired_size / max(h, w)
        h2 = int(h * scale)
        w2 = int(w * scale)
        x2_min = (opt.size - h2) // 2
        x2_max = x2_min + h2
        y2_min = (opt.size - w2) // 2
        y2_max = y2_min + w2
        final_rgba[x2_min:x2_max, y2_min:y2_max] = cv2.resize(
            carved_image[x_min:x_max, y_min:y_max],
            (w2, h2),
            interpolation=cv2.INTER_AREA,
        )
    else:
        final_rgba = carved_image


    # write output
    cv2.imwrite(out_rgba, cv2.cvtColor(final_rgba, cv2.COLOR_RGBA2BGRA))

