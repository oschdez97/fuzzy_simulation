from fuzzy_set import FuzzySet

class FuzzyVariable():
    def __init__(self, min, max, res, name=''):
        self.sets = {}
        self.res = res
        self.min = min
        self.max = max
        self.name = name

    def add_set(self, name, f_set):
        self.sets[name] = f_set

    def get_set(self, name):
        return self.sets[name]

    def get_sets_names(self):
        return list(self.sets.keys())

    def add_triangular(self, name, a, b, c):
        triang = FuzzySet.create_triangular(self.min, self.max, self.res, a, b, c, name)
        self.add_set(name, triang)
        return triang

    def add_trapezoid(self, name, a, b, c, d):
        trapezoid = FuzzySet.create_trapezoidal(self.min, self.max, self.res, a, b, c, d, name)
        self.add_set(name, trapezoid)
        return trapezoid