import numpy as np
import random
import os

# Importing the Keras libraries and packages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import load_model

TRYTIME = 299

TOTAL_NUMBER_OF_SCENEARIOS = 20000

SIZE_X = 3
MAX_X = 9

SIZE_Y = 3
MAX_Y = 9

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
        x,y = findEmpty(current)
        holdSpace.append(x)
        holdSpace.append(y)
        current_copy = current.copy()
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
    #print(holdSpace,SIZE_X,SIZE_Y)
    
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

def deleteFiles(size_x, size_y):
    for j in range(0,TOTAL_NUMBER_OF_SCENEARIOS):
        filename1 = 'x_input_' + str(size_x) + 'x' + str(size_y) + '_' + str(j) + '.npz'
        filename2 = 'y_input_' + str(size_x) + 'x' + str(size_y) + '_' + str(j) + '.npz'
        os.remove(filename1)
        os.remove(filename2)
        

filaname = ''

arrOfAllBoards = []

arrOfScenearios = []

k=0

for k in range(0,NUMBER_OF_TOTAL_BOARDS):
    j = 0
    print(SIZE_X,SIZE_Y)
    for j in range(0,TOTAL_NUMBER_OF_SCENEARIOS):
        print(j)
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
        filename = 'x_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j) + '.npz'
        np.savez_compressed(filename, input=arrOfSeq)
        holdSpace = []
        j=j+1

        y_train = []
        
        filename = 'x_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j-1) + '.npz'
        loaded = np.load(filename)
        for i in range(1, TRYTIME+2):
            lastmove = 'S'
            if i == TRYTIME+1:
                y_train.append([0, 0, 0, 0,1])
            else:
                y_train.append(recognizeMovement(loaded['input'][i-1],loaded['input'][i]))
        
        filename = 'y_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j-1)
        np.savez_compressed(filename, input=y_train)

    #add this end of the creation of all models

    model = Sequential()

    model.add(LSTM(units = 128 ,input_shape = (1,81) ,  return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units = 128 ,input_shape = (1,81) ,  return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units = 128 ,input_shape = (1,81)  ,  return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units = 128 ,input_shape = (1,81)  ))
    model.add(Dropout(0.2))

    # Adding the output layer

    model.add(Dense(units = 5))

    model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])

    for j in range(0,TOTAL_NUMBER_OF_SCENEARIOS):
        filename1 = 'x_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j) + '.npz'
        filename2 = 'y_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j) + '.npz'
        x_input = np.load(filename1)
        y_input = np.load(filename2)
        x_input = x_input['input'].reshape(-1,1,81)
        y_input = y_input['input']
        history = model.fit(x_input, y_input, epochs=10)

    filename = 'model_%s.h5' % (str(SIZE_X) + 'x' + str(SIZE_Y))
    model.save(filename)
    deleteFiles(SIZE_X,SIZE_Y)
    
    SIZE_X = SIZE_X+1
    k = k+1
    if SIZE_X == MAX_X + 1:
        SIZE_X=3
        SIZE_Y=SIZE_Y+1
