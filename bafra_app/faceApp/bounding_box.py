import os
import cv2
from faceApp.base_camera import BaseCamera
import numpy as np
import imutils


class CameraTest(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            CameraTest.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(CameraTest, self).__init__()

    @staticmethod
    def set_video_source(source):
        CameraTest.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(CameraTest.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        path_prototxt = 'models/deploy.prototxt.txt'
        path_model = "models/res10_300x300_ssd_iter_140000.caffemodel"
        net = cv2.dnn.readNetFromCaffe(path_prototxt, path_model)
        while True:
            # read current frame
            _, img = camera.read()

            img = imutils.resize(img, width=400)

            (h, w) = img.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

            net.setInput(blob)
            detections = net.forward()

            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence < 0.5:
                    continue

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY -10 > 10 else startY +10
                cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 1)
                cv2.putText(img, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()



