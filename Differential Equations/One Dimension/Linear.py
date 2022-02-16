import math
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import pandas as pd

## Condition such that [h,x,f(x),f'(x) .... f^n(x)] in a row
condition_vector = np.array([[0.1, 0, 1, np.nan,-2], [0.1, 2, 1, np.nan,np.nan]])

transformation_matrix = np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, -2, 0, 0]])
xmin = 0
xmax = 4

def identity(x):
    return x

def nan_matrix_mult(A,x):
    y = np.full((len(x), 1), np.nan)
    for i in range(0, len(y)):
        mults = []
        for j in range(0, len(y)):
            if A[i][j] != 0:
                mults.append(A[i][j] * x[j])
        y[i] = sum(mults)
    return y


class ODE:
    def __init__(self, condition_vect, matrix_transform=False, nonlin_transform_function=False, xmin=False, xmax=False, itterations=10):

        self.condition_vect = condition_vect
        if matrix_transform.all() == False:
            self.matrix_transform = np.identity(len(condition_vect[0]))
        else:
            self.matrix_transform = matrix_transform
        
        if nonlin_transform_function == False:
            self.func = identity
            self.fast_search = True
        else:
            self.func = nonlin_transform_function
            self.fast_search = False

        if xmin == False:
            self.xmin = min(condition_vect.T[1])
        else:
            self.xmin = xmin

        if xmax == False:
            self.xmax = max(condition_vect.T[1])
        else:
            self.xmax = xmax
        self.itterations = itterations
        self.conditions = self.seperate_conditions()

        self.initial_vect = self.annealing()
        self.output = self.build_set()
    def seperate_conditions(self):
        # Initialise an empty Array
        known_conditions = [ ] 
        #Take all obvious values
        for vect in self.condition_vect:
            k = 0
            #If not NaN, then it provides information
            for value in vect[2:len(vect)]:
                if not np.isnan(value):
                    known_conditions.append([vect[1], k, value])
                k += 1

        #Apply the transform to enxure that other conditions are met
        for vect in self.condition_vect:
            i = 0
            #Had to redefine matrix multiplcation so that 0*nan is 0
            vect_transformed = np.full((len(vect), 1), np.nan)
            for i in range(0, len(vect_transformed)):
                mults = []
                for j in range(0, len(vect_transformed)):
                    if self.matrix_transform[i][j] != 0:
                        mults.append(self.matrix_transform[i][j] * vect[j])
                vect_transformed[i] = sum(mults)
            #Apply the transform function
            vect_transformed = self.func(nan_matrix_mult(self.matrix_transform, vect))
            k = 0
            for value in vect_transformed[2:len(vect)]:
                if not np.isnan(value):
                    known_conditions.append([vect[1], k, value[0]])
                k += 1


        ## Remove Duplicates
        known_conditions = np.unique(known_conditions, axis=0)
        return known_conditions

    def build_matrix_step(self, sign):
        h = sign * self.condition_vect[0][0]
        matrix_base = np.identity(len(self.matrix_transform))
        matrix_base[1][0] = np.sign(sign)
        for i in range(2, len(matrix_base)):
            for j in range(i, len(matrix_base)):
                matrix_base[i][j] = h ** (j - i) / math.factorial(j - i)
        matrix_step = np.matmul(self.matrix_transform, matrix_base)
        return matrix_step

    def step(self, vect, sign):
        step_matrix = self.build_matrix_step(sign)
        new_vect = self.func(np.matmul(step_matrix,vect))
        return new_vect


    def mult_step(self,steps,vect):
        if steps == 0:
            return vect

        if steps > 0 :
            i = 0
            while i < steps:
                vect = self.step(vect,1)
                i += 1
            return vect
                
        if steps < 0:
            i = 0
            while i < steps:
                vect = self.step(vect,-1)
                i += 1
            return vect

    def mult_step_lin(self,steps,vect):
        if steps == 0:
            return vect

        if steps > 0 :
            step_matrix = self.build_matrix_step(1)
            return np.matmul(np.linalg.matrix_power(step_matrix,steps),vect)
                
        if steps < 0:
            step_matrix = self.build_matrix_step(-1)
            return np.matmul(np.linalg.matrix_power(step_matrix,steps),vect)



    def annealing(self):
        i  = np.argmin([(np.isnan(self.func(np.matmul(self.matrix_transform,vect.T)))) for vect in self.condition_vect])
        initial_vect =   self.func(nan_matrix_mult(self.matrix_transform,self.condition_vect[i].T))
        index = [i for i,x in enumerate(initial_vect) if np.isnan(x)] 
        initial_vect = np.nan_to_num(initial_vect)
        for mag in range(5,5-self.itterations,-1):
            search_step = 10**mag
            initial_vect = self.annealing_step(initial_vect,index,search_step)

        return  initial_vect

        

    def annealing_step(self,initial_vector,where,search_step):
        ## Create a set of all possible initial vectors 
        mods =  list(it.product(np.arange(-10,11), repeat=len(where)))
        dists = []
        vects = []
        for i  in mods:
            trial_dist = []
            trial_vect = initial_vector.copy()
            for j,k in enumerate(where):
                trial_vect[k] += search_step * i[j]
            for c in self.conditions:
                x_goal = c[0]
                x_initial = trial_vect[1][0]
                h = trial_vect[0][0]
                steps = round((x_goal-x_initial)/h)
                if self.fast_search:
                    y_goal = self.mult_step_lin(steps,trial_vect)
                else:
                    y_goal = self.mult_step(steps,trial_vect)
                trial_dist.append(abs(y_goal[int((c[1]+2))] - c[2]))
            dists.append(sum(trial_dist))
            vects.append(trial_vect)
        return vects[np.argmin(dists)]

    def build_set(self):
        output = np.zeros(shape = (round((self.xmax-self.xmin)/self.initial_vect[0][0])+1,len(self.initial_vect)))
        #find index of self.initial_vect
        index = round((self.initial_vect[1][0] - self.xmin)/self.initial_vect[0][0])
        output[index] = self.initial_vect.T
        ## Do backwords steps
        k = 1
        while k <= index:
            output[index - k] = self.step(output[index - k + 1].T, -1).T
            k += 1
        ## Do forwards
        k = 1
        while k < len(output) - index:
            output[index + k] = self.step(output[index +  k - 1].T, 1).T
            k += 1
        return output

print(ODE(condition_vector, transformation_matrix,itterations = 10).build_set())
def f(vect):
    vect[4] = vect[2]**2 -3
    return vect

print(ODE(condition_vector, transformation_matrix,f,itterations = 10).build_set())

