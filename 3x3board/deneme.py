import numpy as np
import random

TRYTIME = 199

lastmove = 'S'

moves = ['L', 'R', 'U', 'D']

def move(x, direction):
    if direction == 'R':
        x[holdSpace[1]*holdSpace[0]], x[holdSpace[1]*holdSpace[0]+1] =  x[holdSpace[1]*holdSpace[0]+1], x[holdSpace[1]*holdSpace[0]]
        holdSpace[0] = holdSpace[0]+1
    elif direction == 'L':
        x[holdSpace[1]*holdSpace[0]], x[holdSpace[1]*holdSpace[0]-1] =  x[holdSpace[1]*holdSpace[0]-1], x[holdSpace[1]*holdSpace[0]]
        holdSpace[0] = holdSpace[0]-1
    elif direction == 'U':
        x[holdSpace[1]*holdSpace[0]], x[holdSpace[1]-1*holdSpace[0]] =  x[holdSpace[1]-1*holdSpace[0]], x[holdSpace[1]*holdSpace[0]]
        holdSpace[1] = holdSpace[1]-1
    elif direction == 'D':
        x[holdSpace[1]*holdSpace[0]], x[holdSpace[1]+1*holdSpace[0]] =  x[holdSpace[1]+1*holdSpace[0]], x[holdSpace[1]*holdSpace[0]]
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

holdSpace = [2,2]

arr = []

j=0
while j<1000:

    x =  np.arange(1, 10).reshape(9)
    x[8] = -1

    i=0
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

    arr.append(arrOfBoards)
    j=j+1

print(np.array(arr).shape)



