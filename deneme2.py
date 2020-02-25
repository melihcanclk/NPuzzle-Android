import numpy as np
from tensorflow.keras.models import load_model

holdSpace = []

def index(board, x,y):
    return (y * 9) + x


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
x_input = np.zeros((81,), dtype=int)
SIZE_X = 3
SIZE_Y = 3

createBoard(x_input)

print(x_input)

move(x_input,'U')
move(x_input,'L')
move(x_input,'U')

x_input = x_input.reshape((1, 1, 81))

print(x_input)
model = load_model('model_%s.h5' % ( str(SIZE_X) + 'x' + str(SIZE_Y)))

yhat = model.predict(x_input, verbose=0)
print(yhat)

x_input = x_input.reshape((81,))
#left doesnt work
move(x_input,'R')

print(x_input)
x_input = x_input.reshape((1, 1, 81))
yhat = model.predict(x_input, verbose=0)
print(yhat)

