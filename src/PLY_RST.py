import copy, cv2, glob, os, sys
import numpy as np
import open3d as o3d

def getRotationMatrix(idx, angle):

    rotate = None

    if idx == 0:
        rotate = np.array([[1, 0, 0, 0],
            [0, np.cos(angle), -np.sin(angle), 0],
            [0, np.sin(angle), np.cos(angle), 0],
            [0, 0, 0, 1]])

    elif idx == 1:
        rotate = np.array([[np.cos(angle), 0, np.sin(angle), 0],
            [0, 1, 0, 0],
            [-np.sin(angle), 0, np.cos(angle), 0],
            [0, 0, 0, 1]])

    elif idx == 2:
        rotate = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
            [np.sin(angle), np.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

    return rotate

def getTranslationMatrix(t):

    translate = np.array(
       [[1, 0, 0, t[0]],
        [0, 1, 0, t[1]],
        [0, 0, 1, t[2]],
        [0, 0, 0, 1]])

    return translate

def getScalingMatrix(s):

    scale = np.array([
        [s[0], 0,    0,    0],
        [0,    s[1], 0,    0],
        [0,    0,    s[2], 0],
        [0,    0,    0,    1]])

    return scale

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s Rotates, Scales, Translates ply' % argv[0])
    print('%s <mesh ply> <wildcard for procedures(.txt)>' % argv[0])
    print('%s <mesh ply> <procesure 1> <procedure2 > ...' % argv[0]) 

    if argc < 2:
        quit()

    mesh =  o3d.io.read_triangle_mesh(argv[1])
    mesh_orig = copy.deepcopy(mesh)

    paths = []

    if argc > 2:
        for i in range(2, argc):
            paths.append(argv[i])

    else:
        paths = glob.glob(argv[2])

    
    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]
    dst_path = '%s_modified.ply' % filename
  
    accum = None 
    fNeedToSave = False
 
    for path in paths:

        with open(path, mode='r', encoding='utf-8') as f:
            lines = f.read().split('\n') 

        fGrouping = False
        fRepeatCount = False
        Maccum = np.eye(4)

        fRotate = False
        fAxis = False
        fScale = False
        fTranslate = False
        fRotateRepeat = False
        fScaleRepeat = False
        fTranslateRepeat = False

        count = -1
        axis = -1
        angle = 0
        s = []
        t = []

        for line in lines:
            words = line.split(' ')

            for word in words:

                if len(word) < 1 or word[0] == '#':
                    break 
           
                elif fRotate:

                    if fAxis:

                        angle = np.deg2rad(float(eval(word)))
                        rotate = getRotationMatrix(axis, angle)

                        if fGrouping:
                            Maccum = Maccum @ rotate
                        else:
                            mesh.transform(rotate)

                        fNeedToSave = True
                        fRotate = False
                        fAxis = False
                        axis = -1
                        angle = 0

                    else:

                        if word == 'x' or word == 'X':
                            axis = 0
                        elif word == 'y' or word == 'Y':
                            axis = 1
                        elif word == 'z' or word == 'Z':
                            axis = 2
                        
                        fAxis = True

                elif fRotateRepeat:

                    if fRepeatCount:

                        if fAxis:

                            angle = np.deg2rad(float(eval(word)))
                            rotate = getRotationMatrix(axis, angle)

                            for i in range(count):
                                mesh.transform(rotate)

                                if i == 0:
                                    accum = copy.deepcopy(mesh)
                                   
                                else:
                                    accum += copy.deepcopy(mesh)

                            mesh = copy.deepcopy(accum)

                            fNeedToSave = True
                            fRotateRepeat = False
                            fRepeatCount = False
                            count = -1
                            fAxis = False
                            axis = -1
                            angle = 0

                        else:

                            if word == 'x' or word == 'X':
                                axis = 0
                            elif word == 'y' or word == 'Y':
                                axis = 1
                            elif word == 'z' or word == 'Z':
                                axis = 2

                            fAxis = True

                    else:

                        count = int(word)
                        fRepeatCount = True    
            

                elif fScale:

                    s.append(float(eval(word)))

                    if len(s) == 3:

                        scale = getScalingMatrix(s)

                        if fGrouping:
                            Maccum = Maccum @ scale
                        else:
                            mesh.transform(scale)

                        fNeedToSave = True
                        fScale = False    

                elif fScaleRepeat:

                    if fRepeatCount:

                        s.append(float(eval(word)))

                        if len(s) == 3:

                            scale = getScalingMatrix(s)

                            for i in range(count):
                                mesh.transform(scale)

                                if i == 0:
                                    accum = copy.deepcopy(mesh)
                                   
                                else:
                                    accum += copy.deepcopy(mesh)

                            mesh = copy.deepcopy(accum)

                            fNeedToSave = True
                            fScaleRepeat = False
                            fRepeatCount = False 
                            count = -1
                            s = []
                    else:

                        count = int(word)
                        fRepeatCount = True

                elif fTranslate:

                    t.append(float(eval(word)))

                    if len(t) == 3:
                        translate = getTranslationMatrix(t)

                        if fGrouping:
                            Maccum = Maccum @ translate
                        else:
                            mesh.transform(translate)

                        fNeedToSave = True
                        fTranslate = False 

                elif fTranslateRepeat:

                    if fRepeatCount:

                        t.append(float(eval(word)))

                        if len(t) == 3:

                            translate = getTranslationMatrix(t)

                            for i in range(count):

                                mesh.transform(translate)
                                
                                if i == 0:
                                    accum = copy.deepcopy(mesh)
                                   
                                else:
                                    accum += copy.deepcopy(mesh)

                            mesh = copy.deepcopy(accum)

                            fNeedToSave = True
                            fTranslateRepeat = False 
                            fRepeatCount = False
                            count = -1
                            t = []

                    else:
                        count = int(word)
                        fRepeatCount = True

                elif fGrouping and not fRepeatCount:

                    count = int(word)
                    fRepeatCount = True

                elif word == 'r' or word == 'R':
                    fRotate = True
                    axis = -1
                    angle = 0

                elif word == 'rr' or word == 'RR':
                    fRotateRepeat = True
                    count = -1
                    axis = -1
                    angle = 0

                elif word == 's' or word == 'S':
                    fScale = True
                    s = []

                elif word == 'ss' or word == 'SS':
                    fScaleRepeat = True
                    count = -1
                    s = []

                elif word == 't' or word == 'T':
                    fTranslate = True
                    t = []
        
                elif word == 'tt' or word == 'TT':
                    fTranslateRepeat = True
                    count = -1
                    t = []
        
                elif word == 'g' or word == 'G':
                    fGrouping = True
                    fRepeatCount = False
                    count = 1
                    
                elif '.ply' in word:
                    dst_path = word
                    if fNeedToSave:

                        if fGrouping:
                            
                            for i in range(count):
                                
                                mesh.transform(Maccum)
                               
                                if i == 0:
                                    accum = copy.deepcopy(mesh)
                                else:
                                    accum += copy.deepcopy(mesh)

                            mesh = copy.deepcopy(accum)

                            fGrouping = False
                            fRepeatCount = False
                            count = -1
                            Maccum = np.eye(4)

                        o3d.io.write_triangle_mesh(dst_path, mesh)
                        print('save %s' % dst_path)
                        fNeedToSave = False
                        mesh = copy.deepcopy(mesh_orig)

        if fNeedToSave: 
            base = os.path.basename(argv[1])
            filename = os.path.splitext(base)[0]
            dst_path = '%s_modified.ply' % filename
   
            o3d.io.write_triangle_mesh(dst_path, mesh)
            print('save %s' % dst_path)
            fNeedToSave = False

if __name__ == '__main__':
    main()
