import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#1
def c(vector, n ):
    if n == 0:
        return vector[1]
    if n== 1:
        return  vector[2]
    if n == 2:
        return -(vector[0] * vector[2] + vector[0]**2 * vector[1])/(vector[0]**2)


    return vector[1]
int_vector = [1,2,0]

#2
depth = 10
step = 0.01
d_min = 0.01
d_max = 10

#2.1 Set up output space
d_min_scale  = int(round(d_min / step))
d_max_scale = int(round(d_max / step))
ls_points = list(range(d_min_scale, d_max_scale))
ls_points = list(map(lambda x: x*step, ls_points))
df = pd.DataFrame(ls_points, columns=['Point'])
df['Value'] = 0
df.set_index('Point', inplace=True)


#2.2 Set up n list
ls_n = list(range(0,depth))

#3
def point(step, vector, ls_n, derivative):
    ls_point_term = []
    for n in ls_n:
        coefficient =  c(vector, n + derivative)
        point = coefficient / math.factorial(n) * step ** n
        ls_point_term.append(point)
    point_value = sum(ls_point_term)
    return point_value



point_vector = int_vector.copy()

while point_vector[0] <= d_max :
    try:
        point_values = []
        for d in range(0 , len(point_vector)- 1 ):
            value = point(step, point_vector, ls_n, d)
            point_values.append(value)

        location = df.index.get_loc(point_vector[0], method= 'nearest')
        df.iloc[location,0] = point_values[0]
        point_vector[0] += step
        point_vector[1:len(point_vector)]  = point_values
    except OverflowError:
        break
    except ZeroDivisionError:
        point_vector[0] += step


point_vector = int_vector.copy()

while point_vector[0] > d_min - step :
    try:
        point_values = []
        for d in range(0 , len(point_vector) - 1):
            value = point(-step, point_vector, ls_n, d)
            point_values.append(value)

        location = df.index.get_loc(point_vector[0], method= 'nearest')
        df.iloc[location,0] = point_values[0]
        point_vector[0] -= step
        point_vector[1:len(point_vector)] = point_values
    except OverflowError:
        break
    except ZeroDivisionError:
        point_vector[0] -= step
df.plot()

plt.show()