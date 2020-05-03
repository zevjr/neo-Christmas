import numpy as np
import re
import tensorflow as tf
import pandas as pd
import matplotlib
from googletrans import Translator
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils
import keras.backend.tensorflow_backend as tb

var = '''
        and the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.
        and God said, Let there be light: and there was light.
        and God saw the light, that it was good: and God divided the light from the darkness.
        and God called the light Day, and the darkness he called Night. And the evening and the morning were the first day.
        and God said, Let there be a firmament in the midst of the waters, and let it divide the waters from the waters.
        and God made the firmament, and divided the waters which were under the firmament from the waters which were above the firmament: and it was so.
        and God called the firmament Heaven. And the evening and the morning were the second day.
    '''
countsLabels = {}
var = re.sub('[^A-Za-z- ]+', '', var)

for i in var.split():
    if i not in countsLabels.keys():
        countsLabels[i] = 1
    else:
        countsLabels[i] = (countsLabels[i] + 1)

print(countsLabels)

