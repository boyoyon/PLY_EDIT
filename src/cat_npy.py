import glob, sys
import numpy as np

argv = sys.argv
argc = len(argv)

print('%s concatenates .npy' % argv[0])
print('[usage] python %s <wildcard for .npy>' % argv[0])
print('[usage] python %s <.npy #1> <.npy #2> ...' % argv[0])

if argc < 2:
    quit()

paths = []

if argc < 3:
    paths = glob.glob(argv[2])

else:

   for i in range(1, argc):
       paths.append(argv[i])

data = None

for i, path in enumerate(paths):

    _data = np.load(path)
    print('%d: %d, %d, %d' % (i, _data.shape[0], _data.shape[1], _data.shape[2]))

    if i == 0:
        data = _data
    else:
        data = np.vstack((data, _data))

dst_path = 'stacked.npy'
np.save(dst_path, data)
print('save %s' % dst_path)
   

