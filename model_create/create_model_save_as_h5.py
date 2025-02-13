import numpy as np
import random
import os
import math

# Importing the Keras libraries and packages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import load_model

TRYTIME = 10

TOTAL_NUMBER_OF_SCENEARIOS = 100

SIZE_X = 5
MAX_X = 5

SIZE_Y = 9
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

k=0

record = 0

for k in range(0,NUMBER_OF_TOTAL_BOARDS):
    j = 0
    
    TRYTIME = 20
    print(SIZE_X,SIZE_Y, TRYTIME)
    for j in range(0,TOTAL_NUMBER_OF_SCENEARIOS):
        print(j)
        SIZE = SIZE_X * SIZE_Y
        X = np.empty(81, dtype=int)
        X.fill(0)
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
        #delete last item
        arrOfSeq = arrOfSeq[:-1]
        arrOfSeq = np.array(arrOfSeq)
        filename = 'x_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j) + '.npz'
        np.savez_compressed(filename, input=arrOfSeq)
        #del arrOfSeq
        holdSpace = []
        j=j+1

        y_train = []
        
        filename = 'x_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j-1) + '.npz'
        loaded = np.load(filename)
        lastmove = 'S'
        for i in range(1, TRYTIME):
            y_train.append(recognizeMovement(loaded['input'][i-1],loaded['input'][i]))
            
        X = np.empty(81, dtype=int)
        X.fill(0)
        createBoard(X)
        move(X,'U')
        Y = loaded['input'][i]
        if np.array_equal(X,Y):
            y_train.append([0,-1,0,1])
        move(X,'D')
        move(X,'L')
        if np.array_equal(X,Y):
            y_train.append([0,1,0,-1])
        
        filename = 'y_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j-1)
        np.savez_compressed(filename, input=y_train)
        del y_train

    #add this end of the creation of all models

    model = Sequential()

    model.add(LSTM(units = TRYTIME ,input_shape = (1,81) ,  return_sequences=True))
    Dropout(0.2)
    
    model.add(LSTM(units = TRYTIME ,input_shape = (1,81)  ))
    Dropout(0.2)
    
    # Adding the output layer

    model.add(Dense(units = 4, activation='softmax'))

    model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])

    total_x = []
    total_y = []
    for j in range(0,TOTAL_NUMBER_OF_SCENEARIOS):
        filename1 = 'x_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j) + '.npz'
        filename2 = 'y_input_' + str(SIZE_X) + 'x' + str(SIZE_Y) + '_' + str(j) + '.npz'
        x_input = np.load(filename1)
        y_input = np.load(filename2)
        x_input = x_input['input'].reshape(-1,1,81)
        y_input = y_input['input']
        for i in range(0,TRYTIME):
            total_x.append(x_input[i])
            total_y.append(y_input[i])
        
    total_x = np.array(total_x)
    total_y = np.array(total_y)

    train_size = int(len(total_x) * 0.8)
    train_x, test_x = total_x[0:train_size], total_x[train_size:len(total_x)]
    train_y, test_y = total_y[0:train_size], total_y[train_size:len(total_y)]
    print(train_x.shape)
    print(test_x.shape)
    print(train_y.shape)
    print(test_y.shape)
    history = model.fit(train_x, train_y, batch_size=128, epochs=10,validation_data=(test_x,test_y))
    
    filename = 'model_%s.h5' % (str(SIZE_X) + 'x' + str(SIZE_Y))
    model.save(filename)

    model = load_model(filename)
    model.evaluate(test_x, test_y)
    deleteFiles(SIZE_X,SIZE_Y)
    
    SIZE_X = SIZE_X+1
    k = k+1
    if SIZE_X == MAX_X + 1:
        SIZE_X=3
        SIZE_Y=SIZE_Y+1
