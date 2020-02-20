import numpy as np
import random

TRYTIME = 19

TOTAL_NUMBER_OF_SCENEARIOS = 2000

lastmove = 'S'

moves = ['L', 'R', 'U', 'D']

holdSpace = [2,2]

def createBoard(x,sizeX, sizeY):
    counter = 1

    for m in range(0,sizeY):
        for l in range(0,sizeX):
            
            x[index(x,l,m)] = counter
            counter = counter + 1

    x[index(x,sizeX-1,sizeY-1)] = -1
    holdSpace.append(sizeX - 1)
    holdSpace.append(sizeY - 1)

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
    return (y * 9) + x

arr = []

j=0
while j<TOTAL_NUMBER_OF_SCENEARIOS:

    X = np.zeros((81,), dtype=float)
    
    createBoard(X,3,3)
    i=0
    holdSpace = [2,2]
    arrOfBoards = []
    arrOfBoards.append(X)
    y=X.copy()

    while i<TRYTIME:
        randomMove = random.choice(moves)
        while not isAvailableMove(X,randomMove) :
            randomMove = random.choice(moves)
        move(y,randomMove)
        lastmove = '%s' % randomMove 
        arrOfBoards.append(y.copy())
        i = i+1
    
    arrOfBoards = np.flip(arrOfBoards,0)
    arr.append(arrOfBoards)
    j=j+1

# Importing the Keras libraries and packages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout


X_train = []
y_train = []


for i in range(0,TOTAL_NUMBER_OF_SCENEARIOS):
    for j in range(1, TRYTIME):
        X_train.append(arr[i][j-1:j])
        y_train.append(arr[i][j])
       

X_train, y_train = np.array(X_train), np.array(y_train)

print(X_train.shape)
print(y_train.shape)

model = Sequential()

model.add(LSTM(units = 50, return_sequences = True, input_shape = (1, 81)))
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
model.add(Dense(units = 81))

model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=3)

x_input = np.zeros((81,), dtype=int)
counter = 0.01
for m in range(0,3):
    for l in range(0,3):
        x_input[index(x_input,l,m)] = counter
        counter = counter + 0.01

x_input[index(x_input,2,2)] = -1


x_input = x_input.reshape((1, 1, 81))

yhat = model.predict(x_input, verbose=0)
print(yhat)