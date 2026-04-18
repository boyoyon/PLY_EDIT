import open3d as o3d
import numpy as np
import threading
import queue
import copy, os, sys
from getValues import Eval, Evals
from polygon import get_rotation_to_vector
import manifold3d
from manifold3d import Manifold
from polygon import *

input_queue = None

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600   

KEY_LEFT  = 263
KEY_RIGHT = 262
KEY_UP    = 265
KEY_DOWN  = 264

LATITUDE = 45
LONGITUDE = -90
r = 1.5
scale = 0.2

feedLati = 0.0
feedLongi = 1.0

STEP = 5

target = None

drill = None
drill0 = None

fMark = False
markedR = None
markedLati = None
markedLongi = None
drillR = None
drillLati = None
drillLongi = None

fUpdate = True

undo_buffer = []

def manifold_to_mesh(mani):
    # 演算後のデータをOpen3D形式に戻す
    m = mani.to_mesh()

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(m.vert_properties)

    triangles = copy.deepcopy(m.tri_verts)
    #mesh.triangles = o3d.utility.Vector3iVector(m.tri_verts)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    return mesh

def mesh_to_manifold(o3d_mesh):
    # 頂点と面を抽出し、型を指定
    verts = np.asarray(o3d_mesh.vertices, dtype=np.float32)
    tri_indices = np.asarray(o3d_mesh.triangles, dtype=np.int32)
    
    # manifold3d.Mesh オブジェクトを作成
    mani_mesh = manifold3d.Mesh(
        vert_properties=verts,
        tri_verts=tri_indices
    )
    
    # MeshオブジェクトをManifoldコンストラクタに渡す
    return manifold3d.Manifold(mani_mesh)

def key_callback_drill(vis, action, mods):

    global drillR, drillLati, drillLongi

    if action == 0:
        drillR = r
        drillLati = LATITUDE
        drillLongi = LONGITUDE

        if drillR is not None and markedR is not None:
            Drill(vis)
        else:
            print('Press m-key at the point starting drill')

def Drill(vis):

    global r, LATITUDE, LONGITUDE, target

    diffR = drillR - markedR
    signR = 1
    if diffR < 0:
        signR = -1

    diffLati = drillLati - markedLati
    signLati = 1
    if diffLati < 0:
        signLati = -1

    diffLongi = drillLongi - markedLongi
    signLongi = 1
    if  diffLongi < 0:
        signLongi = -1

    count = int(signLongi * diffLongi) + 1
    stepLati = diffLati / count
    stepLongi = diffLongi / count  
    stepR = diffR / count  

    if signLati * diffLati > signLongi * diffLongi:
        count = int(signLati * diffLati) + 1
        stepLati = diffLati / count
        stepLongi = diffLongi / count 
        stepR = diffR / count        

    _r = markedR
    _LATITUDE = markedLati
    _LONGITUDE = markedLongi
    
    ctrl = vis.get_view_control()
    _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
    
    undo_buffer.append(target)
    vis.remove_geometry(target)

    result = copy.deepcopy(target)
    for i in range(count-1):
       print('processing %d/%d' % (i, count-2))

       _drill = copy.deepcopy(drill0)
       pos = getPos(_r, _LATITUDE, _LONGITUDE)
       R = get_rotation_to_vector(-np.array(pos), np.array((0,0,1)))
       _drill.rotate(R, center=(0,0,0)) 
       _drill.translate(pos)
                    
       mani_target = mesh_to_manifold(result)
       mani_drill = mesh_to_manifold(_drill)
    
       result_mani = mani_target - mani_drill
       result = manifold_to_mesh(result_mani)

       _r += stepR
       _LATITUDE += stepLati
       _LONGITUDE += stepLongi

    target = copy.deepcopy(result)
    target.compute_vertex_normals()

    vis.add_geometry(target)
    ctrl.convert_from_pinhole_camera_parameters(_EyePos)

def key_callback_minus(vis, action, mods):

    global target, LATITUDE, LONGITUDE

    ctrl = vis.get_view_control()
    _EyePos = ctrl.convert_to_pinhole_camera_parameters() 

    if action == 0:

        undo_buffer.append(target)
        vis.remove_geometry(target)

        mani_target = mesh_to_manifold(target)
        mani_drill = mesh_to_manifold(drill)

        result_mani = mani_target - mani_drill
        target = manifold_to_mesh(result_mani)
        target.compute_vertex_normals()
                    
        vis.add_geometry(target)
        ctrl.convert_from_pinhole_camera_parameters(_EyePos)

    else:

        if feedLati != 0.0 or feedLongi != 0.0:

            LATITUDE += feedLati
            LONGITUDE += feedLongi

            updateDrill(vis)

    return True

def key_callback_plus(vis, action, mods):

    global target, LATITUDE, LONGITUDE

    if action == 0:

        ctrl = vis.get_view_control()
        _EyePos = ctrl.convert_to_pinhole_camera_parameters() 

        undo_buffer.append(target)
        vis.remove_geometry(target)
        target += drill
        vis.add_geometry(target)
        
        ctrl.convert_from_pinhole_camera_parameters(_EyePos)

        if feedLati != 0.0 or feedLongi != 0.0:

            LATITUDE += feedLati
            LONGITUDE += feedLongi

            updateDrill(vis)

    return True

def getPos(r, latitude, longitude):

    Lati  = np.deg2rad(latitude)
    Longi = np.deg2rad(longitude)

    pos = np.array((0, r, 0)) # column vector
    R1 = np.eye(3)
    R1[1][1] = np.cos(Lati)
    R1[1][2] = -np.sin(Lati)
    R1[2][1] = np.sin(Lati)
    R1[2][2] = np.cos(Lati)

    pos = R1 @ pos
    
    R2 = np.eye(3)
    R2[0][0] = np.cos(Longi)
    R2[0][2] = -np.sin(Longi)
    R2[2][0] = np.sin(Longi)
    R2[2][2] = np.cos(Longi)
    pos = R2 @ pos

    return pos

def updateDrill(vis):

    global drill
 
    ctrl = vis.get_view_control()
    _EyePos = ctrl.convert_to_pinhole_camera_parameters()

    vis.remove_geometry(drill)

    pos = getPos(r, LATITUDE, LONGITUDE)

    drill = copy.deepcopy(drill0)
    R = get_rotation_to_vector(-np.array(pos), np.array((0,0,1)))
    drill.rotate(R, center=(0,0,0)) 
    drill.translate(pos)

    vis.add_geometry(drill)
    ctrl.convert_from_pinhole_camera_parameters(_EyePos)

def key_callback_lati_dec(vis, action, mods):

    global LATITUDE

    LATITUDE -= STEP

    updateDrill(vis)
 
    return True

def key_callback_lati_inc(vis, action, mods):

    global LATITUDE

    LATITUDE += STEP

    updateDrill(vis)
 
    return True

def key_callback_longi_dec(vis, action, mods):

    global LONGITUDE

    LONGITUDE -= STEP

    updateDrill(vis)
 
    return True

def key_callback_longi_inc(vis, action, mods):

    global LONGITUDE

    LONGITUDE += STEP

    updateDrill(vis)
 
    return True

def key_callback_forward(vis, action, mods):

    global r

    if action == 0: #on press
        prevR = r
        r -= 0.1
        if r < 0:
            r = 0

        if prevR != r:
            updateDrill(vis)

    return True

def key_callback_backward(vis, action, mods):

    global r

    prevR = r

    r += 0.1
    updateDrill(vis)

    return True

def key_callback_mark(vis, action, mods):

    global fUpdate, fMark, markedR, markedLati, markedLongi

    if action == 0: # push/release で元に戻らないように

        markedR = r
        markedLati = LATITUDE
        markedLongi = LONGITUDE
        fUpdate = True

    return True

def key_callback_undo(vis, action, mods):

    global target

    if action == 0:

        if len(undo_buffer) > 0:

            ctrl = vis.get_view_control()
            _EyePos = ctrl.convert_to_pinhole_camera_parameters()

            vis.remove_geometry(target)
            target = undo_buffer.pop()
            vis.add_geometry(target)

            ctrl.convert_from_pinhole_camera_parameters(_EyePos)

        else:
            print('undo buffer is empty')

def key_callback_dummy(vis, action, mods): # supress capture

    return True

def input_thread():

    while True:

        line = sys.stdin.readline().strip()
        if line:
            input_queue.put(line)
def main():

    global input_queue, target, drill, drill0, feedLati, feedLongi, fUpdate

    argv = sys.argv
    base = os.path.basename(argv[0])
    window_name = os.path.splitext(base)[0]

    width = 800
    height = 600
    
    drillColorNormal = ((255/255, 200/255, 128/255))
    drillColorMark   = ((255/255, 128/255,  64/255))
 
    input_queue = queue.Queue()
    threading.Thread(target=input_thread, daemon=True).start()
    
    # Visualizerウィンドウを開く
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window(window_name=window_name, width=width, height=height)

    vis.register_key_action_callback(KEY_UP, key_callback_lati_dec)
    vis.register_key_action_callback(KEY_DOWN, key_callback_lati_inc)
    vis.register_key_action_callback(KEY_LEFT, key_callback_longi_inc)
    vis.register_key_action_callback(KEY_RIGHT, key_callback_longi_dec)
    vis.register_key_action_callback(ord('F'), key_callback_forward)
    vis.register_key_action_callback(ord('B'), key_callback_backward)
    vis.register_key_action_callback(ord('-'), key_callback_minus)
    vis.register_key_action_callback(ord('+'), key_callback_plus)
    vis.register_key_action_callback(ord('M'), key_callback_mark)
    vis.register_key_action_callback(ord('D'), key_callback_drill)
    vis.register_key_action_callback(ord('P'), key_callback_plus)
    vis.register_key_action_callback(ord('U'), key_callback_undo)

    axis = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'axisXYZ.ply'))
    vis.add_geometry(axis)

    target0 = o3d.geometry.TriangleMesh.create_cylinder(1.0, 1.0, 30)
    R = o3d.geometry.get_rotation_matrix_from_xyz((np.pi/2, 0, 0))
    target0.rotate(R, center=(0,0,0))
    target0.translate(-target0.get_center())
    target0.compute_vertex_normals()

    target = copy.deepcopy(target0)
    
    drill0 = o3d.geometry.TriangleMesh.create_cone(radius=1.0, height=2.0)
    drill0.scale(scale, center=drill0.get_center())
    drill0.paint_uniform_color(drillColorNormal)
    drill0.compute_vertex_normals()

    drill = copy.deepcopy(drill0)

    drill_name = 'cone'

    pos = getPos(r, LATITUDE, LONGITUDE)
    R = get_rotation_to_vector(-np.array(pos), np.array((0,0,1)))
    drill.rotate(R, center=(0,0,0)) 
    drill.translate(pos)

    ctrl = vis.get_view_control()

    vis.add_geometry(target)
    vis.add_geometry(drill)
    ctrl.set_front([0.5, 0.25, 0.5])
  
    undo_mesh = []

    prevLatitude = -1.0
    prevLongitude = -1.0
    prevScale = 1.0
    prevR = 1.0

    print('Hit ESC-key or q-key on visualizer or enter quit on console to terminate this program')

 
    while True:
   
        try:
            # キューからコマンドを取得
            cmds = input_queue.get_nowait().split(' ')
   
            if len(cmds) == 0 or len(cmds[0]) == 0:
                continue

            elif cmds[0] == 'cylinder':

                if len(cmds) > 2:

                    fResult, value = Eval(cmds[1])
                    if fResult:
                        radius = value

                    else:
                        print('cylinder <radius> <height> [<resolution>]')
                        continue

                    fResult, value = Eval(cmds[2])
                    if fResult:
                        height = value
                    else:
                        print('cylinder <radius> <height> [<resolution>]')
                        continue

                    resolution = 30
                    if len(cmds) > 3:
                        fResult, value = Eval(cmds[3])
                        if fResult:
                            resolution
                        else:
                            print('cylinder <radius> <height> [<resolution>]')
                            continue

                    _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                    vis.remove_geometry(target)

                    target = o3d.geometry.TriangleMesh.create_cylinder(
                        radius, height, resolution)
                  
                    R = o3d.geometry.get_rotation_matrix_from_xyz((np.pi/2, 0, 0))
                    target.rotate(R, center=(0,0,0))
 
                    undo_meshes.append(target)
                    
                    vis.add_geometry(target)
                    ctrl.convert_from_pinhole_camera_parameters(_EyePos)

                else:
                    print('cylinder <radius> <height> [<resolution>]')

            elif cmds[0] == 'u':
    
                if len(undo_mesh) > 0:
                
                    _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
   
                    vis.remove_geometry(target)
                    target = undo_mesh.pop()
                    vis.add_geometry(target)

                    ctrl.convert_from_pinhole_camera_parameters(_EyePos)
    
                else:
                    print('undo buffer is empty')
    
            elif cmds[0] == 'save':

                if target is not None:

                    dst_path = 'target.ply'
   
                    if len(cmds) > 1:
                        if not cmds[1].endwith('.ply'):
                            print('save ***.ply')
                            continue

                        dst_path = cmds[2]

                    o3d.io.write_triangle_mesh(dst_path, target)
                    print('save %s' % dst_path)

                else:
                    print('no meshes to be saved')
  
            elif cmds[0] == 'feed':

                if len(cmds) > 2:
                    fResult, values = Evals(cmds[1:], 2)

                    if fResult:
                        feedLati  = values[0]
                        feedLongi = values[1]
                        print('feed %.2f %.2f' % (values[0], values[1]))

                    else:
                        print('feed  latitude  longitude')
                else:
                    print('feed  latitude  longitude')

            elif cmds[0] == 'drill':
     
                if len(cmds) == 1:
                    print('dirll cone/cylinder/ball/box')
                    print('drill:', drill_name)

                else:
                    if cmds[1] == 'cone':
                        drill0 = o3d.geometry.TriangleMesh.create_cone(radius=1.0, height=2.0)
                        drill0.scale(scale, center=drill0.get_center())
                        drill0.paint_uniform_color(drillColorNormal)
                        drill0.compute_vertex_normals()
                        drill_name = 'cone'

                    elif cmds[1] == 'cylinder':
                        drill0 = o3d.geometry.TriangleMesh.create_cylinder(radius=1.0, height=2.0)
                        drill0.scale(scale, center=drill0.get_center())
                        drill0.paint_uniform_color(drillColorNormal)
                        drill0.compute_vertex_normals()
                        drill_name = 'cylinder'


                    elif cmds[1] == 'ball':
                        drill0 = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)
                        drill0.scale(scale, center=drill0.get_center())
                        drill0.paint_uniform_color(drillColorNormal)
                        drill0.compute_vertex_normals()
                        drill_name = 'ball'

                    elif cmds[1] == 'box':
                        drill0 = o3d.geometry.TriangleMesh.create_box(width=1.0, height=2.0, depth=1.0)
                        drill0.scale(scale, center=drill0.get_center())
                        drill0.paint_uniform_color(drillColorNormal)
                        drill0.compute_vertex_normals()
                        drill_name = 'box'
                    else:
                        print('dirll cone/cylinder/ball/box')
                        print('drill:', drill_name)
                        continue

                    _EyePos = ctrl.convert_to_pinhole_camera_parameters() 
                    vis.remove_geometry(drill)
                    ctrl.convert_from_pinhole_camera_parameters(_EyePos)
                    drill = copy.deepcopy(drill0)
                    updateDrill(vis)                   
 
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
