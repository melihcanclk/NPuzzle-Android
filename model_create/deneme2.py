import numpy as np
import random
from tensorflow.keras.models import load_model

lastmove = 'S'

holdSpace = []
moves = ['L', 'R', 'U', 'D']
def index(board, x,y):
    return (y * 9) + x

def predictNext(model,x_input,size_x,size_y):
    yhat = model.predict(x_input, verbose=0)
    value = 1
    absolute_val_array = np.abs(yhat[0] - value)
    smallest_difference_index = absolute_val_array.argmin()
    if(smallest_difference_index == 4):
        if(not isSolved(x_input[0][0],size_x,size_y)):
            createRandomMove(x_input[0][0],lastmove)
    return smallest_difference_index

def isSolved(board,size_x,size_y):
    counter = 1
    for i in range(0,size_y):
        for j in range (0,size_x):
            if(board[index(board,j,i)] != counter):
                if(j == size_x -1 and i == size_y - 1):
                    return True
                return False
            counter += 1
                
            
    
    return True
def reverse(direction):
    if direction == 'R':
        return 'L'
    elif direction == 'L':
        return 'R'
    elif direction == 'U':
        return 'D'
    elif direction == 'D':
        return 'U'

def isAvailableMove(x,direction):
    #print(holdSpace,SIZE_X,SIZE_Y)
    
    if reverse(direction) == lastmove:
        return False
    elif (direction == 'R' and holdSpace[0] +1 < SIZE_X ) or (direction == 'L' and holdSpace[0] -1 >= 0) or (direction == 'U' and holdSpace[1] -1 >= 0) or (direction == 'D' and holdSpace[1] +1 < SIZE_Y):
        return True
    else:
        return False

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

def createRandomMove(x_input,lastmove):
    randomMove = random.choice(moves)
    while not isAvailableMove(x_input,randomMove) :
        randomMove = random.choice(moves)
    move(x_input,randomMove)
    return randomMove


x_input = np.zeros((81,), dtype=int)
SIZE_X = 3
SIZE_Y = 3

model = load_model('model_%s.h5' % ( str(SIZE_X) + 'x' + str(SIZE_Y)))

x_input= np.empty(81, dtype=int)
x_input.fill(0)
createBoard(x_input)

randomMove = random.choice(moves)

for i in range(0,SIZE_X * SIZE_Y):
    lastmove = createRandomMove(x_input,lastmove)

counter = 0
lastmove = 'S'
while not isSolved(x_input,SIZE_X,SIZE_Y):
    x_input = x_input.reshape((1, 1, 81))

    print(x_input)

    result = predictNext(model,x_input,SIZE_X,SIZE_Y)
    x_input = x_input.reshape((81,))
    '''if moves[result] == reverse(lastmove):
        if counter == 1:

            randomMove = random.choice(moves)
            while not isAvailableMove(x_input,randomMove) :
                randomMove = random.choice(moves)
            move(x_input,randomMove)
            lastmove = randomMove 
            counter = 0
        else:
            counter +=1
            move(x_input,moves[result])
            lastmove = moves[result]
    else:
    #left doesnt work'''
    move(x_input,moves[result])
    lastmove = moves[result]    
print(x_input)
