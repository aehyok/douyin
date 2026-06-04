#!/usr/bin/env python3
"""连通域色键抠图：去掉与图像边缘连通的纯色背景，保护主体内部孔洞
   (例如封面笔记本浅色屏幕不会被误删)。用法: chroma_cut.py in.png out.png [thr]"""
import sys
import numpy as np
from PIL import Image, ImageFilter

inp, outp = sys.argv[1], sys.argv[2]
thr = float(sys.argv[3]) if len(sys.argv) > 3 else 52.0

im = Image.open(inp).convert("RGBA")
arr = np.asarray(im).copy()
rgb = arr[..., :3].astype(np.float32)

# 背景色 = 四角 24x24 块平均
c = np.concatenate([
    rgb[:24, :24].reshape(-1, 3), rgb[:24, -24:].reshape(-1, 3),
    rgb[-24:, :24].reshape(-1, 3), rgb[-24:, -24:].reshape(-1, 3)])
bg = c.mean(0)
dist = np.sqrt(((rgb - bg) ** 2).sum(-1))
bgmask = dist < thr

# 只删与边缘连通的背景；主体内部接近背景色的孔洞保留
try:
    from scipy import ndimage
    lbl, n = ndimage.label(bgmask)
    edge = np.unique(np.concatenate([lbl[0], lbl[-1], lbl[:, 0], lbl[:, -1]]))
    edge = edge[edge != 0]
    connected = np.isin(lbl, edge)
    mode = f"connected-component (scipy, {n} labels)"
except Exception as e:
    connected = bgmask
    mode = f"flat-threshold (no scipy: {e})"

alpha = np.where(connected, 0, 255).astype(np.uint8)
# 边缘羽化 1.2px
alpha_img = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.2))
arr[..., 3] = np.asarray(alpha_img)
Image.fromarray(arr).save(outp)
print(f"OK {outp} | bg={bg.astype(int).tolist()} thr={thr} | {mode}")
