import sys
import os, fnmatch
import numpy
import numpy as np
import tensorflow as tf
import pandas as pd
from googletrans import Translator
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils
import keras.backend.tensorflow_backend as tb
import wikipedia


def relationship(content):
    init = content.find('== Ver também ==') + 16
    finish = content.find('== Notas ==')
    return content[init:finish].split()


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


search = 'Lula'

wikipedia.set_lang("pt")
file = wikipedia.search(search)
data = list()
base = wikipedia.page(file[1]).content
data.append(base)

pattern, path = f'{search}.hdf5', '../db'

if find(pattern, path) is False:

    # data.append(wikipedia.summary(file[1], sentences=1))
    # data.append(relationship(base))

    for raw_text in data:
        chars = sorted(list(set(raw_text)))
        char_to_int = dict((c, i) for i, c in enumerate(chars))
        # print("Total Characters: ", len(raw_text))
        # print("Total Vocab: ", len(chars))

        seq_length = 140
        dataX = []
        dataY = []
        for i in range(0, len(raw_text) - seq_length, 1):
            seq_in = raw_text[i:i + seq_length]
            seq_out = raw_text[i + seq_length]
            dataX.append([char_to_int[char] for char in seq_in])
            dataY.append(char_to_int[seq_out])
        n_patterns = len(dataX)
        print("Total Patterns: ", n_patterns)

        X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
        X = X / float(len(chars))
        y = np_utils.to_categorical(dataY)

        model = Sequential()
        model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1], activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')

        filepath = path + "/" + pattern
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        model.fit(X, y, epochs=3, batch_size=128, callbacks=callbacks_list)

        model.load_weights(filepath)
        model.compile(loss='categorical_crossentropy', optimizer='adam')

        int_to_char = dict((i, c) for i, c in enumerate(chars))

        start = numpy.random.randint(0, len(dataX) - 1)
        pattern = dataX[start]
        print("Seed:")

        print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
        # generate characters
        for i in range(1000):
            x = numpy.reshape(pattern, (1, len(pattern), 1))
            x = x / float(len(chars))
            prediction = model.predict(x, verbose=0)
            index = numpy.argmax(prediction)
            result = int_to_char[index]
            seq_in = [int_to_char[value] for value in pattern]
            sys.stdout.write(result)
            pattern.append(index)
            pattern = pattern[1:len(pattern)]
        print("\nDone.")
else:
    for raw_text in data:
        chars = sorted(list(set(raw_text)))
        char_to_int = dict((c, i) for i, c in enumerate(chars))
        # print("Total Characters: ", len(raw_text))
        # print("Total Vocab: ", len(chars))

        seq_length = 100
        dataX = []
        dataY = []
        for i in range(0, len(raw_text) - seq_length, 1):
            seq_in = raw_text[i:i + seq_length]
            seq_out = raw_text[i + seq_length]
            dataX.append([char_to_int[char] for char in seq_in])
            dataY.append(char_to_int[seq_out])
        n_patterns = len(dataX)
        print("Total Patterns: ", n_patterns)

        X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
        X = X / float(len(chars))
        y = np_utils.to_categorical(dataY)

        model = Sequential()
        model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1], activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')

        filepath = path + "/" + pattern
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        # model.fit(X, y, epochs=3, batch_size=128, callbacks=callbacks_list)

        model.load_weights(filepath)
        model.compile(loss='categorical_crossentropy', optimizer='adam')

        int_to_char = dict((i, c) for i, c in enumerate(chars))

        start = numpy.random.randint(0, len(dataX) - 1)
        pattern = dataX[start]
        print("Seed:")

        print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
        # generate characters
        for i in range(200):
            x = numpy.reshape(pattern, (1, len(pattern), 1))
            x = x / float(len(chars))
            prediction = model.predict(x, verbose=0)
            index = numpy.argmax(prediction)
            result = int_to_char[index]
            seq_in = [int_to_char[value] for value in pattern]
            sys.stdout.write(result)
            pattern.append(index)
            pattern = pattern[1:len(pattern)]
        print("\nDone.")