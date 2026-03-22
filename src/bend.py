import numpy as np
import open3d as o3d
import copy, os, sys

argv = sys.argv
argc = len(argv)

print('%s bends .npy' % argv[0])
print('[usage] python %s <.npy> <angle:degree>[<mode:0/1/2/3>]' % argv[0])

if argc < 2:
    quit()

path = argv[1]

ANGLE = np.deg2rad(float(argv[2]))

mode = 0
if argc > 3:
    mode = int(argv[3])

if mode == 0:
    sign1 = -1
    sign2 = -1
elif mode == 1:
    sign1 = -1
    sign2 = 1
elif mode == 2:
    sign1 = 1
    sign2 = -1
elif mode == 3:
    sign1 = 1
    sign2 = 1
else:
    sign1 = -1
    sign2 = -1
 
r = 1
if argc > 3:
    r = float(argv[3])

s = 1
if argc > 4:
    s = float(argv[4])

print(path)

data = np.load(path)
print(data.shape)

nr_layers = data.shape[0]
nr_points = data.shape[1]

z_min = np.min(data[:,:,2])
z_max = np.max(data[:,:,2])
z_width = z_max - z_min

z0 = sign1 * z_width * r
step = sign2 * ANGLE/(nr_layers - 1)
scale_step = (1 - s) / (nr_layers - 1)

for layer_idx in range(1, nr_layers):

    angle = step * layer_idx
    R = o3d.geometry.get_rotation_matrix_from_xyz((angle, 0, 0))
    scale = 1 - scale_step * layer_idx
   
    _q0 = [0, 0, z0]
    _q = R @ _q0

    for p_idx in range(nr_points):

        _p = data[layer_idx][p_idx]
        _p[1] = 0
        _p[0] *= scale
        _p[2] *= scale
        _p = R @ _p
        data[layer_idx][p_idx] = _p + _q - _q0

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_bended.npy' % filename
np.save(dst_path, data)
print('save %s' % dst_path) 

