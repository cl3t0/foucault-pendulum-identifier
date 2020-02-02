import numpy as np
import cv2
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD

training = False
weights = 'model_weights_8_day.h5'

w = 480
h = 270

model = Sequential()
model.add(Dense(8, input_dim=3*w*h))
model.add(Dense(3))
sgd = SGD(lr=1e-10, nesterov=True)
model.compile(loss='mse',
              optimizer=sgd,
              metrics=['accuracy'])

if training == False:
    model.load_weights(weights)

def loading_training_dataset():
    images = []
    labels = []
    images_list = os.listdir("training_dataset/images")
    quantity_images = len(images_list)
    labels_list = os.listdir("training_dataset/labels")
    quantity_labels = len(labels_list)
    if quantity_images != quantity_labels:
        print("wrong quantities")
        exit(0)
    n = quantity_images
    for i in range(1, n+1):
        image = cv2.imread("training_dataset/images/"+str(i)+".jpeg")
        flat_image = np.reshape(image, (3*w*h))
        images.append(flat_image)
        label_file = open("training_dataset/labels/"+str(i)+".txt", "r")
        content = label_file.read()
        new_label = list(map(float, content.split()))
        # new_label[0] /= w
        # new_label[1] /= h
        # new_label[2] /= w
        labels.append(new_label)
        label_file.close()
    images = np.array(images)
    labels = np.array(labels)
    return images, labels

cap = cv2.VideoCapture("http://131.173.8.23/mjpg/video.mjpg")

if training:
    images, labels = loading_training_dataset()
    model.fit(images, labels,
            epochs=1000,
            batch_size=20,
            shuffle=True)

    model.save_weights(weights)

if training == False:
    while True:
        ret, frame = cap.read()
        new_frame = cv2.resize(frame, (w, h))
        X = np.reshape(new_frame, (3*w*h))
        result = model.predict(np.array([X]))
        x = abs(result[0][0])
        y = abs(result[0][1])
        r = abs(result[0][2])
        print("x:",x)
        print("y:",y)
        print("r:",r)
        cv2.circle(new_frame, (int(x), int(y)), int(r), (0, 0, 255), 4)
        cv2.circle(new_frame, (int(x), int(y)), 2, (0, 0, 255), 4)
        cv2.imshow("image", new_frame)
        if cv2.waitKey(1) == 27:
            exit(0)