import os
import time
import face_recognition
import pickle
import cv2
import imutils
from faceApp.base_camera import BaseCamera
import datetime


class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        encodings_file = 'G:/PROJET/PYTHON/FACE_RECOGNITION/Real_time_face_recognition_with_GPU/encoding_the_face_using_cv2_and_deep_learning/encodings/encodings.pickel'
        #encodings_file = 'G:/PROJET/PYTHON/FACE_RECOGNITION/Real_time_face_recognition_with_GPU_FLASK_V2/faceApp/static/dataset/encodings/encodings.pickel'

        data = pickle.loads(open(encodings_file, "rb").read())

        print("[INFO] Commencer le video stream........")

        writer = None
        time.sleep(2.0)

        while True:

            _, frame = camera.read()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(rgb, width=750)
            r = frame.shape[1] / float(rgb.shape[1])

            '''
            détecter les coordonnées (x, y) des boîtes englobantes correspondantes
            à chaque visage dans l'image d'entrée 
            '''
            boxes = face_recognition.face_locations(rgb, model='cnn')

            '''
            calculez les plongements faciaux pour chaque visage
            '''
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            for encoding in encodings:

                '''
                essayer de faire correspondre chaque visage de l'image d'entrée à notre encodages
                En interne, le compare_faces  La fonction calcule la distance euclidienne entre l'incorporation 
                candidate et toutes les faces de notre jeu de données

                '''
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = "INCONNU"

                if True in matches:
                    '''
                    trouver les index de toutes les faces appariées puis initialiser un
        			dictionnaire pour compter le nombre total de fois par visage
        			a été apparié
        			( Pdb ) matchedIdxs
                        [ 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 
                        50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 ,63 , 64 , 65 , 
                        66 , 67 , 68 , 69 , 71 , 72 , 73 , 74 , 75 ]
                    '''
                    matchesIdxs = [i for (i, b) in enumerate(matches) if b]

                    '''
                    tiendra le nom du personnage comme  clé, le nombre de votes comme  valeur
                    '''
                    counts = {}

                    '''
                    boucle sur les index correspondants et conserve un décompte pour
        			chaque visage reconnu
        			( Pdb ) compte
                    { 'hatim_allouane' : 40 }
                    //counts[name] = counts.get(name, 0) + 1
                    nous n'avons que 41 photos d'Ian dans l'ensemble de données, 
                    donc un score de 40 sans vote pour quelqu'un d'autre est extrêmement élevé.
                    '''
                    for i in matchesIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    '''
                    déterminer le visage reconnu avec le plus grand nombre
        			de votes (note: en cas d'égalité improbable Python
        			sélectionnera la première entrée du dictionnaire)
        			extrait le nom avec le plus de votes decompte , dans ce cas, il serait hatim_allouane .
                    '''
                    name = max(counts, key=counts.get)

                '''
                mettre à jour la liste des noms
                '''
                names.append(name)

            for ((top, right, bottom, left), name) in zip(boxes, names):
                top = int(top * r)
                right = int(right * r)
                bottom = int(bottom * r)
                left = int(left * r)

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            timestamp = datetime.datetime.now()
            cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)



            if writer is None and f'G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\output' is not None:
                try:

                    # creating a folder named data
                    timestamp_output = datetime.datetime.now()
                    if not os.path.exists(
                            f'G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\output\\{timestamp_output.strftime("%A %d %B %Y")}'):
                        os.makedirs(
                            f'G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\output\\{timestamp_output.strftime("%A %d %B %Y")}')

                    # if not created then raise error
                except OSError:
                    print('Error: Creating directory of data')
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(f'G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\output\\{timestamp_output.strftime("%A %d %B %Y")}\\{timestamp_output.strftime("%I_%M_%S")}'+'.avi'
                                         , fourcc, 20, (frame.shape[1], frame.shape[0]), True)

            '''
            si l'auteur n'est pas Aucun, écrivez le cadre avec reconnu
            faces au disque
            '''
            if writer is not None:
                writer.write(frame)


            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', frame)[1].tobytes()
