import cv2
from darkflow.net.build import TFNet
import numpy as np
import time

options = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolov2.weights',
    'threshold': 0.5
}

i = 0
prev_tl = 0
prev_width = 0

tfnet = TFNet(options)
colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 418)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 418)

while True:
    stime = time.time()
    ret, frame = capture.read()
    if ret:
        results = tfnet.return_predict(frame)
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            confidence = result['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            frame = cv2.rectangle(frame, tl, br, color, 5)
            frame = cv2.putText(
                frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)
            width = br[0] - tl[0]
            height = br[1] - tl[1]
            distance = (275 / width) * 18
            #print('{}:'.format(label), width, height, distance)
            if 'cell phone' == '{}'.format(label):
                dis = (487.1 / width) * 14.34
                print('{}:'.format('Distance to cell phone:'), dis, 'cm')
                if tl[0] > (prev_tl + 5):
                    print("Moving right")
                elif tl[0] < (prev_tl - 5):
                    print('Moving left')
                if width < (prev_width - 5):
                    print('Moving away')
                elif width > (prev_width + 5):
                    print('Moving closer')
                else:
                    print('Not moving')


                if i == 2:
                    prev_tl = tl[0]
                    prev_width = width
                    i = 0
                i = i + 1
        cv2.imshow('frame', frame)
        print('FPS {:.1f}'.format(1 / (time.time() - stime)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()