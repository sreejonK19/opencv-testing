# import the necessary packages
import numpy as np
import dlib
import cv2
import imutils
from imutils import face_utils
from pakages.facial_landmarks import visualize_facial_landmarks

# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# initialize the camera
cam = cv2.VideoCapture(0)

flag = 0
while (True):
    # load the input image
    ret, image = cam.read()
    if ret is True:
        # resize input image and convert it to gray scale
        image = imutils.resize(image, width = 500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect faces in the gray scale image
        rects = detector(gray, 1)

        # loop over the face detections
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then convert the landmark (x, y)-coordinates to a NumPy array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # loop over the face parts individually
            for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
                # clone the original image so we can draw on it, then display the name of the face part on the image
                clone = image.copy()
                cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # loop over the subset of facial landmarks, drawing the specific face part
                for (x, y) in shape[i:j]:
                    cv2.circle(clone, (x, y), 2, (0, 0, 255), -1)

                # extract the ROI of the face region as a separate image
                (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
                roi = image[y:y + h, x:x + w]
                roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)

                # show the particular face part
                # cv2.imshow("ROI", roi)
                # cv2.imshow("Image", clone)
                # cv2.waitKey(0)

                if name == "mouth":
                    break

            if flag == 0: # for default green color
                output = visualize_facial_landmarks(image, shape)
            elif flag == 1: # for green color
                output = visualize_facial_landmarks(image, shape)
            elif flag == 2: # for blue color
                output = visualize_facial_landmarks(image, shape, (230, 159, 23))
            elif flag == 3: # for black color
                output = visualize_facial_landmarks(image, shape, (0, 0, 0))

            cv2.imshow("Image", output)
            # cv2.waitKey(0)

        if cv2.waitKey(1) == ord('1'):
            flag = 1
        elif cv2.waitKey(1) == ord('2'):
            flag = 2
        elif cv2.waitKey(1) == ord('3'):
            flag = 3
        elif cv2.waitKey(1) == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
