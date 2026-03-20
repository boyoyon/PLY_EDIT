# https://google.github.io/mediapipe/solutions/hands.html
import cv2, os, sys
import mediapipe as mp
import numpy as np

NR_KEYPOINTS = 21

argv = sys.argv
argc = len(argv)

print('%s extracts fingers from the image' % argv[0])
print('[usage] python %s <image>' % argv[0])

if argc < 2:
    quit()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

image = cv2.imread(argv[1])
points = []
    
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
   
    results = hands.process(image)

    if results.multi_hand_landmarks:

      hands = []
      for hand_landmarks in results.multi_hand_landmarks: # hand <-- hands

          p = []
          for keypoint in range(NR_KEYPOINTS): # keypoints <-- hand

              x = hand_landmarks.landmark[keypoint].x
              y = hand_landmarks.landmark[keypoint].y
              z = hand_landmarks.landmark[keypoint].z

              p.append((x, y, z))

          if len(p) == NR_KEYPOINTS:

              THUMB  = (p[1],p[2],p[3],p[4])
              INDEX  = (p[5],p[6],p[7],p[8])
              MIDDLE = (p[9],p[10],p[11],p[12])
              RING   = (p[13],p[14],p[15],p[16])
              PINKY  = (p[17],p[18],p[19],p[20])
            
              hands.append((THUMB, INDEX, MIDDLE, RING, PINKY)) 

nr_hands = len(hands)

if nr_hands > 0:

    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]

    for i, hand in enumerate(hands):
        hand = np.array(hand)
        if nr_hands == 1:
            dst_path = '%s_fingers.npy' % filename
        else:
            dst_path = '%s_hand_%d_fingers.npy' % (filename, (i+1))

        np.save(dst_path, hand)
        print('save %s' % dst_path)
