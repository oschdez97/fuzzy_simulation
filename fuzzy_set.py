import copy
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from fuzzy_system import PRECISION

class FuzzySet():
    def __init__(self, name=''):
        self.elems = {}
        self.name  = name

    def add_element(self, x, y):
        if y > 1:
            raise ValueError('Degree of membership must not be greater than 1')
        if x in self.elems:
            self.elems[x] = max(self.elems[x], y)
        else:
            self.elems[x] = y

    def sort_set(self):
        self.elems = OrderedDict(sorted(self.elems.items()))

    def eval(self, x):
        if self.membership_type == 'triangular':
            return self.eval_triangular(self.params[0], self.params[1], self.params[2], x)
        elif self.membership_type == 'trapezoidal':
            return self.eval_trapezoidal(self.params[0], self.params[1], self.params[2], self.params[3], x)
        elif self.membership_type == 'agg':
            return self.eval_agg(x)
        else:
            raise('A membership function must be defined')
    
    def eval_agg(self, x):
        if self.elems.__contains__(x):
            return self.elems[x]

        d = 10e6
        id = -1
        for i, v in enumerate(list(self.elems.keys())):
            c_d = abs(v - x)
            if c_d < d:
                d = c_d
                id = v
        return self.elems[id]


    def eval_triangular(self, a, b, c, x):
        if x <= a or x >= c:
            return 0
        elif a < x <= b:
            return round((x-a)/(b-a), PRECISION)
        elif b < x <= c:
            return round((c-x)/(c-b), PRECISION)

    def eval_trapezoidal(self, a, b, c, d, x):
        if x <= a or x > d:
            return 0
        elif a < x <= b:
            return round((x-a)/(b-a), PRECISION)
        elif b < x <= c:
            return 1
        elif c < x <= d:
            return round((d-x)/(d-c), PRECISION)

    @classmethod
    def create_triangular(cls, g_min, g_max, g_res, a, b, c, name):
        if not (a < b < c):
            raise Exception('Error in triangular set definition')
        
        f_set = cls(name)
        f_set.params = [a, b, c]
        f_set.membership_type = 'triangular'
        for i in np.round(np.linspace(g_min, g_max, g_res), PRECISION):
            y = f_set.eval_triangular(a, b, c, i)
            f_set.add_element(i, y)
        return f_set

    @classmethod
    def create_trapezoidal(cls, g_min, g_max, g_res, a, b, c, d, name):
        if not (a <= b < c <= d):
            raise Exception('Error in trapezoidal set definition')
        
        f_set = cls(name)
        f_set.params = [a, b, c, d]
        f_set.membership_type = 'trapezoidal'
        for i in np.round(np.linspace(g_min, g_max, g_res), PRECISION):
            y = f_set.eval_trapezoidal(a, b, c, d, i)
            f_set.add_element(i, y)
        return f_set

    def union(self, f_set):
        result = copy.deepcopy(f_set)
        for x, u in self.elems.items():
            if x in result.elems:
                result[x] = max(result[x], u)
            else:
                result.add_element(x, u)
        result.sort_set()
        return result

    def intersection(self, f_set):
        result = copy.deepcopy(f_set)
        for x, u in self.elems.items():
            if x in result.elems:
                result[x] = min(result[x], u)
            else:
                result.add_element(x, u)
        result.sort_set()
        return result

    def complement(self):
        result = copy.deepcopy(self)
        for x, u in self.elems.items():
            result[x] = 1 - u
        result.sort_set()
        return result

    def fuzzy_cut(self, val):
        res_set = FuzzySet()
        for x, u in self.elems.items():
            if u > val:
                res_set.add_element(x, val)
            else:
                res_set.add_element(x, u)
        return res_set

    def fuzzy_alpha_degree(self, val):
        res_set = FuzzySet()
        for x, u in self.elems.items():
            res_set.add_element(x, u*val)
        return res_set

    def __getitem__(self, x):
        y = 0
        if x in self.elems:
            y = self.elems[x]
        return y

    def __setitem__(self, x, y):
        if x in self.elems:
            self.elems[x] = y

    def plot(self):
        plt.plot(self.elems.keys(), self.elems.values())
        plt.show()

if __name__ == '__main__':
    triang = FuzzySet.create_triangular(0, 40, 100, 15, 25, 35, 'medium')
    trapez = FuzzySet.create_trapezoidal(20, 100, 100, 30, 50, 70, 90, 'wet')
    
    print(triang.elems)
    print(trapez.elems)
    
    print(triang.eval(16))

    uni = triang.union(trapez)
    int = triang.intersection(trapez)
    cut = triang.fuzzy_cut(0.4)

    plt.plot(triang.elems.keys(), triang.elems.values())
    plt.plot(trapez.elems.keys(), trapez.elems.values())
    plt.show()

    