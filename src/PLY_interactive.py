import open3d as o3d
import numpy as np
import threading
import queue
import copy, os, sys
from polygon import polygon

def input_thread():
    while True:
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

def show_menu():

    print('コマンドを入力してください')
    print('show menu            : m[enu]')
    print('load ply             : l[oad] <ply>')
    print('delete selected ply  : d[el]')
    print('set rotate matrix:   : r <angle_x(degree) <angle_y(degree)> <angle_z(degree)>')
    print('set scale matirx:    : s <scale_x> <scale_y> <scale_z>')
    print('set translate matrix : t <offset_x> <offset_y> <offset_z>')
    print('paint with color     : c <r(0-255)> <g(0-255) <b(0-255)>')
    print('undo                 : u')
    print('on/off selected mesh : selected')
    print('on/off axis          : a[xis]')
    print('save ply             : save <ply filename>')
    print('terminate program    : q[uit]') 
    print()

def getFloat3(str0, str1, str2):

    fResult = True
    values = []

    try:
        values.append(float(eval(str0)))
    except NameError:
        print('NameError: %s' % str0)
        fResult = False
    else:

        try:
            values.append(float(eval(str1)))
        except NameError:
            print('NameError: %s' % str1)
            fResult = False
        else:
    
            try:
                values.append(float(eval(str2)))
            except NameError:
                print('NameError: %s' % str2)
                fResult = False

    return fResult, values
                        
argv = sys.argv
argc = len(argv)

print('%s rotates, scales and translates PLY' % argv[0])

meshes = []
meshes_gray = []
names = []
mesh = None
curr = 0
names.append('')
fSelectedOnly = False
fAxis = True

undo_mesh = []
undo_idx = []

input_queue = queue.Queue()

threading.Thread(target=input_thread, daemon=True).start()

# 可視化の準備
vis = o3d.visualization.Visualizer()
vis.create_window(window_name='PLY Edit interactivelly', width=800, height=600)

axis = o3d.io.read_triangle_mesh(os.path.join(os.path.dirname(__file__), 'axisXYZ.ply'))
meshes.append(axis)
meshes_gray.append(axis)

vis.add_geometry(axis)

ctrl = vis.get_view_control()
ctrl.set_front([0.5, 0.25, 0.5])

show_menu()

while True:
    try:
        # キューからコマンドを取得
        cmds = input_queue.get_nowait().split(' ')
        
        if cmds[0][0] == 'm':

            show_menu()

        elif cmds[0][0] == 'l':

            if len(cmds) < 2:
                print('ply file is not specified. skip...')
            elif not os.path.exists(cmds[1]) or not '.ply' in cmds[1]:
                print('%s does not exist or not ply. skip...' % cmds[1])
            else:
                mesh = o3d.io.read_triangle_mesh(cmds[1])           
 
                vis.add_geometry(mesh)
                ctrl.set_front([0.5, 0.25, 0.5])

                meshes.append(mesh)
                names.append(cmds[1])
                curr = len(meshes) - 1
                mesh_gray = copy.deepcopy(mesh)
                mesh_gray.paint_uniform_color([0.9,0.9,0.9])
                meshes_gray.append(mesh_gray)

                vis.update_geometry(mesh)

        elif cmds[0] == 'axis':

            if fAxis:
                vis.remove_geometry(axis)
            else:
                vis.add_geometry(axis)
                
            ctrl.set_front([0.5, 0.5, 0.5])

            fAxis = not fAxis

        elif cmds[0] == 'c':

            if len(cmds) != 4:
                print('specify red(0-255) green(0-255) blue(0-255)')
            else:
                red = int(cmds[1]) / 255
                green = int(cmds[2]) / 255
                blue = int(cmds[3]) / 255

                undo_idx.append(curr)
                undo_mesh.append(copy.deepcopy(meshes[curr]))

                meshes[curr].paint_uniform_color([red, green, blue])
                vis.update_geometry(meshes[curr])

        elif cmds[0] == 'selected':

            print(names[curr])

            vis.clear_geometries()
          
            start = 0
            if not fAxis:
                start = 1
 
            for i in range(start, len(meshes)):
            
                if i == curr:
                    vis.add_geometry(meshes[i])
                        
                else:
                    if fSelectedOnly:
                        vis.add_geometry(meshes[i])
                    else:
                        vis.add_geometry(meshes_gray[i])

            ctrl.set_front([0.5, 0.25, 0.5])

            fSelectedOnly = not fSelectedOnly

        elif cmds[0] == 'select':

            try:
                idx = names.index(cmds[1])
            except ValueError:
                print('select from ', names)

            except IndexError:
                print('select from ', names)
            else:
                curr = idx

        elif cmds[0][0] == 'd':

            if len(meshes) > 1:
                vis.remove_geometry(meshes[curr])
             
                meshes.pop(curr)
                curr = len(meshes) - 1
                names.pop(curr)

                try:
                    idx = undo_idx.index(curr)
                except ValueError:
                    pass
                else:
                    undo_idx.pop(idx)
                    undo_mesh.pop(idx)

                ctrl.set_front([0.5, 0.25, 0.5])
            
            else:
                print('unable to delete')

        elif cmds[0] == 'r':

            if len(cmds) < 4:
                print('specify angle_x(degree) angle_y(degree) angle_z(degree) [<count(>=2)>]')
                print('current Rmatrix:', R)

            else:

                fResult, values = getFloat3(cmds[1], cmds[2], cmds[3])

                if fResult:

                    rad_x = np.deg2rad(values[0])
                    rad_y = np.deg2rad(values[1])
                    rad_z = np.deg2rad(values[2])

                    R = o3d.geometry.get_rotation_matrix_from_xyz((rad_x, rad_y, rad_z))
                    count = 0

                    if len(cmds) > 4:
                        count = int(cmds[4])

                    undo_idx.append(curr)
                    undo_mesh.append(copy.deepcopy(meshes[curr]))

                    if count < 2:
                        meshes[curr].rotate(R, center=(0,0,0))
                        vis.update_geometry(meshes[curr])

                    else:
                        for i in range(count):
                            meshes[curr].rotate(R, center=(0,0,0))
                        
                            if i == 0:
                                accum = copy.deepcopy(meshes[curr])
                            else:
                                accum += copy.deepcopy(meshes[curr])
                    
                        meshes[curr] = copy.deepcopy(accum)
                        accum.paint_uniform_color([0.9,0.9,0.9])
                        meshes_gray[curr] = copy.deepcopy(accum)

                        refresh(vis, meshes, fAxis)
                        ctrl.set_front([0.5, 0.25, 0.5])
 
        elif cmds[0] == 's':

            if len(cmds) < 4:
                print('specify scalee_x scale_y scale_z [<count(>=2)>]')
                print('current Smatrix: ', S)

            else:

                fResult, values = getFloat3(cmds[1], cmds[2], cmds[3])

                if fResult:

                    S = np.array([[values[0],  0,          0,         0],
                                  [ 0,         values[1],  0,         0],
                                  [ 0,         0,          values[2], 0],
                                  [ 0,         0,          0,         1]])

                    count = 0
    
                    if len(cmds) > 4:
                        count = int(cmds[4])
    
                    undo_idx.append(curr)
                    undo_mesh.append(copy.deepcopy(meshes[curr]))
    
                    if count < 2:
                        meshes[curr].transform(S)
                        vis.update_geometry(meshes[curr])
    
                    else:
                        for i in range(count):
                            meshes[curr].transform(S)
                            
                            if i == 0:
                                accum = copy.deepcopy(meshes[curr])
                            else:
                                accum += copy.deepcopy(meshes[curr])
                        
                        meshes[curr] = copy.deepcopy(accum)
                        accum.paint_uniform_color([0.9,0.9,0.9])
                        meshes_gray[curr] = copy.deepcopy(accum)
    
                        refresh(vis, meshes, fAxis)
                        ctrl.set_front([0.5, 0.25, 0.5])

        elif cmds[0] == 't':

            if len(cmds) < 4:
                print('specify offset_x offset_y offset_z [<count(>=2)>]')
                print('current Tmatrix: ', T)

            else:

                fResult, values = getFloat3(cmds[1], cmds[2], cmds[3])

                if fResult:

                    T = np.array([[ 1,  0,  0, values[0]],
                                  [ 0,  1,  0, values[1]],
                                  [ 0,  0,  1, values[2]],
                                  [ 0,  0,  0, 1]])
    
    
                    count = 0
    
                    if len(cmds) > 4:
                        count = int(cmds[4])
    
                    undo_idx.append(curr)
                    undo_mesh.append(copy.deepcopy(meshes[curr]))
    
                    if count < 2:
                        meshes[curr].transform(T)
                        vis.update_geometry(meshes[curr])
    
                    else:
                        for i in range(count):
                            meshes[curr].transform(T)
                            
                            if i == 0:
                                accum = copy.deepcopy(meshes[curr])
                            else:
                                accum += copy.deepcopy(meshes[curr])
                        
                        meshes[curr] = copy.deepcopy(accum)
                        accum.paint_uniform_color([0.9,0.9,0.9])
                        meshes_gray[curr] = copy.deepcopy(accum)
    
                        refresh(vis, meshes, fAxis)
                        ctrl.set_front([0.5, 0.25, 0.5])

        elif cmds[0] == 'g':

            if len(cmds) < 5:
                print('specify group operation (ex. t xx xx xx r xx xx xx) [<count(>=2)>]')

            else:
                G = np.eye(4)

                idx = 1
                fResult = True

                while len(cmds) - idx > 3:

                    fResult, values = getFloat3(cmds[idx+1], cmds[idx+2], cmds[idx+3])

                    if not fResult:
                        break;

                    if cmds[idx] == 'r' or cmds[idx] == 'R':

                        rad_x = np.deg2rad(values[0])
                        rad_y = np.deg2rad(values[1])
                        rad_z = np.deg2rad(values[2])

                        r = o3d.geometry.get_rotation_matrix_from_xyz((rad_x, rad_y, rad_z))
                        
                        R = np.eye(4)
                        R[:3,:3] = r

                        G = G @ R

                    elif cmds[idx] == 's' or cmds[idx] == 'S':

                        S = np.array([[values[0],  0,          0,         0],
                                      [ 0,         values[1],  0,         0],
                                      [ 0,         0,          values[2], 0],
                                      [ 0,         0,          0,         1]])

                        G = G @ S

                    elif cmds[idx] == 't' or cmds[idx] == 'T':
 
                        T = np.array([[ 1,  0,  0, values[0]],
                                      [ 0,  1,  0, values[1]],
                                      [ 0,  0,  1, values[2]],
                                      [ 0,  0,  0, 1]])
    
                        G = G @ T

                    idx += 4

                if fResult:
    
                    count = 0
    
                    if len(cmds) - idx > 0:
                        count = int(cmds[idx])
    
                    undo_idx.append(curr)
                    undo_mesh.append(copy.deepcopy(meshes[curr]))
    
                    if count < 2:
                        meshes[curr].transform(G)
                        vis.update_geometry(meshes[curr])
    
                    else:
                        for i in range(count):
                            meshes[curr].transform(G)
                            
                            if i == 0:
                                accum = copy.deepcopy(meshes[curr])
                            else:
                                accum += copy.deepcopy(meshes[curr])
                        
                        meshes[curr] = copy.deepcopy(accum)
                        accum.paint_uniform_color([0.9,0.9,0.9])
                        meshes_gray[curr] = copy.deepcopy(accum)
    
                        refresh(vis, meshes, fAxis)
                        ctrl.set_front([0.5, 0.25, 0.5])

        elif cmds[0] == 'polygon':

            _meshes, _names = polygon(cmds, False) # lowercase --> separate mode

            if len(_meshes) > 0:

                for i in range(len(_meshes)):

                    vis.add_geometry(_meshes[i])

                    meshes.append(_meshes[i])
                    names.append(_names[i])
                    mesh_gray = copy.deepcopy(_meshes[i])
                    mesh_gray.paint_uniform_color([0.9,0.9,0.9])
                    meshes_gray.append(mesh_gray)

                curr = len(meshes) - 1
                mesh_gray = copy.deepcopy(mesh)
                ctrl.set_front([0.5, 0.25, 0.5])
                vis.update_geometry(mesh)

        elif cmds[0] == 'POLYGON':

            _meshes, _names = polygon(cmds, True) # uppercase --> integrate mode

            if len(_meshes) > 0:

                vis.add_geometry(_meshes[0])
                meshes.append(_meshes[0])
                names.append(_names[0])
                mesh_gray = copy.deepcopy(_meshes[0])
                mesh_gray.paint_uniform_color([0.9,0.9,0.9])
                meshes_gray.append(mesh_gray)

                curr = len(meshes) - 1
                mesh_gray = copy.deepcopy(mesh)
                ctrl.set_front([0.5, 0.25, 0.5])
                vis.update_geometry(mesh)

        elif cmds[0][0] == 'u':

            if len(undo_mesh) > 0:

                idx = undo_idx.pop()
                mesh = undo_mesh.pop()
                meshes[idx] = copy.deepcopy(mesh)
 
                vis.update_geometry(meshes[idx])
                refresh(vis, meshes, fAxis)
                ctrl.set_front([0.5, 0.5, 0.5])

            else:
                print('undo buffer is empty')

        elif cmds[0] == 'save':

            if len(meshes) > 1:
                
                for i in range(1,len(meshes)):
                    if i == 1:
                        accum = copy.deepcopy(meshes[i])
                    else:
                        accum += meshes[i]
                o3d.io.write_triangle_mesh(cmds[1], accum)
                print('save %s' % cmds[1])
            else:
                print('no meshes to be saved')

        elif cmds[0] == 'quit':
            break

    except queue.Empty:
        pass

    if not vis.poll_events():
        break
    vis.update_renderer()

vis.destroy_window()
