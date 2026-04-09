import open3d as o3d
import numpy as np
from skimage import measure
import copy, os, sys

KEY_LEFT  = 263
KEY_RIGHT = 262
KEY_UP    = 265
KEY_DOWN  = 264

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

XMIN = -2
XMAX =  2
YMIN = -2
YMAX =  2
ZMIN = -2
ZMAX =  2

level = 0
step = 0.025
upper = 0.49
lower = -0.49

dst_path = 'implicit.ply'
dst_front_path = 'implicitA.ply'
dst_back_path = 'implicitAA.ply'

mesh = None
meshFront = None
meshBack = None

fAxis = True

fCapture = False

def key_callback_reset_level(vis, action, mod):

    global level

    level = 0
    print('level:', level)
    step = 0.025
    print('step:', step)

    return True
    
def key_callback_UP_level(vis, action, mod):

    global level

    if fCapture:

        if action == 0:
            level += step
            if level >= upper:
                level = upper
            print('level:',level)

    else:

        level += step
        if level >= upper:
            level = upper
        print('level:',level)
    
    return True

def key_callback_up_level(vis, action, mod):

    global level

    if fCapture:

        if action == 0:
            level += step * 0.2
            if level >= upper:
                level = upper
            print('level:',level)

    else:

        level += step * 0.2
        if level >= upper:
            level = upper
        print('level:',level)
    
    return True

def key_callback_DOWN_level(vis, action, mod):

    global level

    if fCapture:

        if action == 0:
            level -= step
            if level <= lower:
                level = lower
            print('level:',level)

    else:
        level -= step
        if level <= lower:
            level = lower
        print('level:',level)
    
    return True

def key_callback_down_level(vis, action, mod):

    global level

    if fCapture:
    
        if action == 0:
            level -= step * 0.2
            if level <= lower:
                level = lower
            print('level:',level)

    else:
        level -= step * 0.2
        if level <= lower:
            level = lower
        print('level:',level)
    
    return True

def key_callback_decrease_step(vis, action, mod):

    global step

    step *= 0.9
    print('step:', step)

    return True
    
def key_callback_increase_step(vis, action, mod):

    global step

    step *= 1.1
    print('step:', step)

    return True
    
def key_callback_toggle_axis_flag(vis, action, mods):

    global fAxis

    if action == 0:
        fAxis = not fAxis

def key_callback_toggle_capture_flag(vis, action, mods):

    global fCapture

    if action == 0:
        fCapture = not fCapture
        print('Capture flag: ', fCapture)

def key_callback_set_save_flag(vis, action, mods):

    o3d.io.write_triangle_mesh(dst_path, mesh)
    print('save %s' % dst_path)

    o3d.io.write_triangle_mesh(dst_front_path, meshFront)
    print('save %s' % dst_front_path)

    o3d.io.write_triangle_mesh(dst_back_path, meshBack)
    print('save %s' % dst_back_path)
       
    vis.destroy_window()
    return False


def main():

    global level, mesh, meshFront, meshBack

    argv = sys.argv
    argc = len(argv)
    
    print('%s creates mesh from implicit function' % argv[0])
    print('[usage] python %s <implicit function>' % argv[0])
    print('        press arrow-key to select level')
    print('        press 7/8-key to decrease/increase level step')
    print('        press 0-key to reset level and step')
    print('        press a-key to toggle axis display flag')
    print('        press c-key to toggle capture flag')
    print('        press s-key to save mesh and terminate')
    print('        press ESC/q-key to abort')
    print()
    
    if argc < 2:
        quit()
    
    expression = ''
    for i in range(1, argc):
        expression += '%s ' % argv[i]
   
    print(expression)

    # ボクセルの作成
    res = 50  # 解像度
    
    x, y, z = np.ogrid[XMIN:XMAX:res*1j, YMIN:YMAX:res*1j, ZMIN:ZMAX:res*1j]
    
    vol = eval(expression)

    vol_min = np.min(vol)
    vol_max = np.max(vol)
    
    vol -= vol_min
    vol /= vol_max - vol_min + 1e-6
    vol -= 0.5
  
    print('vol:', np.min(vol), np.max(vol))

    level = 0
    prevLevel = -1    

    # 可視化の設定
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window(window_name=expression, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    vis.register_key_action_callback(ord('0'), key_callback_reset_level)
    vis.register_key_action_callback(ord('7'), key_callback_decrease_step)
    vis.register_key_action_callback(ord('8'), key_callback_increase_step)
    vis.register_key_action_callback(KEY_UP, key_callback_UP_level)
    vis.register_key_action_callback(KEY_RIGHT, key_callback_up_level)
    vis.register_key_action_callback(KEY_DOWN, key_callback_DOWN_level)
    vis.register_key_action_callback(KEY_LEFT, key_callback_down_level)
    vis.register_key_action_callback(ord('A'), key_callback_toggle_axis_flag)
    vis.register_key_action_callback(ord('C'), key_callback_toggle_capture_flag)
    vis.register_key_action_callback(ord('S'), key_callback_set_save_flag)

    color_front = np.array((128/255, 128/255, 255/255))
    color_back  = np.array((200/255, 200/255, 255/255))
    
    axis = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'axisXYZ.ply'))
    
    vis.add_geometry(axis)

    ctrl = vis.get_view_control()
    ctrl.set_front([0.5, 0.25, 0.5])
    EyePos0 = ctrl.convert_to_pinhole_camera_parameters() 
   

    prevAxis = fAxis

    no = 1
 
    while True:

        if prevLevel != level:
 
            prevLevel = level

            _EyePos = ctrl.convert_to_pinhole_camera_parameters() 

            if mesh is not None:
                vis.remove_geometry(mesh)

            # マーチングキューブ法でメッシュ化
            verts, faces, normals, values = measure.marching_cubes(vol, level=level)

            verts *= 1/res

            colorsFront = np.tile(color_front, (verts.shape[0], 1))
            colorsBack  = np.tile(color_back, (verts.shape[0], 1))

            # Open3Dのメッシュ形式に変換
            meshFront = o3d.geometry.TriangleMesh()
            meshFront.vertices = o3d.utility.Vector3dVector(verts)
            meshFront.triangles = o3d.utility.Vector3iVector(faces)
            meshFront.vertex_colors = o3d.utility.Vector3dVector(colorsFront)

            center = meshFront.get_center()
            meshFront.translate(-center)

            meshBack = copy.deepcopy(meshFront)
            triangles = np.array(meshBack.triangles)
            meshBack.triangles = o3d.utility.Vector3iVector(triangles[:,[0,2,1]])
            meshBack.vertex_colors = o3d.utility.Vector3dVector(colorsBack)

            mesh = meshFront + meshBack
            mesh.compute_vertex_normals()

            vis.add_geometry(mesh)

            ctrl.convert_from_pinhole_camera_parameters(_EyePos)

            if fCapture:
                dst_path = '%04d.png' % no
                vis.capture_screen_image(dst_path)
                print('save %s' % dst_path)
                no += 1

        if prevAxis != fAxis:

            prevAxis = fAxis

            _EyePos = ctrl.convert_to_pinhole_camera_parameters() 

            if fAxis:
                vis.add_geometry(axis)
            else:
                vis.remove_geometry(axis)

            ctrl.convert_from_pinhole_camera_parameters(_EyePos)

        if not vis.poll_events():
            break

        vis.update_renderer()

    vis.destroy_window()

if __name__ == '__main__':
    main()
