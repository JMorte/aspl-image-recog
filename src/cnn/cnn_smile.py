# -*- coding: utf-8 -*-
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

import matplotlib.pyplot as plt


class CNNSmile:
    def __init__(self, dropout_prob=0.25):
        self.dropout_prob = dropout_prob
        self.model = None

    def build_model(self, input_shape):
        model = Sequential()

        model.add(Conv2D(32, (3, 3), padding='same', input_shape=input_shape))
        model.add(Activation('relu'))

        model.add(MaxPooling2D(pool_size=(2, 2)))
        # model.add(Dropout(self.dropout_prob))

        model.add(Conv2D(32, (3, 3), padding='same'))
        model.add(Activation('relu'))

        model.add(MaxPooling2D(pool_size=(2, 2)))
        # model.add(Dropout(self.dropout_prob))

        model.add(Conv2D(32, (3, 3), padding='same'))
        model.add(Activation('relu'))

        model.add(MaxPooling2D(pool_size=(2, 2)))
        # model.add(Dropout(0.5))

        model.add(Flatten())

        model.add(Dense(128))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(1))

        model.add(Activation('sigmoid'))

        optimizer = keras.optimizers.adam()

        model.compile(loss='binary_crossentropy',
                      optimizer=optimizer,
                      metrics=['accuracy'])
        self.model = model
        model.summary()

    def train_model(self, x_train, y_train,
                    batch_size=32, epochs=50):
        history = self.model.fit(x_train, y_train,
                                 batch_size=batch_size,
                                 epochs=epochs,
                                 shuffle=True,
                                 validation_split=0.1)
        # list all data in history
        print(history.history.keys())
        # summarize history for accuracy
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        # summarize history for loss
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

    def train_generator_model(self, train_generator,
                              epochs=50):
        self.model.fit_generator(train_generator,
                                 epochs=epochs)

    def evaluate_model(self, x_test, y_test):
        scores = self.model.evaluate(x_test, y_test,
                                     verbose=1)
        print('Test loss:', scores[0])
        print('Test accuracy:', scores[1])

    def save_model(self, model_path):
        self.model.save(model_path)
