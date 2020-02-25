import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.model import load_model


SIZE_X = 3
MAX_X = 9

SIZE_Y = 3
MAX_Y = 9

NUMBER_OF_TOTAL_BOARDS = ((MAX_X - SIZE_X) +1) * ((MAX_Y - SIZE_Y) +1)

for k in range(0,NUMBER_OF_TOTAL_BOARDS):

    SIZE_X = 3
    SIZE_Y = 3

    keras_file = 'model_%s.h5' % ( str(SIZE_X) + 'x' + str(SIZE_Y))
    model = load_model()

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.experimental_new_converter = True
    tflite_model = converter.convert()

    keras_file = "model_%s.tflite" % ( str(SIZE_X) + 'x' + str(SIZE_Y))
    open(keras_file,"wb").write(tflite_model)

    SIZE_X = SIZE_X+1
    k = k+1
    if SIZE_X == MAX_X + 1:
        SIZE_X=3
        SIZE_Y=SIZE_Y+1
