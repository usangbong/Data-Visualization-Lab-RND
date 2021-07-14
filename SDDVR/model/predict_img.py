import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras.optimizers import Adam

from sklearn.model_selection import train_test_split
from imutils import paths
from keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np
import cv2
import time
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
import matplotlib.pyplot as plt
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import MultiLabelBinarizer

import os
import random
import shutil

class Predict():

    def get_mlb() :
        mlb = MultiLabelBinarizer()
        labels = [
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5")
        ]
        mlb=MultiLabelBinarizer()
        mlb.fit(labels)
        return mlb

    def predict_classnum(unclassifiedImg, _model, _modelSize) :
        mlb = Predict.get_mlb()


        # pre-process the image for classification
        image1 = cv2.resize(unclassifiedImg, (_modelSize, _modelSize))
        image1 = image1.astype("float") / 255.0
        image1 = img_to_array(image1)
        image1 = np.expand_dims(image1, axis=0)
        proba = _model.predict(image1)[0]
        idxs = np.argsort(proba)[::-1][:2]

        predict_class=0.98
        predict_classnum=0

        for (i, j) in enumerate(idxs):
        	# build the label and draw the label on the image
        	label = "{}: {:.2f}%".format(mlb.classes_[j], proba[j] * 100)

        # show the probabilities for each of the individual labels
        for (label, p) in zip(mlb.classes_, proba):
            #print("{}: {:.2f}%".format(label, p * 100))
            if (predict_class < p) :
                predict_classnum = label
                predict_class=p


        #print("predicted class is {}".format(predict_classnum))
        return int(predict_classnum)
