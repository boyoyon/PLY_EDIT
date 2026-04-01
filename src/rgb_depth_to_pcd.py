import cv2, os, sys
import numpy as np
import open3d as o3d

KEY_LEFT  = 263
KEY_RIGHT = 262
KEY_UP    = 265
KEY_DOWN  = 264

angle_step = np.pi / 180
translation_step = 0.005
scale_up = 1.1
scale_down = 0.9

pcd = None
dst_path = None

def key_callback_updown_angle_step(vis, action, mods):

    global angle_step, translation_step

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

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

def key_callback_set_save_flag(vis, action, mods):

    o3d.io.write_point_cloud(dst_path, pcd)
    print('save %s' % dst_path)
    
    vis.destroy_window()
    return False

def main():

    global pcd, dst_path

    argv = sys.argv
    argc = len(argv)

    if argc < 3:
        print('%s loads ply and visualizes 3d model' % argv[0])
        print('%s <rgb image> <depth image> [<zScale> <focal_length:x> <focal_length:y>]' % argv[0])
        quit()

    rgb = cv2.imread(argv[1])
    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]
    dst_path = '%s_pcd.ply' % filename

    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    height, width = rgb.shape[:2]

    depth = cv2.imread(argv[2], cv2.IMREAD_UNCHANGED)

    fx = width
    fy = height

    zScale = np.min((height, width)) / 2

    if argc > 3:
        zScale = float(argv[3])
    
    if argc > 4:
        fx = int(argv[4])

    if argc > 5:
        fy = int(argv[5])

    cx = width // 2
    if argc > 6:
        cx = int(argv[6])

    cy = height // 2
    if argc > 7:
        cy = int(argv[7])

    print('zScale:%.1f, fx:%d, fy:%d, cx:%d, cy:%d' % (zScale, fx, fy, cx, cy))

    RGB = o3d.geometry.Image(rgb)

    #depth = 65535 - depth
    depth //= 2
    depth += 30000

    DEPTH = o3d.geometry.Image(depth)
    
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
            RGB, DEPTH, depth_scale=65535, convert_rgb_to_intensity=False)

    cam = o3d.camera.PinholeCameraIntrinsic()
    cam.intrinsic_matrix = np.asarray([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, cam)

    points = np.asarray(pcd.points)
    points[:,2] *= zScale
    pcd.points = o3d.utility.Vector3dVector(points)

    center = pcd.get_center()
    pcd.translate(-center)

    # 可視化の設定
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    vis.add_geometry(pcd)
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
    vis.register_key_action_callback(ord("S"), key_callback_set_save_flag)

    # 実行
    vis.run()
    vis.destroy_window()

if __name__ == '__main__':
    main()
