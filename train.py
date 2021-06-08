# -*- coding: utf-8 -*-
"""Copy of fruits.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QbQJlLidgOe_bKuqE65CoYDcKA7L0klL
"""

!mkdir data

cd data

!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/apple.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/pineapple.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/grapes.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/banana.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/eye.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/face.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/star.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/bowtie.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/house.npy
!wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/cloud.npy

!ls

cd ..

from sklearn.model_selection import train_test_split as tts
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.utils import np_utils
from random import randint
import numpy as np
import os
from PIL import Image

N_FRUITS = 10
FRUITS = {0: "Apple", 1: "Banana", 2: "Grape", 3: "Pineapple",4:"eye", 5:"face",6:"star",7:"bowtie",8:"house",9:"cloud"}

# number of samples to take in each class
N = 5000

N_EPOCHS = 10

# data files in the same order as defined in FRUITS
files = ["apple.npy", "banana.npy", "grapes.npy", "pineapple.npy","eye.npy", "face.npy","star.npy","bowtie.npy","house.npy","cloud.npy"]

def load(dir, reshaped, files):
    "Load .npy or .npz files from disk and return them as numpy arrays. \
    Takes in a list of filenames and returns a list of numpy arrays."

    data = []
    for file in files:
        f = np.load(dir + file)
        if reshaped:
            new_f = []
            for i in range(len(f)):
                x = np.reshape(f[i], (28, 28))
                x = np.expand_dims(x, axis=0)
                x = np.reshape(f[i], (28, 28, 1))
                new_f.append(x)
            f = new_f
        data.append(f)
    return data


def normalize(data):
    "Takes a list or a list of lists and returns its normalized form"

    return np.interp(data, [0, 255], [-1, 1])

def visualize(array):
    "Visulaze a 2D array as an Image"
    array = np.reshape(array, (28,28))
    img = Image.fromarray(array)
    return img


def set_limit(arrays, n):
    "Limit elements from each array up to n elements and return a single list"
    new = []
    for array in arrays:
        i = 0
        for item in array:
            if i == n:
                break
            new.append(item)
            i += 1
    return new


def make_labels(N1, N2):
    "make labels from 0 to N1, each repeated N2 times"
    labels = []
    for i in range(N1):
        labels += [i] * N2
    return labels

fruits = load("data/", False, ['star.npy'])

visualize(fruits[0][90])

#second argument is True for reshaping the image to a 28x28 form. A conv net expects this format.
fruits = load("data/", True, files)

#second argument is False because we don't need to reshape the image. An MLP net expects this format.
#fruits = load("data/", False, files)


# limit no of samples in each class to N
fruits = set_limit(fruits, N)

# normalize the values
fruits = map(normalize, fruits)

# define the labels
labels = make_labels(N_FRUITS, N)

# prepare the data
x_train, x_test, y_train, y_test = tts(fruits, labels, test_size=0.05)

# one hot encoding
Y_train = np_utils.to_categorical(y_train, N_FRUITS)
Y_test = np_utils.to_categorical(y_test, N_FRUITS)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28,28,1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(N_FRUITS, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


# train
model.fit(np.array(x_train), np.array(Y_train), batch_size=32, epochs=N_EPOCHS)

print "Training complete"

print "Evaluating model"
preds = model.predict(np.array(x_test))

score = 0
for i in range(len(preds)):
    if np.argmax(preds[i]) == y_test[i]:
        score += 1

print "Accuracy: ", ((score + 0.0) / len(preds)) * 100


model.save("fruits"+ ".h5")
print "Model saved"

print preds[0]

print(type(preds))

print type(preds)

model.save('/content/drive/My Drive/doodle.h5')
