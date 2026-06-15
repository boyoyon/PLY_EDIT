import open3d as o3d
import numpy as np
import threading
import queue
import sys, os, copy

TAB = 258

KEY_UP    = 265
KEY_DOWN  = 264

KEY_LEFT  = 263
KEY_RIGHT = 262

STEP = 0.01
SCALE = 1.0

WEIGHT = None
RANGE = 10

input_queue = None

Points = None
curr = -1

Marker = None
LS = None

fUpdate = True
fAxis = True
axis = None

mesh = None

def set_weight():

    global WEIGHT

    WEIGHT = np.empty((RANGE), np.float32)

    angle_step = np.pi/RANGE

    for i in range(RANGE):
        WEIGHT[i] = np.cos(angle_step * i) + 1

    print(RANGE)
    print(WEIGHT.shape)

def key_callback_range_up(vis, action, mods):

    global RANGE

    if action == 0: # on press
        RANGE += 1

        set_weight()
        print('weight:', WEIGHT)

    return False

def key_callback_range_down(vis, action, mods):

    global RANGE

    if action == 0: # on press

        prev_range = RANGE

        RANGE -= 1

        if RANGE < 1:
            RANGE = 1

        if RANGE != prev_range:
            set_weight()

        print('weight:', WEIGHT)

    return False

def key_callback_step_up(vis, action, mods):

    global STEP

    if action == 0: # on press
        STEP += 0.01

    print('STEP:', STEP)

    return False

def key_callback_step_down(vis, action, mods):

    global STEP

    if action == 0: # on press
        STEP -= 0.01

        if STEP < 0.01:
            STEP = 0.01

    print('STEP:', STEP)

    return False

def key_callback_a(vis, action, mods):

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

def key_callback_prev(vis, action, mods):

    global curr, fUpdate

    if action == 0:

        if Points is not None:

            if mods == 1:
                curr -= 10

            else:
                curr -= 1 

            if curr < 0:
                curr = 0

            fUpdate = True

    return True

def key_callback_next(vis, action, mods):

    global curr, fUpdate

    if action == 0:

        if Points is not None:

            if mods == 1:
                curr += 10
            else:
                curr += 1

            if curr >= Points.shape[0]:
                curr = Points.shape[0] - 1

            fUpdate = True

    return True

def displayMarker(vis, marker, Points, flag):

    global Marker, LS

    ctrl = vis.get_view_control()
    _EyePos = ctrl.convert_to_pinhole_camera_parameters() 

    scaled = copy.deepcopy(marker)
    scaled.scale(SCALE, center=scaled.get_center())

    if Marker is not None:
        vis.remove_geometry(Marker)

    if LS is not None:
        vis.remove_geometry(LS)

    if mesh is not None:
        vis.remove_geometry(mesh)

    if flag and Points is not None:

        accum = None

        for i in range(Points.shape[0]):
            p = Points[i]
            _marker = copy.deepcopy(scaled)
            _marker.translate(np.array((p[0],p[1],p[2])))

            if i == curr:
                _marker.paint_uniform_color([1.0, 0.0, 0.0]) # 赤
            else:
                _marker.paint_uniform_color([1.0, 200/255, 64/255]) # オレンジ

            if i == 0:
                accum = copy.deepcopy(_marker)
            else:
                accum += copy.deepcopy(_marker)
                   
                ls = o3d.geometry.LineSet()
                ls.points = o3d.utility.Vector3dVector(Points)
                ls.lines = o3d.utility.Vector2iVector([[i-1,i]])     

                if i == 1:
                    LS = ls
                else:
                    LS += ls

        Marker = copy.deepcopy(accum)

        if Marker is not None:
            vis.add_geometry(Marker)
            if mesh is not None:
                vis.add_geometry(mesh)
            else:
                vis.add_geometry(LS)

    ctrl.convert_from_pinhole_camera_parameters(_EyePos)
    return True

def key_callback_z(vis, action, mods):

    global fUpdate

    if action == 0:

        step = STEP * -1
     
        if mods == 1:
        
            step = STEP

        for i in range(RANGE):

            if i == 0:
                Points[curr][2] += (step * WEIGHT[0])

            else:

                if curr + i < Points.shape[0]:
                    Points[curr+i][2] += (step * WEIGHT[i])

                if curr - i >= 0:
                    Points[curr-i][2] += (step * WEIGHT[i])

        fUpdate = True

    return True

def key_callback_scale_up(vis, action, mods):

    global SCALE, fUpdate

    if action == 0 and mods == 1:

        SCALE += 0.1
        fUpdate = True

    return True

def key_callback_scale_down(vis, action, mods):

    global SCALE, fUpdate

    if action == 0:

        SCALE -= 0.1
        fUpdate = True

    return True

def key_callback_dummy(vis, action, mods): # supress capture

    return True

def input_thread():

    while True:

        line = sys.stdin.readline().strip()
        if line:
            input_queue.put(line)

def main():

    global input_queue, Points, curr, fUpdate, axis, mesh

    width = 800
    height = 600
 
    input_queue = queue.Queue()
    threading.Thread(target=input_thread, daemon=True).start()
    
    # Visualizerウィンドウを開く
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window(window_name='knot edit', width=width, height=height)

    vis.register_key_action_callback(ord('A'), key_callback_a)
    vis.register_key_action_callback(ord('Z'), key_callback_z)
    vis.register_key_action_callback(ord('P'), key_callback_prev)
    vis.register_key_action_callback(ord('N'), key_callback_next)
    vis.register_key_action_callback(ord(';'), key_callback_scale_up)
    vis.register_key_action_callback(ord('-'), key_callback_scale_down)
    vis.register_key_action_callback(KEY_LEFT, key_callback_range_down)
    vis.register_key_action_callback(KEY_RIGHT, key_callback_range_up)
    vis.register_key_action_callback(KEY_DOWN, key_callback_step_down)
    vis.register_key_action_callback(KEY_UP, key_callback_step_up)

    axis = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'axisXYZ.ply'))
    Pmarker = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'Pmarker.ply'))
    #Pmarker.scale(3.0, center=Pmarker.get_center())

    ctrl = vis.get_view_control()

    vis.add_geometry(axis)
    ctrl.set_front([0.5, 0.25, 0.5])

    set_weight()
    mesh = None

    print('Hit ESC-key or q-key on visualizer or enter quit on console to terminate this program')
    
    mode = None

    while True:
   
        try:
            # キューからコマンドを取得
            cmds = input_queue.get_nowait().split(' ')
   
            if len(cmds) == 0 or len(cmds[0]) == 0:
                continue

            elif cmds[0] == 'l':
    
                if len(cmds) < 2:
                    print('l <.npy>')
                elif not os.path.exists(cmds[1]):
                    print('%s does not exist' % cmds[1])
                else:
                    ext = os.path.splitext(cmds[1])[1]
               
                    if ext == '.npy':

                        data = np.load(cmds[1])
                        order = len(data.shape)                        

                        if order == 2:
                            Points = data
                            mode = 'npy'
                            curr = 0

                        else:
                            print('unknown format or unexpected shape:', data.shape)
                            continue

                    elif ext == '.ply':

                        mesh = o3d.io.read_triangle_mesh(cmds[1])
                        Points = np.asarray(mesh.vertices)
                        curr = 0
                        mode = 'ply'                        

                    fUpdate = True

            elif cmds[0] == 'save':

                if Points is None:
                    print('Points is None')
                    continue

                if mesh is not None:

                    dst_path = 'knot.ply'

                    if len(cmds) > 1:
                        dst_path = cmds[1]

                    if not dst_path.endswith('.ply'):
                        print('save <.ply>')
                        continue

                    mesh.vertices = o3d.utility.Vector3dVector(Points)
                    o3d.io.write_triangle_mesh(dst_path, mesh)
                    print('save %s' % dst_path)

                else:

                    dst_path = 'knot.npy'

                    if len(cmds) > 1:
                        dst_path = cmds[1]

                    if not dst_path.endswith('.npy'):
                        print('save <.npy>')
                        continue

                    np.save(dst_path, Points)
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
   
        if fUpdate:
            fUpdate = False
            displayMarker(vis, Pmarker, Points, True)
 
    vis.destroy_window()

if __name__ == '__main__':
    main()
