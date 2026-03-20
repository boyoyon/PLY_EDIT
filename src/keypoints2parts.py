import os, sys
import numpy as np

argv = sys.argv
argc = len(argv)

print('%s creates parts description from pose landmarks' % argv[0])
print('[usage] python %s <landmarks .npy>' % argv[0])

if argc < 2:
    quit()

p = np.load(argv[1])

lines = []

"""
# 左目

line = 'p clear\n'
lines.append(line)

for i in (0, 4, 5, 6, 8):
    line = 'p %f %f %f\n' % (p[i][0], p[i][1], p[i][2]) 
    lines.append(line)

line = 'polyline\n'
lines.append(line)

# 右目

line = 'p clear\n'
lines.append(line)

for i in (0, 1, 2, 3, 7):
    line = 'p %f %f %f\n' % (p[i][0], p[i][1], p[i][2]) 
    lines.append(line)

line = 'polyline\n'
lines.append(line)

# 口

line = 'p clear\n'
lines.append(line)

for i in (10, 9):
    line = 'p %f %f %f\n' % (p[i][0], p[i][1], p[i][2]) 
    lines.append(line)

line = 'polyline\n'
lines.append(line)
"""

# 胴

line = 'p clear\n'
lines.append(line)

for i in (12, 11, 23, 24):
    line = 'p %f %f %f\n' % (p[i][0], p[i][1], p[i][2]) 
    lines.append(line)

line = 'POLYLINE\n'
lines.append(line)

# 左腕

line = 'p clear\n'
lines.append(line)

for i in (12, 14, 16):
    line = 'p %f %f %f\n' % (p[i][0], p[i][1], p[i][2]) 
    lines.append(line)

line = 'polyline\n'
lines.append(line)

# 右腕

line = 'p clear\n'
lines.append(line)

for i in (11, 13, 15):
    line = 'p %f %f %f\n' % (p[i][0], p[i][1], p[i][2]) 
    lines.append(line)

line = 'polyline\n'
lines.append(line)

# 左足

line = 'p clear\n'
lines.append(line)

for i in (24, 26, 28):
    line = 'p %f %f %f\n' % (p[i][0], p[i][1], p[i][2]) 
    lines.append(line)

line = 'polyline\n'
lines.append(line)

# 右足

line = 'p clear\n'
lines.append(line)

for i in (23, 25, 27):
    line = 'p %f %f %f\n' % (p[i][0], p[i][1], p[i][2]) 
    lines.append(line)

line = 'polyline\n'
lines.append(line)

line = 'sphere 0.1\n'
lines.append(line)

line = 't %f %f %f\n' % (p[0][0], p[0][1], p[0][2])
lines.append(line)

line = 'merge\n'
lines.append(line)


dst_path = 'skeleton.txt'

with open(dst_path, mode='w') as f:
    for line in lines:
        f.write(line)

print('save %s' % dst_path)



