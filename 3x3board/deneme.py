import numpy as np
import random

moves = ['L', 'R', 'U', 'D']

def move(x, direction):
    if direction == 'R':
        x[holdSpace[1]][holdSpace[0]], x[holdSpace[1]][holdSpace[0]+1] =  x[holdSpace[1]][holdSpace[0]+1], x[holdSpace[1]][holdSpace[0]]
        holdSpace[0] = holdSpace[0]+1
    elif direction == 'L':
        x[holdSpace[1]][holdSpace[0]], x[holdSpace[1]][holdSpace[0]-1] =  x[holdSpace[1]][holdSpace[0]-1], x[holdSpace[1]][holdSpace[0]]
        holdSpace[0] = holdSpace[0]-1
    elif direction == 'U':
        x[holdSpace[1]][holdSpace[0]], x[holdSpace[1]-1][holdSpace[0]] =  x[holdSpace[1]-1][holdSpace[0]], x[holdSpace[1]][holdSpace[0]]
        holdSpace[1] = holdSpace[1]-1
    elif direction == 'D':
        x[holdSpace[1]][holdSpace[0]], x[holdSpace[1]+1][holdSpace[0]] =  x[holdSpace[1]+1][holdSpace[0]], x[holdSpace[1]][holdSpace[0]]
        holdSpace[1] = holdSpace[1]+1

def isAvailableMove(x,direction):
    if (direction == 'R' and holdSpace[0] +1 < 3 ) or (direction == 'L' and holdSpace[0] -1 >= 0) or (direction == 'U' and holdSpace[1] -1 >= 0) or (direction == 'D' and holdSpace[1] +1 < 3):
        return True
    else:
        return False


holdSpace = [2,2]

arr = []

x =  np.arange(1, 10).reshape(3,3)
x[2,2] = -1

i=0
arr.append(x)
y=x.copy()

while i<100:
    randomMove = random.choice(moves)
    while not isAvailableMove(x,randomMove) :
        randomMove = random.choice(moves)
    move(y,randomMove)
    arr.append(y.copy())
    i = i+1

print(np.array(arr))



