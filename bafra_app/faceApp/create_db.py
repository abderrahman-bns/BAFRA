import cv2
import os


def create_db():
    TRAINING_BASE = 'G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\vid'
    dirs = os.listdir(TRAINING_BASE)

    for label in dirs:
        for i, fn in enumerate(os.listdir(os.path.join(TRAINING_BASE, label))):
            print(f"start collecting faces from {label}'s data")
            cam = cv2.VideoCapture(os.path.join(TRAINING_BASE, label, fn))
            #cam = cv2.VideoCapture(os.path.join(TRAINING_BASE, f'{label}.mp4'))
            # Read the video from specified path
            #cam = cv2.VideoCapture("C:\\Users\\Admin\\PycharmProjects\\project_1\\openCV.mp4")
            try:

                # creating a folder named data
                if not os.path.exists(f'G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\img\\{label}'):
                    os.makedirs(f'G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\img\\{label}')

                # if not created then raise error
            except OSError:
                print('Error: Creating directory of data')

            # frame
            currentframe = 0

            while (True):

                # reading from frame
                ret, frame = cam.read()

                if ret:
                    if currentframe % 4 == 0:
                        # if video is still left continue creating images
                        name = f'G:\\PROJET\\PYTHON\\FACE_RECOGNITION\\Real_time_face_recognition_with_GPU_FLASK_V2\\faceApp\\static\\dataset\\img\\{label}\\{label}' + str(currentframe) + '.jpg'
                        print('Creating...' + name)

                        # writing the extracted images
                        cv2.imwrite(name, frame)

                        # increasing counter so that it will
                        # show how many frames are created
                    currentframe += 1
                else:
                    break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()