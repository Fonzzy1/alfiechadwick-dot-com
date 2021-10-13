import math
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import pandas as pd

## Condition such that [h,x,f(x),f'(x) .... f^n(x)] in a row
condition_vect = np.array([[0.01, 0, np.nan, np.nan]])

matrix_transform = np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, -2, 0, 0]])
xmin = 0
xmax = 4
## Condition Vector



class LinODE:
    def __init__(self, condition_vect, matrix_transform, xmin, xmax, itterations):
        self.condition_vect = condition_vect
        self.matrix_transform = matrix_transform
        self.xmin = xmin
        self.xmax = xmax
        self.search_min = -1000
        self.search_max = 1000
        self.search_step = 100

        self.wellposed = np.NaN
        self.known_conditions = []

        self.output = np.NaN
        self.dist = np.NaN

        self.best_int_vect = np.NaN
        self.best_dist = np.NaN

        self.find_best_aprox()

        i = 0
        while i<= itterations:
            self.refine_aprox()
            i+=1
        self.check_well_posedness()

    def check_well_posedness(self):
        known_conditions = []
        for vect in self.condition_vect:
            k = 0
            for value in vect[2:len(vect)]:
                if not np.isnan(value):
                    known_conditions.append([vect[1], k, value])
                k += 1

        for vect in self.condition_vect:
            i = 0
            vect_transformed = np.full((len(vect), 1), np.nan)
            for i in range(0, len(vect_transformed)):
                mults = []
                for j in range(0, len(vect_transformed)):
                    if self.matrix_transform[i][j] != 0:
                        mults.append(self.matrix_transform[i][j] * vect[j])
                vect_transformed[i] = sum(mults)
            k = 0
            for value in vect_transformed[2:len(vect)]:
                if not np.isnan(value):
                    known_conditions.append([vect[1], k, value[0]])
                k += 1


        ## Remove Duplicates
        known_conditions = np.unique(known_conditions, axis=0)

        ##Find if value is defined twice differently
        range_of_def = []
        for i in known_conditions:
            range_of_def.append(i[0:2])
        if len(range_of_def) != len(np.unique(range_of_def, axis=0)):
            (self.wellposed, self.known_conditions) = (False, known_conditions)
        elif len(known_conditions) == len(condition_vect[0]) - 2:
            (self.wellposed, self.known_conditions) = (True, known_conditions)

    def lin_IVP(self, vect_initial):

        h = vect_initial[0][0]

        # Build the Stepping matrices
        matrix_step_neg = self.build_matrix_step(-1)
        matrix_step_pos = self.build_matrix_step(1)

        ## Create df_output Space

        df_output = pd.DataFrame(vect_initial.T)

        ## Do the positive steps first
        vect = vect_initial.copy()
        while vect[1][0] <= self.xmax:
            vect = np.matmul(matrix_step_pos, vect)
            df_output.loc[len(df_output)] = vect.T[0]

        ## Do the negative steps next
        vect = vect_initial.copy()
        while vect[1][0] > self.xmin:
            vect = np.matmul(matrix_step_neg, vect)
            df_output.loc[len(df_output)] = vect.T[0]

        # Reprder
        df_output.sort_values(1, inplace=True)

        return df_output

    def single_value_lin_IVP(self, x, initial_vect):
        h = initial_vect[0]

        # Build the Stepping matrices
        matrix_step_neg = self.build_matrix_step(1)
        matrix_step_pos = self.build_matrix_step(-1)

        k = int((x - initial_vect[1]) / h)

        if k > 0:
            step_matrix_k = np.linalg.matrix_power(matrix_step_pos, k)
            vect_output = np.matmul(step_matrix_k, initial_vect)
        if k < 0:
            step_matrix_k = np.linalg.matrix_power(matrix_step_neg, -k)
            vect_output = np.matmul(step_matrix_k, initial_vect)
        if k == 0:
            vect_output = initial_vect

        return vect_output

    def build_matrix_step(self, mult):
        h = mult * self.condition_vect[0][0]
        matrix_base = np.identity(len(matrix_transform))
        matrix_base[1][0] = np.sign(mult)
        for i in range(2, len(matrix_base)):
            for j in range(i, len(matrix_base)):
                matrix_base[i][j] = h ** (j - i) / math.factorial(j - i)
        matrix_step = np.matmul(matrix_transform, matrix_base)
        return matrix_step

    def find_best_aprox(self):
        # Find All Possible initial vectors
        search_permutations = [
            *it.combinations_with_replacement(np.arange(self.search_min,self.search_max + self.search_step, self.search_step),
                                              np.count_nonzero(np.isnan(self.condition_vect[0].T)))]
        nan_location = np.argwhere(np.isnan(self.condition_vect[0].T))
        nan_location = nan_location[nan_location != 0]
        vect_initial_poss = np.zeros((len(search_permutations), len(self.condition_vect[0].T)))
        for i in range(0, len(search_permutations)):
            vect_initial_poss[i] = self.condition_vect[0].T
            vect_initial_poss[i][nan_location] = search_permutations[i]
            ## This ensures only valid input vectors are met
            vect_initial_poss[i] = np.matmul(self.matrix_transform, vect_initial_poss[i].T)

        ## List of scores
        ls_distance = []

        # Run over range of possible vectors
        for vect_initial in vect_initial_poss:
            ls_distance_single = []
            for vect in condition_vect:
                output = self.single_value_lin_IVP(vect[1],vect_initial)
                dist = np.linalg.norm(np.nan_to_num(output - vect))
                ls_distance_single.append(dist)
            ls_distance.append(sum(ls_distance_single))

        df_results = pd.DataFrame(vect_initial_poss)
        df_results['dist'] = ls_distance

        best_index = df_results[['dist']].idxmin()

        best_int_vect = vect_initial_poss[best_index].T
        dist = df_results['dist'][best_index].values


        self.best_int_vect = best_int_vect
        self.best_dist = dist
        self.dist = df_results

        self.output = self.lin_IVP(best_int_vect)

    def refine_aprox(self):

        nan_location = np.argwhere(np.isnan(self.condition_vect[0].T))
        nan_location = nan_location[nan_location != 0]
        if nan_location.size != 0:
            self.search_max = max(self.best_int_vect[nan_location])+self.search_step
            self.search_min = min(self.best_int_vect[nan_location])-+self.search_step
            self.search_step = (self.search_max-self.search_min)/20
        self.find_best_aprox()





    def plot(self, all = False):
            plt.plot(self.output[1],self.output[2])
            legend = ['f(x)']
            if all:

                for i in np.arange(3,len(self.output.T)):
                    plt.plot(self.output[1],self.output[i])
                    legend.append('f'+(i-2)*'\'' + '(x)')
            plt.legend(legend)
            plt.show()


sim = LinODE(condition_vect, matrix_transform, xmin, xmax,0)

