import numpy as np
import open3d as o3d
import sys

def create_checkered_pattern(size, space, outer=np.array((128, 128, 255)), inner=np.array((200,200,255))):

    accumFront = None
    accumBack = None

    zz = -1
    for i, z in enumerate(np.arange(-size/2, size/2+space, step)):
        zz *= -1
        xx = -1
        for j, x in enumerate(np.arange(-size/2, size/2+space, step)):
            xx *= -1
            if xx * zz > 0:
                points = []
                points.append((x, 0, z))
                points.append((x + step, 0, z))
                points.append((x + step, 0, z+step))
                points.append((x, 0, z+step))             
                points = np.array(points)

                faces = []
                faces.append((0, 3, 1))
                faces.append((1, 3, 2))    
                faces = np.array(faces)    

                meshFront = o3d.geometry.TriangleMesh()
                meshFront.vertices = o3d.utility.Vector3dVector(points)
                meshFront.triangles = o3d.utility.Vector3iVector(np.array(faces))
                
                meshBack = o3d.geometry.TriangleMesh()
                meshBack.vertices = o3d.utility.Vector3dVector(points)
                meshBack.triangles = o3d.utility.Vector3iVector(np.array(faces)[:,[0,2,1]])
                meshBack.compute_vertex_normals()
                
                if i == 0 and j == 0:
                    accumFront = meshFront
                    accumBack = meshBack
                else:
                    accumFront += meshFront
                    accumBack += meshBack
 
    accumFront.paint_uniform_color(outer/255)
    accumBack.paint_uniform_color(inner/255)

    return accumFront, accumBack

argv = sys.argv
argc = len(argv)

print('%s creates checkered pattern' % argv[0])
print('[usage] python %s <size> <step>' % argv[0])

if argc < 3:
    quit()

size = eval(argv[1])
step = eval(argv[2])

checkerFront, checkerBack = create_checkered_pattern(size, step)
o3d.visualization.draw_geometries([checkerFront, checkerBack])

dst_path = 'checkerA.ply'
o3d.io.write_triangle_mesh(dst_path, checkerFront)
print('save %s' % dst_path)

dst_path = 'checkerAA.ply'
o3d.io.write_triangle_mesh(dst_path, checkerBack)
print('save %s' % dst_path)
