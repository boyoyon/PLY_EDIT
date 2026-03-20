import copy, cv2, os, sys
import numpy as np
import open3d as o3d
import mediapipe as mp
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
mp_face_mesh = mp.solutions.face_mesh

DEF_TRIANGLES = 'def_triangles.txt'

#奥行き補正用インデックス
RightEyeCover = 470
RightEyePupilTop = 159
RightEyePupilLeft = 469
RightEyePupilCenter = 468
RightEyePupilRight = 471
RightEyePupilBottom = 145
RightEyelidOver = 27
RightEyelidUpperLeft = 158
RightEyelidLowerLeft = 153
RightEyelidUpperCenter = 159
RightEyelidLowerCenter = 472
RightEyelidUpperRight = 160
RightEyelidLowerRight = 144

LeftEyeCover = 475
LeftEyePupilTop = 385
LeftEyePupilLeft = 474
LeftEyePupilCenter = 473
LeftEyePupilRight = 476
LeftEyePupilBottom = 374
LeftEyelidOver = 258
LeftEyelidUpperLeft = 386
LeftEyelidLowerLeft = 373
LeftEyelidUpperCenter = 385
LeftEyelidLowerCenter = 477
LeftEyelidUpperRight = 384
LeftEyelidLowerRight = 381

# 顔の特徴点で三角形で構成した、頂点インデックスのリストを読み込む
def get_triangles():

    triangles = []

    with open(os.path.join(os.path.dirname(__file__), DEF_TRIANGLES), mode='r') as f:
        lines = f.read().split('\n')
        for line in lines:
            data = line.split(' ')
            if len(data) == 3:
                triangles.append((int(data[0]), int(data[2]), int(data[1])))

    return triangles
    
# mediapipeでfacemeshを取得する
def get_vertices(image):

    vertices = []
    colors = []

    H, W = image.shape[:2]

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5) as face_mesh:
        image = image

        height, width = image.shape[:2]

        aspect = width / height

        # BGR-->RGB変換してMediapipe Facemsh処理に渡す
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # face meshが取得されたら
        if results.multi_face_landmarks:

            # 1個目だけを処理する
            face_landmarks = results.multi_face_landmarks[0]

            for landmark in face_landmarks.landmark:
                x = landmark.x
                y = landmark.y
                z = landmark.z
                vertices.append([(x - 0.5) * aspect, y - 0.5, z])

                X = int(x * W)
                Y = int(y * H)
                b = image[Y][X][0]
                g = image[Y][X][1]
                r = image[Y][X][2]

                colors.append((r/255.0, g/255.0, b/255.0))

    #奥行き補正(まぶたの引っ込み）
    dep1 = vertices[RightEyePupilTop][2]
    dep2 = vertices[RightEyelidOver][2]
    vertices[RightEyeCover][2] = np.mean((dep1, dep2))
    dep1 = vertices[LeftEyePupilTop][2]
    dep2 = vertices[LeftEyelidOver][2]
    vertices[LeftEyeCover][2] = np.mean((dep1, dep2))


    # 奥行き補正(瞳孔の下のひっこみ)
    vertices[RightEyePupilBottom][2] = vertices[RightEyelidLowerCenter][2]
    vertices[LeftEyePupilBottom][2] = vertices[LeftEyelidLowerCenter][2]

    #奥行き補正(瞳孔のひっこみ）
    dep1 = vertices[RightEyelidUpperLeft][2]
    dep2 = vertices[RightEyelidLowerLeft][2]

    vertices[RightEyePupilLeft][2] = np.min((dep1, dep2)) - np.abs(dep1 - dep2) / 16

    dep1 = vertices[RightEyelidUpperCenter][2]
    dep2 = vertices[RightEyelidLowerCenter][2]

    vertices[RightEyePupilCenter][2] = np.min((dep1, dep2)) - np.abs(dep1 - dep2) / 8

    dep1 = vertices[RightEyelidUpperRight][2]
    dep2 = vertices[RightEyelidLowerRight][2]

    vertices[RightEyePupilRight][2] = np.min((dep1, dep2)) - np.abs(dep1 - dep2) / 16

    dep1 = vertices[LeftEyelidUpperLeft][2]
    dep2 = vertices[LeftEyelidLowerLeft][2]

    vertices[LeftEyePupilLeft][2] = np.min((dep1, dep2)) - np.abs(dep1 - dep2) / 16

    dep1 = vertices[LeftEyelidUpperCenter][2]
    dep2 = vertices[LeftEyelidLowerCenter][2]

    vertices[LeftEyePupilCenter][2] = np.min((dep1, dep2)) - np.abs(dep1 - dep2) / 8

    dep1 = vertices[LeftEyelidUpperRight][2]
    dep2 = vertices[LeftEyelidLowerRight][2]

    vertices[LeftEyePupilRight][2] = np.min((dep1, dep2)) - np.abs(dep1 - dep2) / 16

    return vertices, colors

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s create facemesh from the image' % argv[0])
    print('[usage] python %s <image>' % argv[0])

    if argc < 2:
        quit()

    img = cv2.imread(argv[1])

    if img is not None:
        triangles = np.array(get_triangles())
        vertices, colors = np.array(get_vertices(img))

        nr_vertices = vertices.shape[0]

        if nr_vertices > 0:

            bgc = np.array((200, 200, 200)).astype(np.float64) / 255.0
            colorsBack = np.tile(bgc, (nr_vertices, 1))

            meshFront = o3d.geometry.TriangleMesh()
            meshFront.vertices = o3d.utility.Vector3dVector(vertices)
            meshFront.triangles = o3d.utility.Vector3iVector(triangles)
            meshFront.vertex_colors = o3d.utility.Vector3dVector(colors)
           
            trianglesBack = copy.deepcopy(triangles)[:,[0,2,1]]
 
            meshBack = o3d.geometry.TriangleMesh()
            meshBack.vertices = o3d.utility.Vector3dVector(vertices)
            meshBack.triangles = o3d.utility.Vector3iVector(trianglesBack)
            meshBack.vertex_colors = o3d.utility.Vector3dVector(colorsBack)
  
            mesh = meshFront + meshBack
            R = o3d.geometry.get_rotation_matrix_from_xyz((np.pi, -np.pi/2, 0))
            mesh.rotate(R, center=(0,0,0))
 
            base = os.path.basename(argv[1])
            filename = os.path.splitext(base)[0]
            dst_path = '%s.ply' % filename       
    
            o3d.io.write_triangle_mesh(dst_path, mesh)
            print('save %s' % dst_path)

        else:
            print('failed to extract facemesh' )

    else:
        print('failed to read image (%s)' % argv[1])
 

if __name__ == "__main__":
    main()
