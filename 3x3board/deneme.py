import numpy as np
import random

TRYTIME = 199

TOTAL_NUMBER_OF_SCENEARIOS = 2000

SIZE_X = 3
MAX_X = 3

SIZE_Y = 3
MAX_Y = 3

NUMBER_OF_TOTAL_BOARDS = ((MAX_X - SIZE_X) +1) * ((MAX_Y - SIZE_Y) +1)

lastmove = 'S'

holdSpace = []

moves = ['L', 'R', 'U', 'D']

def createBoard(x):
    counter = 1

    for m in range(0,SIZE_Y):
        for l in range(0,SIZE_X):
            
            x[index(x,l,m)] = counter
            counter = counter + 1

    x[index(x,SIZE_X-1,SIZE_Y-1)] = -1
    del holdSpace[:]
    holdSpace.append(SIZE_X - 1)
    holdSpace.append(SIZE_Y - 1)

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

def findEmpty(board):
    for i in range(0,9):
        for j in range(0,9):
            indexOfBoard = index(board,j,i)
            value = board[indexOfBoard]
            if (value) == -1:
                return j,i


def recognizeMovement(current,next):
    a = []
    for i in range (0,4):
        del holdSpace[:]
        x,y = findEmpty(current[0])
        holdSpace.append(x)
        holdSpace.append(y)
        current_copy = current[0].copy()
        if isAvailableMove(current_copy,moves[i]):
            move(current_copy,moves[i])
            comparison = current_copy == next
            if(comparison.all()):
                a.append(1)
            else:
                a.append(0)
        else:
            a.append(-1)
    a.append(0)
    return a
        

    
    

def isAvailableMove(x,direction):
    print(holdSpace,SIZE_X,SIZE_Y)
    
    if reverse(direction) == lastmove:
        return False
    elif (direction == 'R' and holdSpace[0] +1 < SIZE_X ) or (direction == 'L' and holdSpace[0] -1 >= 0) or (direction == 'U' and holdSpace[1] -1 >= 0) or (direction == 'D' and holdSpace[1] +1 < SIZE_Y):
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

arrOfAllBoards = []

arrOfScenearios = []

k=0

while k < NUMBER_OF_TOTAL_BOARDS:
    j = 0
    print(SIZE_X,SIZE_Y)
    while j<TOTAL_NUMBER_OF_SCENEARIOS:

        SIZE = SIZE_X * SIZE_Y
        X = np.zeros((81,), dtype=int)
        createBoard(X)

        i=0
        arrOfSeq = []
        arrOfSeq.append(X)
        Y=X.copy()

        while i<TRYTIME:
            randomMove = random.choice(moves)
            while not isAvailableMove(X,randomMove) :
                randomMove = random.choice(moves)
            move(Y,randomMove)
            lastmove = '%s' % randomMove 
            arrOfSeq.append(Y.copy())
            i = i+1
        
        arrOfSeq = np.flip(arrOfSeq,0)
        arrOfSeq = np.array(arrOfSeq)
        arrOfScenearios.append(arrOfSeq)
        holdSpace = []
        j=j+1

    arrOfAllBoards.append(arrOfScenearios)
    arrOfScenearios = []
    SIZE_X = SIZE_X+1
    k = k+1
    if SIZE_X == MAX_X + 1:
        SIZE_X=3
        SIZE_Y=SIZE_Y+1
    

# Importing the Keras libraries and packages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout

lastmove = 'S'

x_train_temp1 = []
y_train_temp1 = []

x_train_temp2 = []
y_train_temp2 = []

x_train = []
y_train = []

SIZE_X = 3
SIZE_Y = 3

for k in range(0,NUMBER_OF_TOTAL_BOARDS):
    for i in range(0,TOTAL_NUMBER_OF_SCENEARIOS):
        for j in range(1, TRYTIME+2):
            x_train_temp1.append(arrOfAllBoards[k][i][j-1:j])
            if j == TRYTIME+1:
                y_train_temp1.append([0, 0, 0, 0,1])
            else:
                y_train_temp1.append(recognizeMovement(arrOfAllBoards[k][i][j-1:j],arrOfAllBoards[k][i][j]))
        x_train_temp2.append(x_train_temp1)
        y_train_temp2.append(y_train_temp1)
        x_train_temp1 = []
        y_train_temp1 = []
    SIZE_X = SIZE_X+1
    k = k+1
    if SIZE_X == MAX_X + 1:
        SIZE_X=3
        SIZE_Y=SIZE_Y+1
    x_train.append(x_train_temp2)
    y_train.append(y_train_temp2)
    x_train_temp2 = []
    y_train_temp2 = []  
    
       
for i in range(0,NUMBER_OF_TOTAL_BOARDS):
    x_train[i], y_train[i] = np.array(x_train[i]), np.array(y_train[i])
    print(x_train[i].shape)
    print(y_train[i].shape)


model = Sequential()


model.add(LSTM(units = 128 ,input_shape = (x_train[0].shape[2],x_train[0].shape[3]) ,  return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units = 128 ,input_shape = (x_train[0].shape[2],x_train[0].shape[3]) ,  return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units = 128 ,input_shape = (x_train[0].shape[2],x_train[0].shape[3]) ,  return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units = 128 ,input_shape = (x_train[0].shape[2],x_train[0].shape[3]) ))
model.add(Dropout(0.2))

# Adding the output layer
   
model.add(Dense(units = 5))

model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])

for i in range(0,NUMBER_OF_TOTAL_BOARDS):
    for j in range(0,TOTAL_NUMBER_OF_SCENEARIOS):
        history = model.fit(x_train[i][j], y_train[i][j], epochs=1)


x_input = np.zeros((81,), dtype=int)
SIZE_X = 3
SIZE_Y = 3

createBoard(x_input)

print(x_input)

move(x_input,'L')
move(x_input,'L')

x_input = x_input.reshape((1, 1, 81))

print(x_input)

yhat = model.predict(x_input, verbose=0)
print(yhat)

x_input = x_input.reshape((81,))
#left doesnt work
move(x_input,'R')

print(x_input)
x_input = x_input.reshape((1, 1, 81))
yhat = model.predict(x_input, verbose=0)
print(yhat)

