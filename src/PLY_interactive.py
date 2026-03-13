import open3d as o3d
import numpy as np
import threading
import queue
import copy, io, os, subprocess, sys
from polygon import polygon, polyline, get_rotation_to_vector
from sphere import sphere
from getValues import Eval, Evals
from draw import getDrawingPoints
from RST import *

LINES = []
input_queue = None

ctrl = None

KEY_LEFT  = 263
KEY_RIGHT = 262
KEY_UP    = 265
KEY_DOWN  = 264

MIN_VALUE = 0.0000001

angle_step = np.pi / 180
translation_step = 0.01
scale_up = 1.01
scale_down = 0.99

def input_thread():

    while True:
        if len(LINES) > 0:
            line = LINES.pop(0)
            input_queue.put(line)
            print(line)
            if len(LINES) == 0:
                print('complete script')

        else:
            line = sys.stdin.readline().strip()
            if line:
                input_queue.put(line)

def refresh(vis, meshes, fAxis):
                    
    vis.clear_geometries()

    start = 0

    if not fAxis:
        start = 1

    for i in range(start, len(meshes)):
        vis.add_geometry(meshes[i])           

def usageP(Points):
      print('p: display current points')
      print('p clear: clear points')
      print('p xx xx xx: append the point to points')
      print('p polygon: append polygon vertices to points')
      print('p curve (range T) (eq.X with T) (eq.Y with T) (eq.Z with T): append cueve to points')
      print('p centering: centering points')
      print('p r xx xx xx : rotate points')
      print('p s xx xx xx : scale points')
      print('p t xx xx xx : translate points')
      print('p g (array of r/s/t commands) : apply group operation to points')
      print('l xxxx.npy: load points into Points[]')
      print('Points[]=',Points)

def key_callback_d(vis, action, mod):
    pass # supress depth capture

def key_callback_p(vis, action, mod):
    pass # supress screen capture

def key_callback_updown_angle_step(vis, action, mods):

    global angle_step, translation_step

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    if shift_pressed:

        if ctrl_pressed:
            
            angle_step *= 1.5

        else:

            angle_step *= 1.1
    else:

        if ctrl_pressed:
            
            angle_step *= 0.5

        else:

            angle_step *= 0.9

    return True

def key_callback_updown_translation_step(vis, action, mods):

    global angle_step, translation_step

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    if shift_pressed:

        if ctrl_pressed:
            
            translation_step *= 1.5

        else:

            translation_step *= 1.1
    else:

        if ctrl_pressed:
            
            translation_step *= 0.5

        else:

            translation_step *= 0.9

    return True

def key_callback_1(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    if shift_pressed:
        angle = -angle_step
    else:
        angle = angle_step

    if ctrl_pressed:
        angle *= 10

    rotation = np.array([[np.cos(angle), 0, np.sin(angle), 0],
        [0, 1, 0, 0],
        [-np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]])

    extrinsic = param.extrinsic.copy()
    T = np.eye(4)
    T[:,3] = extrinsic[:,3]
    T_inv = np.linalg.inv(T)
    transform = T @ rotation @ T_inv @ extrinsic
    param.extrinsic = transform
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_2(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    if shift_pressed:
        angle = -angle_step
    else:
        angle = angle_step

    if ctrl_pressed:
        angle *= 10

    rotation = np.array([[1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]])

    extrinsic = param.extrinsic.copy()
    T = np.eye(4)
    T[:,3] = extrinsic[:,3]
    T_inv = np.linalg.inv(T)
    transform = T @ rotation @ T_inv @ extrinsic
    param.extrinsic = transform
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_3(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    if shift_pressed:
        angle = -angle_step
    else:
        angle = angle_step

    if ctrl_pressed:
        angle *= 10

    rotation = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    extrinsic = param.extrinsic.copy()
    T = np.eye(4)
    T[:,3] = extrinsic[:,3]
    T_inv = np.linalg.inv(T)
    transform = T @ rotation @ T_inv @ extrinsic
    param.extrinsic = transform
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_4(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    if shift_pressed:
        offset = -translation_step
    else:
        offset = translation_step

    if ctrl_pressed:
        offset *= 10

    translate = np.array([[1, 0, 0, offset],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    extrinsic = param.extrinsic.copy()
    T = np.eye(4)
    T[:,3] = extrinsic[:,3]
    T_inv = np.linalg.inv(T)
    transform = T @ translate @ T_inv @ extrinsic
    param.extrinsic = transform
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_42(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    if shift_pressed:
        offset = -translation_step
    else:
        offset = translation_step

    if ctrl_pressed:
        offset *= 10

    translate = np.array([[1, 0, 0, -offset],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    extrinsic = param.extrinsic.copy()
    T = np.eye(4)
    T[:,3] = extrinsic[:,3]
    T_inv = np.linalg.inv(T)
    transform = T @ translate @ T_inv @ extrinsic
    param.extrinsic = transform
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_5(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    if shift_pressed:
        offset = -translation_step
    else:
        offset = translation_step

    if ctrl_pressed:
        offset *= 10

    translate = np.array([[1, 0, 0, 0],
        [0, 1, 0, offset],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    extrinsic = param.extrinsic.copy()
    T = np.eye(4)
    T[:,3] = extrinsic[:,3]
    T_inv = np.linalg.inv(T)
    transform = T @ translate @ T_inv @ extrinsic
    param.extrinsic = transform
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_6(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    if shift_pressed:
        offset = -translation_step
    else:
        offset = translation_step

    if ctrl_pressed:
        offset *= 10

    translate = np.array([[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, offset],
        [0, 0, 0, 1]])

    extrinsic = param.extrinsic.copy()
    T = np.eye(4)
    T[:,3] = extrinsic[:,3]
    T_inv = np.linalg.inv(T)
    transform = T @ translate @ T_inv @ extrinsic
    param.extrinsic = transform
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_X(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    transform = np.array([[np.cos(-np.pi/2), 0, -np.sin(-np.pi/2), 0],
        [0, 1, 0, 0],
        [np.sin(-np.pi/2), 0, np.cos(-np.pi/2), 3.0],
        [0, 0, 0, 1]])

    Rx = np.array([[1,              0,              0,              0],
                  [0,               np.cos(np.pi),  -np.sin(np.pi), 0],
                  [0,               np.cos(np.pi),  np.cos(np.pi),  0],
                  [0,               0,              0,              1]])

    param.extrinsic = transform @ Rx
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_Y(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    # 外部パラメータの算出方法がわからなかったので取得した値をそのまま設定...

    E = np.array([[ 6.12323400e-17, 1.22464680e-16, -1.00000000e+00, -1.47911420e-31],
        [ 9.99991074e-01,  4.22513628e-03,  6.17492234e-17,  1.18481613e-15],
        [ 4.22513628e-03, -9.99991074e-01, -1.22204872e-16,  3.00000000e+00],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])


    param.extrinsic = E
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_Z(vis, action, mods):

    param = ctrl.convert_to_pinhole_camera_parameters()

    # 外部パラメータの算出方法がわからなかったので取得した値をそのまま設定...

    E = np.array([[ 9.99997484e-01,  2.74701742e-19, -2.24310995e-03,  3.81639165e-17],
        [ 0.00000000e+00, -1.00000000e+00, -1.22464680e-16,  3.94430453e-31],
        [-2.24310995e-03,  6.27980454e-17, -9.99997484e-01,  3.00000000e+00],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])

    param.extrinsic = E
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)

    return False

def key_callback_reset_step(vis, action, mod):

    global angle_step, translation_step, scale

    angle_step = np.pi / 180
    translation_step = 0.005
    scale_up = 1.3
    scale_down = 0.7

    return True
    
def key_callback_scale_up(vis, action, mod):

    param = ctrl.convert_to_pinhole_camera_parameters()

    extrinsic = param.extrinsic.copy()
    T = np.eye(4)
    T[:,3] = extrinsic[:,3]
    T_inv = np.linalg.inv(T)
    T[:3,3] *= scale_down
    transform = T @ T_inv @ extrinsic
    param.extrinsic = transform
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)
    
    return True


def key_callback_scale_down(vis, action, mod):

    param = ctrl.convert_to_pinhole_camera_parameters()

    extrinsic = param.extrinsic.copy()
    T = np.eye(4)
    T[:,3] = extrinsic[:,3]
    T_inv = np.linalg.inv(T)
    T[:3,3] *= scale_up
    transform = T @ T_inv @ extrinsic
    param.extrinsic = transform
    ctrl.convert_from_pinhole_camera_parameters(param, allow_arbitrary=True)
    
    return True

def show_menu():

    print('コマンドを入力してください')
    print('calc/clear normals   : normals')
    print('capture screen       : cap (image name)')
    print('centerling mesh      : centering')
    print('control camera       : cam x/y/z')
    print('                     : cam rotate x/y/z (angle)')
    print('                     : cam translate x/y/z (offset)')
    print('create polygon       : polygon (no. of edges) (size) (height)')
    print('delete selected ply  : d')
    print('get points           : getPoints, or GETPoints')
    print('load ply             : l (.ply)')
    print('load script          : l (.txt)')
    print('on/off selected mesh : selected')
    print('on/off axis          : axis')
    print('paint with color     : c (r(0-255)) (g(0-255)) (b(0-255))')
    print('rotate mesh          : r (angle_x(degree)) (angle_y(degree)) (angle_z(degree)) [(count)]')
    print('save ply             : save (ply filename)')
    print('scale mesh           : s (scale_x) (scale_y) (scale_z) [(count)]')
    print('show menu            : menu')
    print('terminate program    : quit') 
    print('translate mesh       : t (offset_x) (offset_y) (offset_z) [(count)]')
    print('undo                 : u')
    print()

def update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh):

    if len(meshes) > 1: # meshes[0]: axisXYZ
    
        undo_idx.append(curr)
        undo_mesh.append(copy.deepcopy(meshes[curr]))
        undo_name.append(names[curr])

def main():

    global input_queue, LINES, ctrl, angle_step, translation_step
               
    argv = sys.argv
    argc = len(argv)
    
    print('%s creates and edits meshes' % argv[0])
    print('[usage] python %s [(screen width) (screen height)]' % argv[0])    

    width = 800

    if argc > 1 and argv[1].isdecimal():
        width = int(argv[1])
 
    height = 600
 
    if argc > 2 and argv[2].isdecimal():
        height = int(argv[2])
    
    meshes = []
    names = []
    mesh = None
    curr = 0
    names.append('')
    fSelectedOnly = False
    fAxis = True
    
    undo_mesh = []
    undo_name = []
    undo_idx = []
   
    SurfaceOuter = [128,128,255]
    SurfaceInner = [200,200,255]
    LateralOuter = [128,128,255]
    LateralInner = [200,200,255]
    PaddingOuter = [128,128,255]
    PaddingInner = [200,200,255]

    Points = []
    
    EyePos = None    
 
    input_queue = queue.Queue()
    
    threading.Thread(target=input_thread, daemon=True).start()
    
    # 可視化の準備
    #vis = o3d.visualization.Visualizer()
    vis = o3d.visualization.VisualizerWithKeyCallback()

    vis.register_key_action_callback(ord('D'), key_callback_d)
    vis.register_key_action_callback(ord('P'), key_callback_p)

    vis.register_key_action_callback(ord("0"), key_callback_reset_step)
    vis.register_key_action_callback(ord("1"), key_callback_1)
    vis.register_key_action_callback(ord("2"), key_callback_2)
    vis.register_key_action_callback(ord("3"), key_callback_3)
    vis.register_key_action_callback(ord("4"), key_callback_4)
    vis.register_key_action_callback(ord("5"), key_callback_5)
    vis.register_key_action_callback(ord("6"), key_callback_6)
    vis.register_key_action_callback(ord("7"), key_callback_updown_angle_step)
    vis.register_key_action_callback(ord("8"), key_callback_updown_translation_step)
    vis.register_key_action_callback(ord("X"), key_callback_X)
    vis.register_key_action_callback(ord("Y"), key_callback_Y)
    vis.register_key_action_callback(ord("Z"), key_callback_Z)
    vis.register_key_action_callback(KEY_UP, key_callback_scale_up)
    vis.register_key_action_callback(KEY_UP, key_callback_scale_up)
    vis.register_key_action_callback(KEY_UP, key_callback_scale_up)
    vis.register_key_action_callback(KEY_UP, key_callback_scale_up)
    vis.register_key_action_callback(KEY_DOWN, key_callback_scale_down)
    vis.register_key_action_callback(KEY_LEFT, key_callback_42)
    vis.register_key_action_callback(KEY_RIGHT, key_callback_4)

    vis.create_window(window_name='PLY Edit interactivelly', width=width, height=height)
    
    axis = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'axisXYZ.ply'))
    meshes.append(axis)
    
    vis.add_geometry(axis)
    
    ctrl = vis.get_view_control()
    ctrl.set_front([0.5, 0.25, 0.5])
    
    show_menu()
    screenNo = 1
    
    LINES = []

    while True:
    
        try:
            # キューからコマンドを取得
            #cmds = input_queue.get_nowait().split(' ')
            cmds = input_queue.get_nowait().split('#')[0]
            cmds = cmds.split()
   
            if len(cmds) == 0 or len(cmds[0]) == 0:
                continue
    
            if cmds[0] == 'm':
    
                show_menu()
    
            elif cmds[0] == 'l':
    
                if len(cmds) < 2:
                    print('file is not specified. skip...')
                elif not os.path.exists(cmds[1]):
                    print('%s does not exist or not ply. skip...' % cmds[1])
                else:
                    ext = os.path.splitext(cmds[1])[1]
               
                    if ext == '.ply':
    
                        mesh = o3d.io.read_triangle_mesh(cmds[1])           
         
                        vis.add_geometry(mesh)
                        ctrl.set_front([0.5, 0.25, 0.5])
        
                        meshes.append(mesh)
                        base = os.path.basename(cmds[1])
                        name0 = os.path.splitext(base)[0]
                        name = '%s' % name0
                        no = 2
                        while name in names:
                            name = '%s(%d)' % (name0, no)
                            no += 1
                        names.append(name)

                        curr = len(meshes) - 1
        
                        vis.update_geometry(mesh)
    
                    elif ext == '.txt':
    
                        orig_stdin = sys.stdin
    
                        with open(cmds[1], mode='r', encoding='utf-8') as f:
                            lines = f.read().split('\n')
   
                        LINES.clear() 
                        for line in lines:
                            LINES.append(line)
   
                    elif ext == '.npy':

                        Points = []
                        Points = np.load(cmds[1]).tolist()
 
            elif cmds[0] == 'axis':
  
                if len(cmds) > 1:
                    if cmds[1] == 'off':
                        vis.remove_geometry(axis)
                    elif cmds[1] == 'on':
                        vis.add_geometry(axis)
                    else:
                        print('invalid parametar (%s)' % cmds[1])
                        continue
  
                elif fAxis:
                    vis.remove_geometry(axis)
                else:
                    vis.add_geometry(axis)
                    
                ctrl.set_front([0.5, 0.25, 0.5])
    
                fAxis = not fAxis
    
            elif cmds[0] == 'c':
  
                if len(meshes) < 2:
                    print('no meshes')
                    continue
 
                if len(cmds) > 3 and cmds[1].isdecimal() and cmds[2].isdecimal() and cmds[3].isdecimal():
                    red = int(cmds[1]) / 255
                    green = int(cmds[2]) / 255
                    blue = int(cmds[3]) / 255
    
                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)
 
                    meshes[curr].paint_uniform_color([red, green, blue])
                    vis.update_geometry(meshes[curr])

                else:
                    print('specify red(0-255) green(0-255) blue(0-255)')
                        
    
            elif cmds[0] == 'SurfaceOuter':
    
                if len(cmds) > 3 and cmds[1].isdecimal() and cmds[2].isdecimal() and cmds[3].isdecimal():
                    red = int(cmds[1]) / 255
                    SurfaceOuter = [int(cmds[1]),int(cmds[2]), int(cmds[3])]
    
                else:
                    print('specify red(0-255) green(0-255) blue(0-255)')

                print('Current Setting:', SurfaceOuter)
    
            elif cmds[0] == 'SurfaceInner':
    
                if len(cmds) > 3 and cmds[1].isdecimal() and cmds[2].isdecimal() and cmds[3].isdecimal():
                    SurfaceInner = [int(cmds[1]),int(cmds[2]), int(cmds[3])]
                
                else:
                    print('specify red(0-255) green(0-255) blue(0-255)')
    
                print('Current Setting:', SurfaceInner)
    
            elif cmds[0] == 'LateralOuter':
    
                if len(cmds) > 3 and cmds[1].isdecimal() and cmds[2].isdecimal() and cmds[3].isdecimal():
                    LateralOuter = [int(cmds[1]),int(cmds[2]), int(cmds[3])]
    
                else:
                    print('specify red(0-255) green(0-255) blue(0-255)')
                
                print('Current Setting:', LateralOuter)
    
            elif cmds[0] == 'LateralInner':
    
                if len(cmds) > 3 and cmds[1].isdecimal() and cmds[2].isdecimal() and cmds[3].isdecimal():
                    LateralInner = [int(cmds[1]),int(cmds[2]), int(cmds[3])]
    
                else:
                    print('specify red(0-255) green(0-255) blue(0-255)')
                
                print('Current Setting:', LateralInner)
    
            elif cmds[0] == 'PaddingOuter':
    
                if len(cmds) > 3 and cmds[1].isdecimal() and cmds[2].isdecimal() and cmds[3].isdecimal():
                    PaddingOuter = [int(cmds[1]),int(cmds[2]), int(cmds[3])]
    
                else:
                    print('specify red(0-255) green(0-255) blue(0-255)')
                
                print('Current Setting:', PaddingOuter)
    
            elif cmds[0] == 'PaddingInner':
    
                if len(cmds) > 3 and cmds[1].isdecimal() and cmds[2].isdecimal() and cmds[3].isdecimal():
                    PaddingInner = [int(cmds[1]),int(cmds[2]), int(cmds[3])]
    
                else:
                    print('specify red(0-255) green(0-255) blue(0-255)')
                
                print('Current Setting:', PaddingInner)

            elif cmds[0] == 'selected':
    
                print(names[curr])
    
                fSelectedOnly = not fSelectedOnly
                if fSelectedOnly and len(meshes) > 2:
                    print('not selected meshes are hidden') 
   
                vis.clear_geometries()
              
                start = 0
                if not fAxis:
                    start = 1
     
                for i in range(start, len(meshes)):
               
                    if i == 0 or i == curr:
                        vis.add_geometry(meshes[i])
    
                    else:
                        if not fSelectedOnly:
                            vis.add_geometry(meshes[i])

                ctrl.set_front([0.5, 0.25, 0.5])
    
            elif cmds[0] == 'select':
    
                try:
                    idx = names.index(cmds[1])
                except ValueError:
                    print('select from ', names)
    
                except IndexError:
                    print('select from ', names)
                else:
                    curr = idx
   
            elif cmds[0] == 'merge':

                if len(meshes) > 1:

                    accum = copy.deepcopy(meshes[1])
                    vis.remove_geometry(meshes[1])

                    for i in range(2, len(meshes)):
                        accum += copy.deepcopy(meshes[i])
                        vis.remove_geometry(meshes[i])

                    meshes.clear()
                    meshes.append(axis)
                    meshes.append(copy.deepcopy(accum))
                    
                    curr = 1
                    vis.add_geometry(meshes[curr])

                    names.clear()
                    names.append('') # axis
                    names.append('merged')
                    undo_idx.clear()
                    undo_mesh.clear()
                    undo_name.clear()
 
                ctrl.set_front([0.5, 0.25, 0.5])
    
            elif cmds[0] == 'd':
                
                if len(meshes) > 1:

                    if len(cmds) > 1 and cmds[1] == 'all':

                        for i in range(1, len(meshes)):
                       
                            vis.remove_geometry(meshes[i])
                     
                        meshes.clear()
                        meshes.append(axis)
                        names.clear()
                        names.append('')
                        undo_idx.clear()
                        undo_mesh.clear()
                        undo_name.clear()
                        curr = 0

                    else:

                        vis.remove_geometry(meshes[curr])
   
                        update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)
                        meshes.pop(curr)
                        names.pop(curr)
                        curr = len(meshes) - 1
    
                    ctrl.set_front([0.5, 0.25, 0.5])
                    
                else:
                    print('unable to delete')
                   
            elif cmds[0] == 'r':
   
                if len(meshes) < 2:
                    print('no mesh') 
                    continue
   
                R = getRotateMatrix(cmds[1:])

                if R is not None:

                    count = 0

                    if len(cmds) > 4:

                        if cmds[4].isdecimal(): 
                            count = int(cmds[4])
                        else:
                            usageRotate()
                            continue

                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)

                    if count < 2:
                        meshes[curr].rotate(R, center=(0,0,0))
                        vis.update_geometry(meshes[curr])

                    else:
                        accum = copy.deepcopy(meshes[curr])

                        for i in range(count - 1):
                            meshes[curr].rotate(R, center=(0,0,0))
                            accum += copy.deepcopy(meshes[curr])
                    
                        meshes[curr] = copy.deepcopy(accum)

                    refresh(vis, meshes, fAxis)
                    ctrl.set_front([0.5, 0.25, 0.5])
     
            elif cmds[0] == 's':
   
                if len(meshes) < 2:
                    print('no mesh')
                    continue 
 
                S = getScaleMatrix(cmds[1:])

                if S is not None:
 
                    count = 0
    
                    if len(cmds) > 4:

                        if cmds[4].isdecimal():
                            count = int(cmds[4])
                        else:
                            usageScale()
                            continue
    
                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)
    
                    if count < 2:
                        meshes[curr].transform(S)
                        vis.update_geometry(meshes[curr])
    
                    else:
                        accum = copy.deepcopy(meshes[curr])
                        for i in range(count - 1):
                            meshes[curr].transform(S)
                            accum += copy.deepcopy(meshes[curr])
                        
                        meshes[curr] = copy.deepcopy(accum)
    
                    refresh(vis, meshes, fAxis)
                    ctrl.set_front([0.5, 0.25, 0.5])
    
            elif cmds[0] == 't':
    
                if len(meshes) < 2:
                    print('no mesh')
                    continue

                T = getTranslateMatrix(cmds[1:])
                 
                if T is not None:

                    count = 0
    
                    if len(cmds) > 4:

                        if cmds[4].isdecimal():
                            count = int(cmds[4])
                        else:
                            usageTranslate()
                            continue     

                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)
 
                    if count < 2:
                        meshes[curr].transform(T)
                        vis.update_geometry(meshes[curr])
    
                    else:
                        accum = copy.deepcopy(meshes[curr])
                        
                        for i in range(count - 1):
                            meshes[curr].transform(T)
                            accum += copy.deepcopy(meshes[curr])
                        
                        meshes[curr] = copy.deepcopy(accum)
    
                    refresh(vis, meshes, fAxis)
                    ctrl.set_front([0.5, 0.25, 0.5])
    
            elif cmds[0] == 'g':
    
                if len(meshes) < 2:
                    print('no mesh')
                    continue

                G, fRemain = getGroupMatrix(cmds[1:])

                if G is not None:
        
                    count = 0
                    accum = None
    
                    if fRemain:

                        if cmds[-1].isdecimal(): 
                            count = int(cmds[-1])
                        else:
                            usageGroup()
                            continue 
   
                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)
 
                    if count < 2:
                        meshes[curr].transform(G)
                        vis.update_geometry(meshes[curr])
    
                    else:
                        accum = copy.deepcopy(meshes[curr])
                        
                        for i in range(count - 1):
                            meshes[curr].transform(G)
                            accum += copy.deepcopy(meshes[curr])
                        
                        if accum is not None:
                            meshes[curr] = copy.deepcopy(accum)
    
                            refresh(vis, meshes, fAxis)
                            ctrl.set_front([0.5, 0.25, 0.5])

                        else:
                            print('no meshes added')
    
            elif cmds[0] == 'polygon':
    
                _meshes, _names = polygon(cmds, False, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner) # lowercase --> separate mode
    
                if len(_meshes) > 0:
    
                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)

                    for i in range(len(_meshes)):
    
                        vis.add_geometry(_meshes[i])
    
                        meshes.append(_meshes[i])

                        name0 = _names[i]
                        name = '%s' % name0
                        no = 2
                        while name in names:
                            name = '%s(%d)' % (name0, no)
                            no += 1
                        names.append(name)

                    curr = len(meshes) - 1
                    ctrl.set_front([0.5, 0.25, 0.5])
                    vis.update_geometry(mesh)
    
            elif cmds[0] == 'POLYGON':
    
                _meshes, _names = polygon(cmds, True, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner) # uppercase --> integrate mode
    
                if len(_meshes) > 0:
    
                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)
                    
                    vis.add_geometry(_meshes[0])
                    meshes.append(_meshes[0])

                    name0 = _names[0]
                    name = '%s' % name0
                    no = 2
                    while name in names:
                        name = '%s(%d)' % (name0, no)
                        no += 1
                    names.append(name)
    
                    curr = len(meshes) - 1
                    ctrl.set_front([0.5, 0.25, 0.5])
                    vis.update_geometry(mesh)

            elif cmds[0] == 'polyline' or cmds[0] == 'POLYLINE': 

                if cmds[0] == 'polyline': # open path
                    _meshes, _names = polyline(cmds, Points, False, True, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, PaddingOuter, PaddingInner)

                else: # closed path
                    _meshes, _names = polyline(cmds, Points, True, True, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, PaddingOuter, PaddingInner)

                if len(_meshes) > 0:

                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)

                    vis.add_geometry(_meshes[0])
                    meshes.append(_meshes[0])

                    name0 = _names[0]
                    name = '%s' % name0
                    no = 2
                    while name in names:
                        name = '%s(%d)' % (name0, no)
                        no += 1
                    names.append(name)
                   
                    curr = len(meshes) - 1
                    ctrl.set_front([0.5, 0.25, 0.5])
                    vis.update_geometry(mesh)

            elif cmds[0] == 'poly-line' or cmds[0] == 'POLY-LINE': 

                if cmds[0] == 'poly-line': # open path
                    _meshes, _names = polyline(cmds, Points, False, False, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner)

                else: # closed path
                    _meshes, _names = polyline(cmds, Points, True, False, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner)

                if len(_meshes) > 0:

                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)

                    vis.add_geometry(_meshes[0])
                    meshes.append(_meshes[0])

                    name0 = _names[0]
                    name = '%s' % name0
                    no = 2
                    while name in names:
                        name = '%s(%d)' % (name0, no)
                        no += 1
                    names.append(name)
                   
                    curr = len(meshes) - 1
                    ctrl.set_front([0.5, 0.25, 0.5])
                    vis.update_geometry(mesh)
            elif cmds[0] == 'sphere':

                _meshes, _names = sphere(cmds, LateralOuter, LateralInner)

                if len(_meshes) > 0:

                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)
                    
                    vis.add_geometry(_meshes[0])
                    meshes.append(_meshes[0])

                    name0 = _names[0]
                    name = '%s' % name0
                    no = 2
                    while name in names:
                        name = '%s(%d)' % (name0, no)
                        no += 1
                    names.append(name)
                    
                    curr = len(meshes) - 1
                    ctrl.set_front([0.5, 0.25, 0.5])
                    vis.update_geometry(mesh)
    
            elif cmds[0] == 'u':
    
                if len(undo_mesh) > 0:
    
                    idx = undo_idx.pop()
                    if idx < len(meshes):
                        vis.remove_geometry(meshes[idx])
                        meshes.pop(idx)
                        names.pop(idx)
 
                    mesh = undo_mesh.pop()
                    meshes.append(mesh)

                    name0 = undo_name.pop()
                    name = '%s' % name0
                    no = 2
                    while name in names:
                        name = '%s(%d)' % (name0, no)
                        no += 1
                    names.append(name)

                    curr = len(meshes) - 1    

                    vis.update_geometry(meshes[idx])
                    refresh(vis, meshes, fAxis)
                    ctrl.set_front([0.5, 0.25, 0.5])
    
                else:
                    print('undo buffer is empty')
    
            elif cmds[0] == 'save':
   
                accum = None
 
                if len(meshes) > 1:
                    
                    for i in range(1,len(meshes)):
                        if i == 1:
                            accum = copy.deepcopy(meshes[i])
                        else:
                            accum += meshes[i]

                    if accum is not None:
                        o3d.io.write_triangle_mesh(cmds[1], accum)
                        print('save %s' % cmds[1])
                else:
                    print('no meshes to be saved')
  
            elif cmds[0] == 'normals':

                if len(meshes) > 1:

                    if meshes[curr].has_vertex_normals():
                        print('clear normals')
                        meshes[curr].vertex_normals = o3d.utility.Vector3dVector([])
                    else:
                        print('calculate normals')
                        meshes[curr].compute_vertex_normals()

                else:
                    print('no meshes to be calculated normals')

            elif cmds[0] == 'centering':

                if len(meshes) > 1:

                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)

                    center = meshes[curr].get_center()
                    meshes[curr].translate(-center)

                    vis.update_geometry(meshes[curr])

                else:
                    print('no meshes to be centering')

            elif cmds[0] == 'i':

                if len(meshes) > 1:
                    vertices = np.array(meshes[curr].vertices)
                    xmin = np.min(vertices[:,0])
                    xmax = np.max(vertices[:,0])
                    xwidth = xmax - xmin

                    print('axis, width, tmin - tmax')
                    print('x\t%f\t%f\t-\t%f' % (xwidth, xmin, xmax))

                    ymin = np.min(vertices[:,1])
                    ymax = np.max(vertices[:,1])
                    ywidth = ymax - ymin

                    print('y\t%f\t%f\t-\t%f' % (ywidth, ymin, ymax))

                    zmin = np.min(vertices[:,2])
                    zmax = np.max(vertices[:,2])
                    zwidth = zmax - zmin

                    print('z\t%f\t%f\t-\t%f' % (zwidth, zmin, zmax))

                else:
                    print('no meshes')
            
            elif cmds[0] == 'p':

                if len(cmds) < 2:
                    usageP(Points)
                else:
                    if cmds[1] == 'clear':
                        Points.clear()
                        print('Points[] is cleared')

                    elif cmds[1] == 'polygon':

                        _meshes, _names = polygon(cmds[1:], False, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner)

                        if len(_meshes) > 0:

                            nr_points = int(cmds[2])

                            Points.clear()
                            if len(cmds) < 5:
                                _points = np.asarray(_meshes[0].vertices).tolist() 
                            else:
                                _points = np.asarray(_meshes[0].vertices).tolist()[::2]
                            Points = _points[:nr_points]

                    elif cmds[1] == 'curve':

                        if len(cmds) < 5:
                            usageP(Points)
                            continue

                        else:

                            fResult, value = Eval(cmds[2])

                            if fResult:
                                T = value
                            else:
                                usageP(Points)
                                continue

                            fResult, value = Eval(cmds[3],T)

                            if fResult:
                                X = value
                            else:
                                usageP(Points)
                                continue

                            fResult, value = Eval(cmds[4],T)

                            if fResult:
                                Y = value
                            else:
                                usageP(Points)
                                continue

                            fResult, value = Eval(cmds[5],T)

                            if fResult:
                                Z = value
                            else:
                                usageP(Points)
                                continue

                            Points.clear()
                            Points = list(zip(X,Y,Z))
    
                    elif cmds[1] == 'centering':

                        if len(Points) > 0:

                            _points = np.array(Points)
                            centroid = np.mean(_points, axis=0)
                            Points.clear()
                            Points = (_points - centroid).tolist()
                            print('centring points')
                            
                        else:
                            print('Points[] is empty')

                    elif cmds[1] == 'r':

                        if len(Points) > 0:
                        
                            R = getRotateMatrix(cmds[2:])

                            if R is not None:

                                for i, p in enumerate(Points):
                                    Points[i] = (R @ np.array(p)).tolist()
                                print('rotate points')
                            else:
                                usageP(Points)
                                continue

                        else:
                            print('Points[] is empty')

                    elif cmds[1] == 's':

                        if len(Points) > 0:
                        
                            s = getScaleMatrix(cmds[2:])

                            if s is not None:

                                S = s[:3,:3]

                                for i, p in enumerate(Points):

                                    v1 = np.array(p)
                                    Points[i] = (S @ np.array(p)).tolist()

                                print('scaling points')
                            else:
                                usageP(Points)
                                continue

                        else:
                            print('Points[] is empty')

                    elif cmds[1] == 't':

                        if len(Points) > 0:
                        
                            fResult, values = Evals(cmds[2:], 3)

                            if fResult:

                                for i, p in enumerate(Points):
                                    Points[i] = np.array(p) + np.array(values).tolist()
                                print('translate points')
                            else:
                                usageP(Points)
                                continue

                        else:
                            print('Points[] is empty')

                    elif cmds[1] == 'save':

                        if len(Points) > 0:

                            filename = 'Points'

                            if len(cmds) > 2:
                                filename = os.path.splitext(cmds[2])[0]

                            dst_path = '%s.npy' % filename

                            no = 2
                            while os.path.exists(dst_path):

                                dst_path = '%s_%d.npy' % (filename, no)
                                no += 1 

                            np.save(dst_path, np.array(Points))
                            print('save %s' % dst_path)

                        else:
                            print('Points[] is empty')
                        

                    elif len(cmds)== 4:

                        fResult, values = Evals(cmds[1:], 3)

                        if fResult: 
                            Points.append(values)
                            print('Points[]=', Points)

            elif cmds[0] == 'distribute':

                if len(Points) < 1:
                    print('Points[] is empty')

                elif len(cmds) > 1:

                    mesh = None
                    accum = None
                    mode = 0

                    if cmds[1].endswith('.ply'):
                        mesh = o3d.io.read_triangle_mesh(cmds[1])           

                        if len(cmds) > 2:

                            if cmds[2] == 'radial':
                                mode = 1
                            
                            elif cmds[2] == '-radial':
                                mode = 2

                    elif cmds[1] == 'sphere':
                        _meshes, _names = sphere(cmds[1:], LateralOuter, LateralInner)

                        if len(_meshes) > 0:
                            mesh = _meshes[0]
                        else:
                            print('no meshes created')

                    if mesh is not None:
                        
                        for i, p in enumerate(Points):
                            _mesh = copy.deepcopy(mesh)
   
                            if mode > 0:
                              
                                if mode == 2:
                                    R = o3d.geometry.get_rotation_matrix_from_xyz((0, np.pi,0))
                                    _mesh.rotate(R, center=(0,0,0))

                                R = get_rotation_to_vector(p)
                                _mesh.rotate(R, center=(0,0,0))
 
                            T = np.array([[1, 0, 0, p[0]],
                                          [0, 1, 0, p[1]],
                                          [0, 0, 1, p[2]],
                                          [0, 0, 0, 1]], np.float64)
    
                            _mesh.transform(T)
                            
                            if i == 0:
                                accum = copy.deepcopy(_mesh)
                            else:
                                accum += copy.deepcopy(_mesh)
  
                    update_undo_info(meshes, names, curr, undo_idx, undo_name, undo_mesh)
 
                    if accum is not None:
                        meshes.append(accum)
                    
                    no = 2
                    filename = cmds[1].split('.')[0]
                    name = '%s' % filename
                    while name in names:
                        name = '%s(%d)' % (filename, no)
                        no += 1
    
                    names.append(name)
                    curr = len(meshes) - 1
                    vis.add_geometry(meshes[curr])
                    ctrl.set_front([0.5, 0.25, 0.5])

                else:
                    print('distribute <ply>')
                    print('distribute ply to the places specidied by Points[]') 

            elif cmds[0] == 'cap':

                dst_path = 'screen.png'

                if len(cmds) < 2:
                    dst_path = '%04d.png' % screenNo
                else:
                    filename, ext = os.path.splitext(cmds[1])

                    if ext == '':
                        ext = '.png'

                    dst_path = '%s%s' % (filename, ext)
                    no = 1

                while os.path.exists(dst_path):

                    if len(cmds) < 2:
                        screenNo += 1
                        dst_path = '%04d.png' % screenNo

                    else:
                        no += 1
                        dst_path = '%s(%d)%s' % (filename, no, ext)

                vis.capture_screen_image(dst_path)
                print('save %s' % dst_path)

            elif cmds[0] == 'getEyePos':

                EyePos = ctrl.convert_to_pinhole_camera_parameters() 

                print('EyePos.extrinsic: ', EyePos.extrinsic)

            elif cmds[0] == 'setEyePos':

                if EyePos is not None:
                    ctrl.convert_from_pinhole_camera_parameters(EyePos)

            elif cmds[0] == 'getPoints' or cmds[0] == 'GETPoints':

                if len(meshes) > 1:

                    divider = 10
                    if len(cmds) > 2:
                        divider = int(cmds[2])

                    pcd = o3d.geometry.PointCloud()
                    pcd.points = meshes[curr].vertices
                    vertices = np.asarray(pcd.points)                    

                    minX = np.min(vertices[:,0])
                    maxX = np.max(vertices[:,0])
                    sizeX = maxX - minX
                    
                    minY = np.min(vertices[:,1])
                    maxY = np.max(vertices[:,1])
                    sizeY = maxY - minY
                    
                    minZ = np.min(vertices[:,2])
                    maxZ = np.max(vertices[:,2])
                    sizeZ = maxZ - minZ
                    
                    size = np.min((sizeX, sizeY, sizeZ))
                    
                    if size > MIN_VALUE:
                        down_pcd = pcd.voxel_down_sample(voxel_size = size/divider)
                        points = np.asarray(down_pcd.points).tolist()

                    else:
                        print('volume 0 mesh. get points by numpy unique')
                        points = np.unique(vertices, axis=0).tolist()

                    print('No. of points obtained:',len(points))

                    if cmds[0] == 'getPoints':
                        Points.clear()

                    Points += points

                else:
                    print('no mesh')

            elif cmds[0] == 'cam':

                if len(cmds) > 1:               
 
                    if cmds[1] == 'rotate':
    
                        curr_angle_step = angle_step
                            
                        if len(cmds) > 3:

                            fResult, value = Eval(cmds[3])

                            if fResult:
                                angle = value
                            else:
                                continue

                            curr_angle_step = angle_step
                            angle_step = np.deg2rad(angle)
    
                        if cmds[2] == 'x':
                           key_callback_1(vis, 1, 0)
    
                        elif cmds[2] == '-x':
                           key_callback_1(vis, 1, 1)
    
                        if cmds[2] == 'y':
                           key_callback_2(vis, 1, 0)
    
                        elif cmds[2] == '-y':
                           key_callback_2(vis, 1, 1)
    
                        if cmds[2] == 'z':
                           key_callback_3(vis, 1, 0)
    
                        elif cmds[2] == '-z':
                           key_callback_3(vis, 1, 1)
    
                        if len(cmds) > 3:
                           angle_step = curr_angle_step
    
                    elif cmds[1] == 'translate':
    
                        curr_translation_step = translation_step
                       
                        if len(cmds) > 3:

                            fresult, value = Eval(cmds[3])

                            if fResult:
                                translation_step = value
                            else:
                                continue
                       
                        if cmds[2] == 'x':
                           key_callback_4(vis, 1, 0)
    
                        elif cmds[2] == '-x':
                           key_callback_4(vis, 1, 1)
    
                        if cmds[2] == 'y':
                           key_callback_5(vis, 1, 0)
    
                        elif cmds[2] == '-y':
                           key_callback_5(vis, 1, 1)
    
                        if cmds[2] == 'z':
                           key_callback_6(vis, 1, 0)
    
                        elif cmds[2] == '-z':
                           key_callback_6(vis, 1, 1)
    
                        if len(cmds) > 3:
                            translation_step = curr_translation_step
    
                    elif cmds[1] == 'x':
                        key_callback_X(vis, -1, -1)
    
                    elif cmds[1] == 'y':
                        key_callback_Y(vis, -1, -1)
    
                    elif cmds[1] == 'z':
                        key_callback_Z(vis, -1, -1)
    
                else:
                    print('cam rotate x/y/z/-x/-y/-z [angle]')
                    print('cam translate x/y/z/-x/-y/-z [offset]')
                    print('cam x')
                    print('cam y')
                    print('cam z')
                    print()

            elif cmds[0] == 'calc':

                if len(cmds) > 1:

                    cmd = ''
                    for c in cmds[1:]:
                        cmd += '%s ' % c 

                    fResult, value = Eval(cmd)

                    if fResult:
                        print(value)
                else:
                    print('calc <expression>')
                    continue

            elif cmds[0] == 'draw':

                width = 800
                heigt = 600
                mode = 0
               
                if len(cmds) > 1:

                    if cmds[1].isdecimal():
                        width = int(cmds[1])

                    else:
                        print('draw [<width> <height> <mode>]')
                        continue

                if len(cmds) > 2:
              
                    if cmds[2].isdecimal():
                        height = int(cmds[2])

                    else:
                        print('draw [<width> <height> <mode>]')
                        continue

                if len(cmds) > 3:

                    if cmds[3].isdecimal():
                        mode = int(cmds[3])

                _points = getDrawingPoints(width, height, mode)
                   
                if _points is not None: 
                    Points = _points.tolist()

            elif cmds[0] == 'img2mesh':

                 if len(cmds) > 1 and os.path.exists(cmds[1]):
                     img2mesh = os.path.join(os.path.dirname(__file__), 'img2mesh.py')
                     cmd = 'python %s %s' % (img2mesh, cmds[1]) 
                     
                     subprocess.run(cmd, shell=True)

                     base = os.path.basename(cmds[1])
                     filename = os.path.splitext(base)[0]

                     LINES.append('l %s_contour.npy' % filename)
                     LINES.append('l %s_A.ply' % filename)
                     LINES.append('l %s_AA.ply' % filename)
                     LINES.append('POLYLINE')

                     print('Hit any key')

                 else:
                     print('img2mesh <image file> ... background color shall be black')

            elif cmds[0] == 'dir' or cmds[0] == 'copy' or cmds[0] == 'move' or cmds[0] == 'ren' or cmds[0] == 'del':

                cmd = ''
                for c in cmds:
                    cmd += '%s ' % c

                subprocess.run(cmd, shell=True)

            elif cmds[0] == 'quit':
                break
    
        except queue.Empty:
            pass
    
        if not vis.poll_events():
            break
        vis.update_renderer()
    
    vis.destroy_window()

if __name__ == '__main__':
    main()
