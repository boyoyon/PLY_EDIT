import numpy as np
import os, sys

argv = sys.argv
argc = len(argv)

print('%s translates data' % argv[0])
print('[usage] python %s <.npy> <offst x> <offset y> <offset z>' % argv[0])

if argc < 5:
    quit()

data = np.load(argv[1])
offset_x = float(argv[2])
offset_y = float(argv[3])
offset_z = float(argv[4])

data += (offset_x, offset_y, offset_z)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_translated.npy' % filename

np.save(dst_path, data)
print('save %s' % dst_path)




