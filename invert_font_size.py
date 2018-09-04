# Author: Ankush Gupta
# Date: 2015
"Script to generate font-models."

import pygame
from pygame import freetype
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os.path as osp

pygame.init()
DATA_DIR = 'data'
font_pt_sizes = np.arange(8, 200)
# [[8,1],[9,1],[10,1]...]
A = np.c_[font_pt_sizes, np.ones_like(font_pt_sizes)]
models = {}  # linear model
# get the names of fonts to use:
fontlist_txt_path = osp.join(DATA_DIR, 'fonts/fontlist.txt')
fonts_path = [osp.join(DATA_DIR, 'fonts', line.strip()) for line in open(fontlist_txt_path)]
# FS = FontState()
# plt.figure()
# plt.hold(True)
for i in range(len(fonts_path)):
    print(i)
    font = freetype.Font(fonts_path[i], size=12)
    font_px_heights = []
    for font_pt_size in font_pt_sizes:
        font_px_heights.append(font.get_sized_glyph_height(float(font_pt_size)))
    font_px_heights = np.array(font_px_heights)
    # a = np.linalg.lstsq(A,h),有 h = a * A
    # y = mx + c --> y = Ap = [[x 1]] * [[m],[c]]
    # >>> A = np.vstack([x, np.ones(len(x))]).T
    # >>> A
    # array([[ 0.,  1.],
    #        [ 1.,  1.],
    #        [ 2.,  1.],
    #        [ 3.,  1.]])
    # >>>
    # >>> m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    # >>> print(m, c)
    # 1.0 -0.95
    mc, _, _, _ = np.linalg.lstsq(A, font_px_heights, rcond=None)
    print(font.name)
    models[font.name] = mc

with open('font_pt2px.pk', 'wb') as f:
    pickle.dump(models, f)
# plt.plot(xs,ys[i])
# plt.show()
