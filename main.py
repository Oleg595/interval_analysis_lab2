import math
from copy import copy
from sympy import Interval
import matplotlib.pyplot as plt
import matplotlib.patches as pth

def sum(i1, i2):
    min = i1.inf + i2.inf
    max = i1.sup + i2.sup
    return Interval(min, max)

def sub(i1, i2):
    min = i1.inf - i2.sup
    max = i1.sup - i2.inf
    return Interval(min, max)

def mul(i1, i2):
    first_data = [i1.inf, i1.sup]
    second_data = [i2.inf, i2.sup]
    muls = []
    for first in first_data:
        for second in second_data:
            muls.append(first * second)
    return Interval(min(muls), max(muls))

def div(i1, i2):
    first_data = [i1.inf, i1.sup]
    second_data = [i2.inf, i2.sup]
    divs = []
    for first in first_data:
        for second in second_data:
            divs.append(first / second)
    return Interval(min(divs), max(divs))

def sum_matrix(A, B):
    result = copy(A)
    for i in range(len(result)):
        result[i] = sum(result[i], B[i])
    return result

def mul_matrix(A, B):
    result = []
    for i in range(len(A[0])):
        for j in range(1):
            result.append(Interval(.0, .0))
            for q in range(len(B)):
                result[i] = sum(result[i], mul(A[j][q], B[q]))
    return result

def deletePart(newX, oldX):
    result = []
    for i in range(len(newX)):
        result.append(Interval(max([newX[i].inf, oldX[i].inf]), min([newX[i].sup, oldX[i].sup])))
    return result

def equal(newX, oldX):
    eps = 10 ** -16
    for i in range(len(newX)):
        if math.fabs(newX[i].inf - oldX[i].inf) > eps ** -10 or math.fabs(newX[i].sup - oldX[i].sup) > eps:
            return False
    return True

def vizualization(iterations):
    fig, ax = plt.subplots()
    for elem in iterations:
        ax.add_patch(pth.Rectangle((elem[0].inf, elem[1].inf), (elem[0].sup - elem[0].inf), (elem[1].sup - elem[1].inf), linewidth=1, edgecolor='r',  facecolor='none'))
    start_iter = iterations[0]
    x_min = float(start_iter[0].inf - 0.1)
    x_max = float(start_iter[0].sup + 0.1)
    y_min = float(start_iter[1].inf - 0.1)
    y_max = float(start_iter[1].sup + 0.1)
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def plotRadius(iterations):
    rads = []
    iter = []
    for i in range(len(iterations)):
        iter.append(i)
        x = (iterations[i][0].sup - iterations[i][0].inf) / 2
        y = (iterations[i][1].sup - iterations[i][1].inf) / 2
        rads.append(math.log(math.sqrt(x ** 2 + y ** 2)))
    plt.ylabel('log(радиус)')
    plt.xlabel('итерация')
    plt.plot(iter, rads)
    plt.show()

def plotDistance(iterations):
    answer = [1.5, 0]
    distances = []
    iters = []
    for i in range(len(iterations)):
        iters.append(i)
        x = (iterations[i][0].sup + iterations[i][0].inf) / 2 - answer[0]
        y = (iterations[i][1].sup + iterations[i][1].inf) / 2 - answer[1]
        distances.append((math.sqrt(x ** 2 + y ** 2)))
    plt.ylabel('Расстояние')
    plt.xlabel('Итерация')
    plt.plot(iters, distances)
    plt.show()

A = [[Interval(0, 0), Interval(-.25, .25)], [Interval(.0, .0), Interval(-.375, .375)]] #I - VA
B = [Interval(1, 2), Interval(.0, .0)] #VB
oldX = [Interval(-3.2, 3.2), Interval(-3.2, 3.2)]
newX = deletePart(sum_matrix(B, mul_matrix(A, oldX)), oldX)
iterations = [oldX, newX]
while not equal(newX, oldX):
   oldX = copy(newX)
   newX = deletePart(sum_matrix(B, mul_matrix(A, oldX)), oldX)
   iterations.append(newX)
vizualization(iterations)
plotRadius(iterations)
plotDistance(iterations)
