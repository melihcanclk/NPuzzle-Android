import numpy as np
import random

TRYTIME = 199

TOTAL_NUMBER_OF_SCENEARIOS = 2000

lastmove = 'S'

moves = ['L', 'R', 'U', 'D']

def move(x, direction):
    if direction == 'R':
        x[index(x,holdSpace[0], holdSpace[1])], x[index(x,holdSpace[0]+1, holdSpace[1])] =  x[index(x,holdSpace[0] +1, holdSpace[1])], x[index(x,holdSpace[0], holdSpace[1])]
        holdSpace[0] = holdSpace[0]+1
    elif direction == 'L':
        x[index(x,holdSpace[0], holdSpace[1])], x[index(x,holdSpace[0]-1, holdSpace[1])] =  x[index(x,holdSpace[0]-1, holdSpace[1])], x[index(x,holdSpace[0], holdSpace[1])]
        holdSpace[0] = holdSpace[0]-1
    elif direction == 'U':
        x[index(x,holdSpace[0], holdSpace[1])], x[index(x,holdSpace[0], holdSpace[1] -1)] =  x[index(x,holdSpace[0], holdSpace[1] -1)], x[index(x,holdSpace[0], holdSpace[1])]
        holdSpace[1] = holdSpace[1]-1
    elif direction == 'D':
        x[index(x,holdSpace[0], holdSpace[1])], x[index(x,holdSpace[0], holdSpace[1] +1)] =  x[index(x,holdSpace[0], holdSpace[1] +1)], x[index(x,holdSpace[0], holdSpace[1])]
        holdSpace[1] = holdSpace[1]+1

def isAvailableMove(x,direction):
    if reverse(direction) == lastmove:
        return False
    elif (direction == 'R' and holdSpace[0] +1 < 3 ) or (direction == 'L' and holdSpace[0] -1 >= 0) or (direction == 'U' and holdSpace[1] -1 >= 0) or (direction == 'D' and holdSpace[1] +1 < 3):
        return True
    else:
        return False

def reverse(direction):
    if direction == 'R':
        return 'L'
    elif direction == 'L':
        return 'R'
    elif direction == 'U':
        return 'D'
    elif direction == 'D':
        return 'U'

def index(board, x,y):
    return (y * 3) + x

arr = []

j=0
while j<TOTAL_NUMBER_OF_SCENEARIOS:

    x =  np.arange(1, 10).reshape(9)
    x[8] = -1

    i=0
    holdSpace = [2,2]
    arrOfBoards = []
    arrOfBoards.append(x)
    y=x.copy()

    while i<TRYTIME:
        randomMove = random.choice(moves)
        while not isAvailableMove(x,randomMove) :
            randomMove = random.choice(moves)
        move(y,randomMove)
        lastmove = '%s' % randomMove 
        arrOfBoards.append(y.copy())
        i = i+1
    
    arrOfBoards = np.flip(arrOfBoards,0)
    arr.append(arrOfBoards)
    j=j+1

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout


X_train = []
y_train = []


for i in range(0,TOTAL_NUMBER_OF_SCENEARIOS):
    for j in range(5, TRYTIME):
        X_train.append(arr[i][j-5:j])
        y_train.append(arr[i][j])
       

X_train, y_train = np.array(X_train), np.array(y_train)

model = Sequential()

model.add(LSTM(units = 50, return_sequences = True, input_shape = (5, 9)))
model.add(Dropout(0.2))

# Adding a second LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50, return_sequences = True))
model.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50, return_sequences = True))
model.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50))
model.add(Dropout(0.2))

# Adding the output layer
model.add(Dense(units = 9))

model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=3)

print(history.history['acc'])