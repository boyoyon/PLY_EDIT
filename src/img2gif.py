import imageio
import numpy as np
import cv2, glob, os, sys

def make_gif(frames, filename, fps=30, loop=0):
    imageio.mimsave(filename, frames, 'GIF', fps=fps, loop=loop)

def main():
    argv = sys.argv
    argc = len(argv)

    print('%s creates GIF from images' % argv[0])
    print('[usage] python %s <wildcard for images> [<fps> <nrLoops>]' % argv[0])

    if argc < 2:
        quit()

    fps = 30
    if argc > 2:
        fps = int(argv[2])
   
    nrLoops = 0
    if argc > 3:
        nrLoops = int(argv[3])

    frames = []
    paths = glob.glob(argv[1])
    nrData = len(paths)

    for i, path in enumerate(paths):
        print('processing %d/%d: %s' % ((i+1), nrData, path))
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frames.append(img)

    make_gif(frames, 'output.gif', fps=fps, loop=nrLoops)
    print('save output.gif')

if __name__ == "__main__":
    main()
