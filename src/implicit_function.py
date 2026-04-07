import open3d as o3d
import numpy as np
from skimage import measure
import sys

KEY_LEFT  = 263
KEY_RIGHT = 262
KEY_UP    = 265
KEY_DOWN  = 264

XMIN = -2
XMAX =  2
YMIN = -2
YMAX =  2
ZMIN = -2
ZMAX =  2

level = 0
dst_path = 'implicit_function.ply'
mesh = None

def key_callback_reset_level(vis, action, mod):

    global level

    level = 0
    print('level:',level)

    return True
    
def key_callback_UP_level(vis, action, mod):

    global level

    if action == 0: # on press
        level += 0.5
        print('level:',level)
    
    return True

def key_callback_up_level(vis, action, mod):

    global level

    if action == 0: # on press
        level += 0.05
        print('level:',level)
    
    return True

def key_callback_DOWN_level(vis, action, mod):

    global level

    if action == 0: # on press
        level -= 0.5
        print('level:',level)
    
    return True

def key_callback_down_level(vis, action, mod):

    global level

    if action == 0: # on press
        level -= 0.05
        print('level:',level)
    
    return True


def key_callback_set_save_flag(vis, action, mods):

    o3d.io.write_triangle_mesh(dst_path, mesh)
    print('save %s' % dst_path)
    
    vis.destroy_window()
    return False


def main():

    global level, mesh

    argv = sys.argv
    argc = len(argv)
    
    print('%s creates mesh from implicit function' % argv[0])
    print('[usage] python %s <implicit function>' % argv[0])
    print('        press up/down/0 to select level')
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
    #x, y, z = np.ogrid[-2:2:res*1j, -2:2:res*1j, -2:2:res*1j]
    x, y, z = np.ogrid[XMIN:XMAX:res*1j, YMIN:YMAX:res*1j, ZMIN:ZMAX:res*1j]
    
    vol = eval(expression)
    
    level = 0
    prevLevel = -1    

    # 可視化の設定
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    vis.register_key_action_callback(ord("0"), key_callback_reset_level)
    vis.register_key_action_callback(KEY_UP, key_callback_UP_level)
    vis.register_key_action_callback(KEY_RIGHT, key_callback_up_level)
    vis.register_key_action_callback(KEY_DOWN, key_callback_DOWN_level)
    vis.register_key_action_callback(KEY_LEFT, key_callback_down_level)
    vis.register_key_action_callback(ord("S"), key_callback_set_save_flag)

    ctrl = vis.get_view_control()

    color_front = np.array((128/255, 128/255, 255/255))
    color_back  = np.array((200/255, 200/255, 255/255))
    
    while True:

        if prevLevel != level:
 
            prevLevel = level

            _EyePos = ctrl.convert_to_pinhole_camera_parameters() 

            if mesh is not None:
                vis.remove_geometry(mesh)

            # マーチングキューブ法でメッシュ化
            verts, faces, normals, values = measure.marching_cubes(vol, level=level)
    
            colorsFront = np.tile(color_front, (verts.shape[0], 1))
            colorsBack  = np.tile(color_back, (verts.shape[0], 1))

            # Open3Dのメッシュ形式に変換
            meshFront = o3d.geometry.TriangleMesh()
            meshFront.vertices = o3d.utility.Vector3dVector(verts)
            meshFront.triangles = o3d.utility.Vector3iVector(faces)
            meshFront.vertex_colors = o3d.utility.Vector3dVector(colorsFront)

            meshBack = o3d.geometry.TriangleMesh()
            meshBack.vertices = o3d.utility.Vector3dVector(verts)
            meshBack.triangles = o3d.utility.Vector3iVector(faces[:,[0,2,1]])
            meshBack.vertex_colors = o3d.utility.Vector3dVector(colorsBack)

            mesh = meshFront + meshBack

            center = mesh.get_center()
            mesh.translate(-center)
            mesh.compute_vertex_normals()

            vis.add_geometry(mesh)

            ctrl.convert_from_pinhole_camera_parameters(_EyePos)

        if not vis.poll_events():
            break

        vis.update_renderer()

    vis.destroy_window()

if __name__ == '__main__':
    main()
