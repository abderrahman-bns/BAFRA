import os
import cv2
import face_recognition
from imutils import paths
import pickle


def create_encoding():
    print("[INFO] quantification des visages....")
    dataset = "G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\img\\"
    imagePaths = list(paths.list_images(dataset))

    knownEncodings = []
    knownNames = []

    for (i, imagePath) in enumerate(imagePaths):

        print("[INFO] image en traitement {}/{}".format(i + 1, len(imagePaths)))

        name = imagePath.split(os.path.sep)[-2]

        image = cv2.imread(imagePath)

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb, model='cnn')

        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:

            knownEncodings.append(encoding)
            knownNames.append(name)

    print("[INFO] encodage de sérialisation......")
    data = {"encodings": knownEncodings, "names": knownNames}
    encodings_path = 'G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\encodings\\encodings.pickel'
    f = open(encodings_path, "wb")
    f.write(pickle.dumps(data))
    f.close()