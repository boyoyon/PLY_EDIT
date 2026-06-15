import numpy as np
from scipy.interpolate import make_interp_spline
import sys

argv = sys.argv
argc = len(argv)

print('%s interpolates points' % argv[0])
print('[usage] python %s <.npy>' % argv[0])

if argc < 2:
    quit()

points = np.load(argv[1])

distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
t = np.concatenate(([0], np.cumsum(distances)))

spline_x = make_interp_spline(t, points[:, 0], k=3)
spline_y = make_interp_spline(t, points[:, 1], k=3)
spline_z = make_interp_spline(t, points[:, 2], k=3)

t_fine = np.linspace(t[0], t[-1], points.shape[0] * 10)
smooth_points = np.vstack((spline_x(t_fine), spline_y(t_fine), spline_z(t_fine))).T

dst_path = 'interpolated.npy'
np.save(dst_path, smooth_points)
print('save %s' % dst_path)