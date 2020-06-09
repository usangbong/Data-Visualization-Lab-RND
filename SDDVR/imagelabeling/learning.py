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
from keras.layers import ZeroPadding2D
from keras.optimizers import Adam
from keras import regularizers

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

class Learning():
    def create_learning_model_VGG16model(classes) :
        model = Learning.VGG16model(classes)
        #model = Learning.smallerVGGmodel(classes)
        return model

    def create_learning_LeNetmodel(classes) :
        model = Learning.LeNETmodel(classes)
        return model

    def create_learning_AlexnetModel(classes) :
        model = Learning.AlexnetModel(classes)
        return model

#    def AlexnetModel(img_shape=(224, 224, 3), n_classes=5, l2_reg=0., weights=None):
    def AlexnetModel(classes):
        img_shape = (64, 64, 3)
        n_classes = classes

        model = Sequential()
        model.add(Conv2D(64,(11,11),strides=4, padding='valid', input_shape=img_shape))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(192,(5,5),padding='same'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(ZeroPadding2D((1, 1)))
        model.add(Conv2D(384,(3,3),padding='same'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(ZeroPadding2D((1, 1)))
        model.add(Conv2D(256, (3, 3), padding='same'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(ZeroPadding2D((1, 1)))
        model.add(Conv2D(256, (3, 3), padding='same'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(4096))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(4096))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(n_classes))
        model.add(BatchNormalization())
        model.add(Activation('softmax'))
        return model

        '''
        # Initialize model
        alexnet = Sequential()

        # Layer 1
        #, kernel_regularizer= regularizers.l2(l2_reg)
        alexnet.add(Conv2D(96, (11, 11), input_shape=img_shape,
        padding='same'))
        alexnet.add(BatchNormalization())
        alexnet.add(Activation('relu'))
        alexnet.add(MaxPooling2D(pool_size=(2, 2)))

        # Layer 2
        alexnet.add(Conv2D(256, (5, 5), padding='same'))
        alexnet.add(BatchNormalization())
        alexnet.add(Activation('relu'))
        alexnet.add(MaxPooling2D(pool_size=(2, 2)))

        # Layer 3
        alexnet.add(ZeroPadding2D((1, 1)))
        alexnet.add(Conv2D(512, (3, 3), padding='same'))
        alexnet.add(BatchNormalization())
        alexnet.add(Activation('relu'))
        alexnet.add(MaxPooling2D(pool_size=(2, 2)))

        # Layer 4
        alexnet.add(ZeroPadding2D((1, 1)))
        alexnet.add(Conv2D(1024, (3, 3), padding='same'))
        alexnet.add(BatchNormalization())
        alexnet.add(Activation('relu'))

        # Layer 5
        alexnet.add(ZeroPadding2D((1, 1)))
        alexnet.add(Conv2D(1024, (3, 3), padding='same'))
        alexnet.add(BatchNormalization())
        alexnet.add(Activation('relu'))
        alexnet.add(MaxPooling2D(pool_size=(2, 2)))

        # Layer 6
        alexnet.add(Flatten())
        alexnet.add(Dense(3072))
        alexnet.add(BatchNormalization())
        alexnet.add(Activation('relu'))
        alexnet.add(Dropout(0.5))

        # Layer 7
        alexnet.add(Dense(4096))
        alexnet.add(BatchNormalization())
        alexnet.add(Activation('relu'))
        alexnet.add(Dropout(0.5))

        # Layer 8
        alexnet.add(Dense(n_classes))
        alexnet.add(BatchNormalization())
        alexnet.add(Activation('softmax'))

        if weights is not None:
          alexnet.load_weights(weights)

        return alexnet
        '''

    def LeNETmodel(classes) :
        #LeNET
        model = Sequential()
        #Layer 1
        #Conv Layer 1
        model.add(Conv2D(filters = 6,
                         kernel_size = 5,
                         strides = 1,
                         activation = 'relu',
                         input_shape = (32,32,1)))

        #Pooling layer 1
        model.add(MaxPooling2D(pool_size = 2, strides = 2))
        #Layer 2
        #Conv Layer 2
        model.add(Conv2D(filters = 16,
                         kernel_size = 5,
                         strides = 1,
                         activation = 'relu',
                         input_shape = (14,14,6)))
        #Pooling Layer 2
        model.add(MaxPooling2D(pool_size = 2, strides = 2))
        #Flatten
        model.add(Flatten())
        #Layer 3
        #Fully connected layer 1
        model.add(Dense(units = 120, activation = 'relu'))
        #Layer 4
        #Fully connected layer 2
        model.add(Dense(units = 84, activation = 'relu'))
        #Layer 5
        #Output Layer
        model.add(Dense(units = classes, activation = 'softmax'))
        model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])



        return model

    def smallerVGGmodel(classes) :
        model = Sequential()
        inputShape = (64, 64, 3)

        # (CONV => RELU ) * 2 => POOL
        model.add(Conv2D(32, (3, 3), padding="same",
            input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(Conv2D(32, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        # use a *softmax* activation for single-label classification
        # and *sigmoid* activation for multi-label classification
        model.add(Dense(classes))
        model.add(Activation("sigmoid"))

        return model

    #change architecture (VGG16 -> VGG19)
    def VGG16model(classes):
        model = Sequential()
        inputShape = (64, 64, 3)

        # (CONV => RELU ) * 2 => POOL
        model.add(Conv2D(64, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        #model.add(Dropout(0.25))

        # (CONV => RELU ) * 2 => POOL
        model.add(Conv2D(128, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        #model.add(Dropout(0.25))

        # (CONV => RELU ) * 3 => POOL
        model.add(Conv2D(256, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(Conv2D(256, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(Conv2D(256, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(Conv2D(256, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        #model.add(Dropout(0.25))

        # (CONV => RELU ) * 3 => POOL
        model.add(Conv2D(512, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        #model.add(Dropout(0.25))

        # (CONV => RELU ) * 3 => POOL
        model.add(Conv2D(512, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=1))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        #model.add(Dropout(0.25))

        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(4096))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))
        model.add(Dense(4096))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))
        model.add(Dense(1000))
        model.add(BatchNormalization())
        #model.add(Dropout(0.25))

        # use a *softmax* activation for single-label classification
        # and *sigmoid* activation for multi-label classification
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        return model

   # def parameters..(dataset) :

    def _setTrainData() :
        _traingen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _trainset = _traingen.flow_from_directory('../imgs/bonsai/classified/img_type2_train', target_size = (64,64),
                                                 batch_size = 64, color_mode='rgb', class_mode = 'categorical',
                                                 shuffle = True)
        return _trainset

    def _setTestData() :
        _testgen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _testset  = _testgen.flow_from_directory('../imgs/bonsai/classified/img_type2_test', target_size = (64,64),
                                                 batch_size = 64, color_mode='rgb', class_mode = 'categorical',
                                                 shuffle = True)
        return _testset

    def _setTrainData_gray() :
        _traingen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _trainset = _traingen.flow_from_directory('../imgs/bonsai/classified_gray/img_type2_train', target_size = (64,64),
                                                 batch_size = 64, color_mode='rgb', class_mode = 'categorical',
                                                 shuffle = True)
        return _trainset

    def _setTestData_gray() :
        _testgen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _testset  = _testgen.flow_from_directory('../imgs/bonsai/classified_gray/img_type2_test', target_size = (64,64),
                                                 batch_size = 64, color_mode='rgb', class_mode = 'categorical',
                                                 shuffle = True)
        return _testset

    def _setTrainData_edge() :
        _traingen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _trainset = _traingen.flow_from_directory('../imgs/bonsai/classified_edge/img_type2_train', target_size = (64,64),
                                                 batch_size = 64, color_mode='rgb', class_mode = 'categorical',
                                                 shuffle = True)
        return _trainset

    def _setTestData_edge() :
        _testgen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _testset  = _testgen.flow_from_directory('../imgs/bonsai/classified_edge/img_type2_test', target_size = (64,64),
                                                 batch_size = 64, color_mode='rgb', class_mode = 'categorical',
                                                 shuffle = True)
        return _testset

    def _setTrainData_LeNET() :
        _traingen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _trainset = _traingen.flow_from_directory('../imgs/bonsai/classified/img_type2_train', target_size = (32,32),
                                                 batch_size = 32, color_mode='grayscale', class_mode = 'categorical',
                                                 shuffle = True)
        return _trainset

    def _setTestData_LeNET() :
        _testgen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _testset  = _testgen.flow_from_directory('../imgs/bonsai/classified/img_type2_test', target_size = (32,32),
                                                 batch_size = 32, color_mode='grayscale', class_mode = 'categorical',
                                                 shuffle = True)
        return _testset

    def _setTrainData_AlexNet() :
        _traingen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _trainset = _traingen.flow_from_directory('../imgs/bonsai/classified/img_type2_train', target_size = (64,64),
                                                 batch_size = 64, color_mode='rgb', class_mode = 'categorical',
                                                 shuffle = True)
        return _trainset

    def _setTestData_AlexNet() :
        _testgen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        _testset  = _testgen.flow_from_directory('../imgs/bonsai/classified/img_type2_test', target_size = (64,64),
                                                 batch_size = 64, color_mode='rgb', class_mode = 'categorical',
                                                 shuffle = True)
        return _testset

    def splitData() :
        for i in range(1, 6) :
            file_list = os.listdir('../imgs/bonsai/classified/img_type2_check/%s' %(i))
            file_list.sort()

            for filename in (file_list) :
                rnum = random.random()
                if  rnum < 0.7 :
                    #print('move to train %s' % (filename))
                    shutil.move('../imgs/bonsai/classified/img_type2_check/%s/%s' %(i, filename),
                                '../imgs/bonsai/classified/img_type2_train/%s' %(i))
                else :
                    #print('move to test %s' % (filename))
                    shutil.move('../imgs/bonsai/classified/img_type2_check/%s/%s' %(i, filename),
                                '../imgs/bonsai/classified/img_type2_test/%s' %(i))
        print('split imgs done')

    def _save_model(_model, filename) :
        Learning.Lmodel=_model
        _model.save(filename)
        print('model is saved')


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

    def canny_edge_learning() :
        mlb = Learning.get_mlb()
        model = Learning.create_learning_model(len(mlb.classes_))
        # initialize the optimizer
        opt = Adam(lr=1e-3, decay=1e-3 / 75)
        model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
        start = time.time()
        Learning.splitData()

        print("[INFO] read data...done :", (time.time() - start), 'sec')

        path1 = '../imgs/bonsai/classified'
        path2 = '../imgs/bonsai/classified_edge'
        Learning.create_empty_dirtree(path1, path2)
        Learning.edgeConvert(path1, path2)

        trainset = Learning._setTrainData_edge()
        testset = Learning._setTestData_edge()

        early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose = 0, mode='auto')
        #(trainX, testX, trainY, testY) = train_test_split(data,labels, test_size=0.2, random_state=42)

        print("[INFO] training network...")

        cnt = 0
        for root, dirs, files in os.walk(path2):
            cnt += len(files)
        print('found %d files' %(cnt))

        start = time.time()
        #H = model.fit_generator(aug.flow(trainX, trainY, batch_size=64),validation_data=(testX, testY),steps_per_epoch=len(trainX) // 64,epochs=EPOCHS, verbose=1)
        model.fit_generator(
            trainset,
            validation_data = testset,
            steps_per_epoch = int(cnt/64),
            epochs = 100,
            callbacks=[early_stop])

        print("model fit processing time: ", (time.time() - start), 'sec')
        print("model fit processing time: ", int(int((time.time() - start)/60)/60), ':',
              int((time.time() - start)/60)%60, ':', int(time.time() - start)%60)

        Learning._save_model(model, 'pyTest_model_edge.h5')

    def gray_learning() :
        mlb = Learning.get_mlb()
        model = Learning.create_learning_model(len(mlb.classes_))
        # initialize the optimizer
        opt = Adam(lr=1e-3, decay=1e-3 / 75)
        model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
        start = time.time()
        Learning.splitData()

        print("[INFO] read data...done :", (time.time() - start), 'sec')

        path1 = '../imgs/bonsai/classified'
        path2 = '../imgs/bonsai/classified_gray'
        Learning.create_empty_dirtree(path1, path2)
        Learning.grayConvert(path1, path2)

        early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose = 0, mode='auto')
        #(trainX, testX, trainY, testY) = train_test_split(data,labels, test_size=0.2, random_state=42)

        trainset = Learning._setTrainData_gray()
        testset = Learning._setTestData_gray()

        print("[INFO] training network...")

        cnt = 0
        for root, dirs, files in os.walk(path2):
            cnt += len(files)
        print('found %d files' %(cnt))


        start = time.time()
        #H = model.fit_generator(aug.flow(trainX, trainY, batch_size=64),validation_data=(testX, testY),steps_per_epoch=len(trainX) // 64,epochs=EPOCHS, verbose=1)
        model.fit_generator(
            trainset,
            validation_data = testset,
            steps_per_epoch = int(cnt/64),
            epochs = 100,
            callbacks=[early_stop])

        print("model fit processing time: ", (time.time() - start), 'sec')
        print("model fit processing time: ", int(int((time.time() - start)/60)/60), ':',
              int((time.time() - start)/60)%60, ':', int(time.time() - start)%60)

        Learning._save_model(model, 'pyTest_model_gray.h5')

    def create_empty_dirtree(srcdir, dstdir, onerror=None):
        print(dstdir)
        if os.path.exists(dstdir) :
            shutil.rmtree(dstdir)

        srcdir = os.path.abspath(srcdir)
        srcdir_prefix = len(srcdir) + len(os.path.sep)
        os.makedirs(dstdir)
        for root, dirs, files in os.walk(srcdir, onerror=onerror):
            for dirname in dirs:
                dirpath = os.path.join(dstdir, root[srcdir_prefix:], dirname)
                try:
                    os.mkdir(dirpath)
                except OSError as e:
                    if onerror is not None:
                        onerror(e)

    def grayConvert(p1, p2) :
        innerpath = p1
        innersavepath = p2
        file_list = os.listdir(innerpath)
        file_list.sort()
        #print(file_list)
        cnt = 0
        print('converting sub-images to grayscale : ')
        for innerdirname in file_list :
            file_list2 = os.listdir(innerpath+"/"+innerdirname)
            file_list2.sort()
            #print(innerpath+"/"+innerdirname)
            for innerdir2name in file_list2 :
                print('.', end='')
                file_list3 = os.listdir(innerpath+"/"+innerdirname+"/"+innerdir2name)
                file_list3.sort()
                for imgname in file_list3 :
                    img = cv2.imread( innerpath+"/"+innerdirname+"/"+innerdir2name+"/"+imgname)
                    #print(innerpath+"/"+innerdirname+"/"+imgname)
                    img_h = img.shape[0]
                    img_w = img.shape[1]
                    cnt += 1
                    savename = innersavepath+"/"+innerdirname+"/"+innerdir2name+"/"+imgname
                    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    cimg = cv2.GaussianBlur(gray_image, (5,5), 0)
                    cv2.imwrite(savename, cimg)
        print('gray converting done')

    def edgeConvert(p1, p2) :
        innerpath = p1
        innersavepath = p2
        file_list = os.listdir(innerpath)
        file_list.sort()
        #print(file_list)
        cnt = 0
        print('converting sub-images to grayscale : ')
        for innerdirname in file_list :
            file_list2 = os.listdir(innerpath+"/"+innerdirname)
            file_list2.sort()
            #print(innerpath+"/"+innerdirname)
            for innerdir2name in file_list2 :
                print('.', end='')
                file_list3 = os.listdir(innerpath+"/"+innerdirname+"/"+innerdir2name)
                file_list3.sort()
                for imgname in file_list3 :
                    img = cv2.imread( innerpath+"/"+innerdirname+"/"+innerdir2name+"/"+imgname)
                    #print(innerpath+"/"+innerdirname+"/"+imgname)
                    img_h = img.shape[0]
                    img_w = img.shape[1]
                    cnt += 1
                    savename = innersavepath+"/"+innerdirname+"/"+innerdir2name+"/"+imgname
                    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    cimg = cv2.GaussianBlur(gray_image, (5,5), 0)
                    canny = cv2.Canny(gray_image, 100, 200)
                    retval, edges = cv2.threshold(canny,127,255,cv2.THRESH_BINARY_INV)
                    cv2.imwrite(savename, edges)
        print('edge converting done')

    def learning_model_VGG16model() :
        mlb = Learning.get_mlb()
        model = Learning.create_learning_model(len(mlb.classes_))

        # initialize the optimizer
        opt = Adam(lr=1e-3, decay=1e-3 / 75)
        model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

        start = time.time()

        Learning.splitData()
        trainset = Learning._setTrainData()
        testset = Learning._setTestData()


        print("learning model to VGG16model")
        print("[INFO] read data...done :", (time.time() - start), 'sec')

        early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose = 0, mode='auto')
        #(trainX, testX, trainY, testY) = train_test_split(data,labels, test_size=0.2, random_state=42)

        print("[INFO] training network...")

        cnt = 0
        for root, dirs, files in os.walk('../imgs/bonsai/classified'):
            cnt += len(files)
        print('found %d files' %(cnt))


        start = time.time()
        #H = model.fit_generator(aug.flow(trainX, trainY, batch_size=64),validation_data=(testX, testY),steps_per_epoch=len(trainX) // 64,epochs=EPOCHS, verbose=1)
        model.fit_generator(
            trainset,
            validation_data = testset,
            steps_per_epoch = int(cnt/64),
            epochs = 100,
            callbacks=[early_stop])

        print("model fit processing time: ", (time.time() - start), 'sec')
        print("model fit processing time: ", int(int((time.time() - start)/60)/60), ':',
              int((time.time() - start)/60)%60, ':', int(time.time() - start)%60)

        Learning._save_model(model, '64_pyTest_model_VGG16.h5')
        #Learning.Lmodel = model

    def learning_model_LeNET() :
        mlb = Learning.get_mlb()
        model = Learning.create_learning_LeNetmodel(len(mlb.classes_))

        # initialize the optimizer
        opt = Adam(lr=1e-3, decay=1e-3 / 75)
        model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

        start = time.time()

        Learning.splitData()
        trainset = Learning._setTrainData_LeNET()
        testset = Learning._setTestData_LeNET()


        print("learning model to LeNETmodel")
        print("[INFO] read data...done :", (time.time() - start), 'sec')

        early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose = 0, mode='auto')
        #(trainX, testX, trainY, testY) = train_test_split(data,labels, test_size=0.2, random_state=42)

        print("[INFO] training network...")

        cnt = 0
        for root, dirs, files in os.walk('../imgs/bonsai/classified'):
            cnt += len(files)
        print('found %d files' %(cnt))


        start = time.time()
        #H = model.fit_generator(aug.flow(trainX, trainY, batch_size=64),validation_data=(testX, testY),steps_per_epoch=len(trainX) // 64,epochs=EPOCHS, verbose=1)
        model.fit_generator(
            trainset,
            validation_data = testset,
            steps_per_epoch = int(cnt/64),
            epochs = 100,
            callbacks=[early_stop])

        print("model fit processing time: ", (time.time() - start), 'sec')
        print("model fit processing time: ", int(int((time.time() - start)/60)/60), ':',
              int((time.time() - start)/60)%60, ':', int(time.time() - start)%60)

        Learning._save_model(model, '32_pyTest_model_LeNet.h5')
        #Learning.Lmodel = model

    def learning_model_AlexNet() :
        mlb = Learning.get_mlb()
        model = Learning.create_learning_AlexnetModel(len(mlb.classes_))

        # initialize the optimizer
        opt = Adam(lr=1e-3, decay=1e-3 / 75)
        model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

        start = time.time()

        Learning.splitData()
        trainset = Learning._setTrainData_AlexNet()
        testset = Learning._setTestData_AlexNet()


        print("learning model to AlexNetmodel")
        print("[INFO] read data...done :", (time.time() - start), 'sec')

        early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose = 0, mode='auto')
        #(trainX, testX, trainY, testY) = train_test_split(data,labels, test_size=0.2, random_state=42)

        print("[INFO] training network...")

        cnt = 0
        for root, dirs, files in os.walk('../imgs/bonsai/classified'):
            cnt += len(files)
        print('found %d files' %(cnt))


        start = time.time()
        #H = model.fit_generator(aug.flow(trainX, trainY, batch_size=64),validation_data=(testX, testY),steps_per_epoch=len(trainX) // 64,epochs=EPOCHS, verbose=1)
        model.fit_generator(
            trainset,
            validation_data = testset,
            steps_per_epoch = int(cnt/64),
            epochs = 100,
            callbacks=[early_stop])

        print("model fit processing time: ", (time.time() - start), 'sec')
        print("model fit processing time: ", int(int((time.time() - start)/60)/60), ':',
              int((time.time() - start)/60)%60, ':', int(time.time() - start)%60)

        Learning._save_model(model, '64_pyTest_model_AlexNet.h5')
        #Learning.Lmodel = model
