import numpy as np
import open3d as o3d
import os, sys

argv = sys.argv
argc = len(argv)

print('%s thinning .npy' % argv[0])
print('[usage] python %s <.npy> <final scale>' % argv[0])

if argc < 3:
    quit()

data = np.load(argv[1])
print(data.shape)

nr_layers = data.shape[0]
nr_points = data.shape[1]

final_scale = float(argv[2])

step = (1 - final_scale) /(nr_layers - 1)

for layer_idx in range(nr_layers):

    scale = 1 - step * layer_idx

    data[layer_idx,:,0] *= scale
    data[layer_idx,:,2] *= scale

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_thinned.npy' % filename

np.save(dst_path, data)
print('save %s' % dst_path) 
