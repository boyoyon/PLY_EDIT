import numpy as np
import open3d as o3d
import threading
import queue
import copy, os, sys

input_queue = None

KEY_LEFT  = 263
KEY_RIGHT = 262
KEY_UP    = 265
KEY_DOWN  = 264

angle_step = np.pi / 180
translation_step = 0.005
scale_up = 1.05
scale_down = 0.95

pcd = None
axis = None
plane_x0 = None
plane_y0 = None
plane_z0 = None

fAxis = False
fPlaneX0 = False
fPlaneY0 = False
fPlaneZ0 = False

def key_callback_dummy(vis, action, mods):

    return False

def key_callback_axis(vis, action, mods):

    global fAxis

    if action == 0:
        fAxis = not fAxis

        ctrl = vis.get_view_control()
        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
    
        if fAxis:
            vis.add_geometry(axis)
        else:
            vis.remove_geometry(axis)

        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
 
    return True

def key_callback_plane_x0(vis, action, mods):

    global fPlaneX0

    if action == 0:
        fPlaneX0 = not fPlaneX0

        ctrl = vis.get_view_control()
        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
    
        if fPlaneX0:
            vis.add_geometry(plane_x0)
        else:
            vis.remove_geometry(plane_x0)

        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
    
    return True

def key_callback_plane_y0(vis, action, mods):

    global fPlaneY0

    if action == 0:
        fPlaneY0 = not fPlaneY0

        ctrl = vis.get_view_control()
        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
    
        if fPlaneY0:
            vis.add_geometry(plane_y0)
        else:
            vis.remove_geometry(plane_y0)

        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
    
    return True

def key_callback_plane_z0(vis, action, mods):

    global fPlaneZ0

    if action == 0:
        fPlaneZ0 = not fPlaneZ0

        ctrl = vis.get_view_control()
        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
    
        if fPlaneZ0:
            vis.add_geometry(plane_z0)
        else:
            vis.remove_geometry(plane_z0)

        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
    
    return True

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

    print(angle_step, translation_step)

    return True

def key_callback_updown_translation_step(vis, action, mods):

    global angle_step, translation_step

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

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

    print(angle_step, translation_step)

    return True

def key_callback_1(vis, action, mods):

    if pcd is None:
        return False

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

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

    transform = rotation #@ transform
    pcd.transform(transform)

    return True

def key_callback_2(vis, action, mods):

    if pcd is None:
        return False

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

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

    transform = rotation #@ transform
    pcd.transform(transform)

    return True

def key_callback_3(vis, action, mods):

    if pcd is None:
        return False

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

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

    transform = rotation #@ transform
    pcd.transform(transform)

    return True

def key_callback_4(vis, action, mods):

    if pcd is None:
        return False

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

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

    transform = translate
    pcd.transform(transform)

    return True

def key_callback_5(vis, action, mods):

    if pcd is None:
        return False

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

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

    transform = translate
    pcd.transform(transform)

    return True

def key_callback_6(vis, action, mods):

    if pcd is None:
        return False

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

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

    transform = translate
    pcd.transform(transform)

    return True

def key_callback_reset_step(vis, action, mod):

    global angle_step, translation_step, scale

    angle_step = np.pi / 180
    translation_step = 0.005
    scale_up = 1.3
    scale_down = 0.7

    return True
    
def key_callback_scale_up(vis, action, mod):

    if pcd is None:
        return False

    if action == 1: # on pressing

        scale = np.array([
            [scale_up, 0,        0,        0],
            [0,        scale_up, 0,        0],
            [0,        0,        scale_up, 0],
            [0,        0,        0,        1]])

        transform = scale
        pcd.transform(transform)

        center = pcd.get_center()
        pcd.translate(-center)
    
    return True


def key_callback_scale_down(vis, action, mod):

    if pcd is None:
        return False

    if action == 1: # on pressing

        scale = np.array([
            [scale_down, 0,          0,          0],
            [0,          scale_down, 0,          0],
            [0,          0,          scale_down, 0],
            [0,          0,          0,          1]])

        transform = scale
        pcd.transform(transform)

        center = pcd.get_center()
        pcd.translate(-center)
    
    return True

def input_thread():

    while True:

        line = sys.stdin.readline().strip()
        if line:
            input_queue.put(line)

def main():

    global input_queue, pcd, axis, plane_x0, plane_y0, plane_z0, fAxis

    width = 800
    height = 600
 
    input_queue = queue.Queue()
    threading.Thread(target=input_thread, daemon=True).start()
    
    # Visualizerウィンドウを開く
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='point cloud editor', width=width, height=height)

    # 可視化の設定
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window(window_name='point cloud editor', width=width, height=height)

    vis.register_key_action_callback(ord("0"), key_callback_reset_step)
    vis.register_key_action_callback(ord("1"), key_callback_1)
    vis.register_key_action_callback(ord("2"), key_callback_2)
    vis.register_key_action_callback(ord("3"), key_callback_3)
    vis.register_key_action_callback(ord("4"), key_callback_4)
    vis.register_key_action_callback(ord("5"), key_callback_5)
    vis.register_key_action_callback(ord("6"), key_callback_6)
    vis.register_key_action_callback(ord("7"), key_callback_updown_angle_step)
    vis.register_key_action_callback(ord("8"), key_callback_updown_translation_step)
    vis.register_key_action_callback(KEY_UP, key_callback_scale_up)
    vis.register_key_action_callback(KEY_DOWN, key_callback_scale_down)
    vis.register_key_action_callback(ord("A"), key_callback_axis)
    vis.register_key_action_callback(ord("X"), key_callback_plane_x0)
    vis.register_key_action_callback(ord("Y"), key_callback_plane_y0)
    vis.register_key_action_callback(ord("Z"), key_callback_plane_z0)
    vis.register_key_action_callback(ord("D"), key_callback_dummy) # supress depth capture
    vis.register_key_action_callback(ord("P"), key_callback_dummy) # supress screen capture
    vis.register_key_action_callback(ord("Q"), key_callback_dummy) # supress quit

    axis = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'axisXYZ.ply'))
    plane_x0 = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'plane_x0.ply'))
    plane_y0 = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'plane_y0.ply'))
    plane_z0 = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'plane_z0.ply'))
    vis.add_geometry(axis)
    fAxis = True

    ctrl = vis.get_view_control()
    ctrl.set_front([0.5, 0.25, 0.5])

    print('Hit ESC-key or q-key on visualizer or enter quit on console to terminate this program')

    PCDS = []
    UNDO = None

    curr = -1
 
    while True:
   
        try:
            # キューからコマンドを取得
            cmds = input_queue.get_nowait().split(' ')
   
            if len(cmds) == 0 or len(cmds[0]) == 0:
                continue

            elif cmds[0] == 'axis':

                if len(cmds) > 1:
                    if cmds[1] == 'on':
                        if not fAxis:
                            _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                            vis.add_geometry(axis)
                            ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        fAxis = True

                    elif cmds[1] == 'off':
                        if fAxis:
                            _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                            vis.remove_geometry(axis)
                            ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        fAxis = False

                    else:
                        print('axis on/off')

                else:
                    fAxis = not fAxis
                    if fAxis:
                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.add_geometry(axis)
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                    else:
                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(axis)          
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)

            elif cmds[0] == 'l':
                if len(cmds) > 1 and os.path.exists(cmds[1]):
                    pcd = o3d.io.read_point_cloud(cmds[1])
                    PCDS.append(pcd)
                    curr = len(PCDS) - 1
                    _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                    vis.add_geometry(pcd)
                    ctrl.convert_from_pinhole_camera_parameters(_EyePos)

                else:
                    print('l <point cloud (.ply)>')

            elif cmds[0] == 'remove':
            
                if len(cmds) > 1:

                    UNDO = copy.deepcopy(PCDS)
                    _pcd = PCDS.pop(curr)
                    _points = np.asarray(_pcd.points)
                    _colors = np.asarray(_pcd.colors)

                    if cmds[1] == 'x':
                        indices = _points[:,0] < 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        PCDS.append(_pcd)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('removed')

                    elif cmds[1] == 'y':
                        indices = _points[:,1] < 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        PCDS.append(_pcd)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('removed')

                    elif cmds[1] == 'z':
                        indices = _points[:,2] < 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        PCDS.append(_pcd)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('removed')


                    elif cmds[1] == '-x':
                        indices = _points[:,0] > 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        PCDS.append(_pcd)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('removed')


                    elif cmds[1] == '-y':
                        indices = _points[:,1] > 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        PCDS.append(_pcd)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('removed')


                    elif cmds[1] == '-z':
                        indices = _points[:,2] > 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        PCDS.append(_pcd)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('removed')

                    else:
                        print('remove x/y/z/-x/-y/-z')

                else:
                    print('remove x/y/z/-x/-y/-z')

            elif cmds[0] == 'mirror':
            
                if len(cmds) > 1:

                    UNDO = copy.deepcopy(PCDS)
                    _pcd = PCDS.pop(curr)
                    _points = np.asarray(_pcd.points)
                    _colors = np.asarray(_pcd.colors)

                    if cmds[1] == 'x':
                        indices = _points[:,0] > 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        mirrored = copy.deepcopy(filtered_points)
                        mirrored[:,0] *= -1
                        _pcd2 = copy.deepcopy(_pcd)
                        _pcd2.points = o3d.utility.Vector3dVector(mirrored)
                        PCDS.append(_pcd + _pcd2)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('mirrored')

                    elif cmds[1] == 'y':
                        indices = _points[:,1] > 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        mirrored = copy.deepcopy(filtered_points)
                        mirrored[:,1] *= -1
                        _pcd2 = copy.deepcopy(_pcd)
                        _pcd2.points = o3d.utility.Vector3dVector(mirrored)
                        PCDS.append(_pcd + _pcd2)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('mirrored')

                    elif cmds[1] == 'z':
                        indices = _points[:,2] > 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        mirrored = copy.deepcopy(filtered_points)
                        mirrored[:,2] *= -1
                        _pcd2 = copy.deepcopy(_pcd)
                        _pcd2.points = o3d.utility.Vector3dVector(mirrored)
                        PCDS.append(_pcd + _pcd2)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('mirrored')

                    elif cmds[1] == '-x':
                        indices = _points[:,0] < 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        mirrored = copy.deepcopy(filtered_points)
                        mirrored[:,0] *= -1
                        _pcd2 = copy.deepcopy(_pcd)
                        _pcd2.points = o3d.utility.Vector3dVector(mirrored)
                        PCDS.append(_pcd + _pcd2)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('mirrored')

                    elif cmds[1] == '-y':
                        indices = _points[:,1] < 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        mirrored = copy.deepcopy(filtered_points)
                        mirrored[:,1] *= -1
                        _pcd2 = copy.deepcopy(_pcd)
                        _pcd2.points = o3d.utility.Vector3dVector(mirrored)
                        PCDS.append(_pcd + _pcd2)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('mirrored')

                    elif cmds[1] == '-z':
                        indices = _points[:,2] < 0
                        filtered_points = _points[indices]
                        filtered_colors = _colors[indices]
                        
                        _pcd.points = o3d.utility.Vector3dVector(filtered_points)
                        _pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

                        mirrored = copy.deepcopy(filtered_points)
                        mirrored[:,2] *= -1
                        _pcd2 = copy.deepcopy(_pcd)
                        _pcd2.points = o3d.utility.Vector3dVector(mirrored)
                        PCDS.append(_pcd + _pcd2)
                        curr = len(PCDS) - 1
                        pcd = PCDS[curr]

                        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                        vis.remove_geometry(_pcd)
                        vis.add_geometry(PCDS[curr])
                        ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                        print('mirrored')

                    else:
                        print('mirror x/y/z/-x/-y/-z')

                else:
                    print('mirror x/y/z/-x/-y/-z')

            elif cmds[0] == 'select':

                if len(cmds) > 1:
                    _idx = int(cmds[1])
                    if _idx >=0 and _idx < len(PCDS):
                        curr = _idx
                        pcd = PCDS[curr]

                    else:
                        print('select 0 - %d' % len(PCDS)-1)

                else:
                    print(PCDS)

            elif cmds[0] == 'save':

                if len(PCDS) == 0:
                    print('no point cloud')
                    continue

                if len(cmds) > 1:
                    _pcd = None
                    for i, p in enumerate(PCDS):
                        if i == 0:
                            _pcd = p
                        else:
                            _pcd += p
                    o3d.io.write_point_cloud(cmds[1], _pcd)
                    print('save %s' % cmds[1])

                else:
                    print('save <.ply>')
            
            elif cmds[0] == 'd':

                if len(PCDS) > 0:
                    _pcd = PCDS.pop(curr)
                    curr = len(PCDS) - 1
                    if curr < 0:
                        pcd = None
                    else:
                        pcd = PCDS[curr]
                    
                    _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                    vis.remove_geometry(_pcd)
                    ctrl.convert_from_pinhole_camera_parameters(_EyePos)

                else:
                    print('no point clound')

            elif cmds[0] == 'u':

                if UNDO is not None:

                    _EyePos = ctrl.convert_to_pinhole_camera_parameters() 

                    for i in range(len(PCDS)):
                        _pcd = PCDS.pop()
                        vis.remove_geometry(_pcd)
                    
                    for i in range(len(UNDO)):
                        _pcd = UNDO.pop()
                        vis.add_geometry(_pcd)
                        PCDS.append(_pcd)

                    UNDO = None
                    
                    ctrl.convert_from_pinhole_camera_parameters(_EyePos)

                else:
                    print('undo buffer is empty')

            elif cmds[0] == 'cap':

                no = 1
                dst_path = '%04d.png' % no
                while os.path.exists(dst_path):
                    no += 1
                    dst_path = '%04d.png' % no

                vis.capture_screen_image(dst_path)
                print('save %s' % dst_path)

            elif cmds[0] == 'quit':
                break
   
            else:
                print('unknow command')
                print()
 
        except queue.Empty:
            pass
    
        if not vis.poll_events():
            break
        vis.update_renderer()
    
    vis.destroy_window()

if __name__ == '__main__':
    main()
