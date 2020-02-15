
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, CuDNNLSTM ,LSTM

mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test)
'''
model = Sequential()

model.add(LSTM(128,input_shape=x_train.shape[1:],return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(128))
model.add(Dropout(0.2))

model.add(Dense(16,activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(10,activation='softmax'))

opt = keras.optimizers.Adam(lr=1e-3, decay=1e-5)

model.compile(loss='sparse_categorical_crossentropy',
    optimizer=opt,
    metrics=['accuracy'])

model.fit(x_train,y_train, epochs=3, validation_data=(x_test,y_test))

'''