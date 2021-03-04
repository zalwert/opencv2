import cv2
import os

PICTURES_FOLDER = '\\Pictures\\'
PROCESSED_PNG = 'processed.png'
fullbody_classifier = 'fullbody'
upperbody_classifier = 'upperbody'
face1_classifier = 'face1'
face2_classifier = 'face2'
face3_classifier = 'face3'
face4_classifier = 'face4'
face5_classifier = 'face5'
XMLS_FOLDER = '\\xmls\\'
XML = '.xml'

classifiers_list = [fullbody_classifier, upperbody_classifier,
                    face1_classifier,
                    face2_classifier, face3_classifier,
                    face4_classifier, face5_classifier]


def detect_objects(path_img):
    save = False
    img = cv2.imread(path_img)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for classifier in classifiers_list:

        _tracker = cv2.CascadeClassifier(os.getcwd() + XMLS_FOLDER
                                         + classifier + XML)
        objects = _tracker.detectMultiScale(gray_img)

        if len(objects) > 0:
            save = True

        for (x, y, w, h) in objects:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(img, classifier, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if save:
        cv2.imwrite(path_img[:-4] + PROCESSED_PNG, img)
        return path_img[:-4] + PROCESSED_PNG

    return 'no_objects'
