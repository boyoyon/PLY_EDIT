import cv2, os, sys
import numpy as np
import mediapipe as mp

NR_KEYPOINTS = 33

argv = sys.argv
argc = len(argv)

if argc < 2:
    print('%s estimate pose' % argv[0])
    print('%s <images>' % argv[0])
    quit()

bgr_image = cv2.imread(argv[1])
image_height, image_width, _ = bgr_image.shape
rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

mp_pose = mp.solutions.pose

with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5) as pose:

    image = cv2.imread(argv[1])
    image_height, image_width, _ = image.shape
    results = pose.process(rgb_image)

print(results.pose_landmarks)

p = []
for keypoint in range(NR_KEYPOINTS): 

    x = results.pose_landmarks.landmark[keypoint].x
    y = results.pose_landmarks.landmark[keypoint].y
    z = results.pose_landmarks.landmark[keypoint].z

    p.append((x, y, z))

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_pose_keypoints.npy' % filename

np.save(dst_path, np.array(p))
print('save %s' % dst_path)



