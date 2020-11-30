import copy
import numpy as np
import matplotlib.pyplot as plt

PRECISION = 8

class FuzzySystem():
    def __init__(self):
        self.rules = []
        self.input_variables  = {}
        self.output_variables = {}

    def add_input_variable(self, f_var):
        self.input_variables[f_var.name] = f_var

    def add_output_variable(self, f_var):
        self.output_variables[f_var.name] = f_var

    def get_input_variable(self, name):
        return self.input_variables[name]

    def get_output_variable(self, name):
        return self.output_variables[name]
    
    def add_rules(self, rules):
        self.rules = rules

    def get_evaluations(self, f_set, val):
        x = []
        y = []
        for i in np.linspace(0, f_set.eval(val), 1000):
            x.append(val)
            y.append(i)
        return x, y        

    def plot_system(self, solution):
        centroide = self.centroide(solution)
        bisectriz = self.bisectriz(solution)
        media_max = self.media_max(solution)
        
        try:
            fig = plt.figure(figsize=(8, 8))
            color_idx = 0
            colors = ['red', 'green', 'blue', 'orange', 'gray', 'purple', 'yellow', 'black', 'pink']
            
            rows = len(self.input_variables) + len(self.output_variables) + 1

            for i, var_name in enumerate(self.input_variables):
                var = self.get_input_variable(var_name)
                ax  = plt.subplot(rows, 1, i+1)
                for set_name in var.get_sets_names():
                    set = var.get_set(set_name)
                    ax.plot(set.elems.keys(), set.elems.values(), color=colors[color_idx], label=set_name)
                    color_idx += 1
                if var_name == 'Edad':
                    ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title=var_name, frameon=False)
                else:
                    ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title='Porciento de ' + var_name, frameon=False)

            color_idx = 0
            for i, var_name in enumerate(self.output_variables):
                var = self.get_output_variable(var_name)
                ax = plt.subplot(rows, 1, len(self.input_variables)+i+1)
                for set_name in var.get_sets_names():
                    set = var.get_set(set_name)
                    ax.plot(set.elems.keys(), set.elems.values(), color=colors[color_idx], label=set_name)
                    color_idx += 1
                ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title='Riesgo Financiero', frameon=False)

            
            ax = plt.subplot(rows, 1, rows)
            plt.plot(solution.elems.keys(), solution.elems.values(), color='blue', label='Agregación')
            
            
            x_centroide, y_centroide = self.get_evaluations(solution, centroide)
            x_bisectriz, y_bisectriz = self.get_evaluations(solution, bisectriz)
            x_media_max, y_media_max = self.get_evaluations(solution, media_max)
            
            ax.plot(x_centroide, y_centroide, color='red', label='Centroide')
            ax.plot(x_bisectriz, y_bisectriz, color='green', label='Bisector del Área')
            ax.plot(x_media_max, y_media_max, color='purple', label='Media de los Máximos')
            ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title='', frameon=False)
            
            plt.tight_layout()
            plt.show()
        
        except:
            print('Centroide: ' + str(centroide))
            print('Bisector del Área: ' + str(bisectriz))
            print('Media de los Máximos: ' + str(media_max))

    def getArea(self, y, lf, rg):
        res = 0
        for i in range(lf, rg):
            res += y[i]
        return res

    def bisectriz(self, f_set):
        x = list(f_set.elems.keys())
        y = list(f_set.elems.values())
        
        lf = 0
        rg = len(x)

        for _ in range(100):
            m = int((lf + rg) / 2)
            a1 = self.getArea(y, 0, m)
            a2 = self.getArea(y, m, len(x))
            
            if np.fabs(a1 - a2) <  10**-6:
                return m

            if a1 > a2 :
                rg = m

            else:
                lf = m

        return x[m]

    def centroide(self, f_set):
        x = list(f_set.elems.keys())
        y = list(f_set.elems.values())
        
        num = 0
        dem = 0
        for i in range(0,len(x)):
            num += x[i] * y[i]
            dem += y[i] 
    
        return round(num/dem, PRECISION)

    def media_max(self, f_set):
        x = list(f_set.elems.keys())
        y = list(f_set.elems.values())
        
        elems = []
        max = 0
        for i in range(0, len(x)):
            v = y[i]
            if max < v:
                max = v
                elems = [x[i]]
            elif max == v:
                elems.append(x[i])
            else:
                pass
        return round(sum(elems) / len(elems), PRECISION)

    def eval(self, input_values, _method='mamdani'):
        if _method not in ['mamdani', 'larsen']:
            raise('Error in fuzzy method name')
        
        sets = []
        for elem in self.rules:
            rule = elem.split(' ')
            sets.append(self.eval_rule(rule, input_values, _method))
        
        agg = sets[0]
        for i in range(1, len(sets)):
           tmp = agg.union(sets[i])
           agg = copy.deepcopy(tmp)
           agg.membership_type = 'agg'

        return agg

    def eval_rule(self, rule, input_values, _method):
        operands  = []
        operators = []
        for token in rule:
            if token == 'AND' or token == 'OR' or token == 'THEN':
                if len(operators):
                    op = operators.pop()
                    if op == 'OR':
                        if len(operands) == 4:
                            set1_name, var1_name = operands.pop(), operands.pop()
                            set2_name, var2_name = operands.pop(), operands.pop()

                            var1   = self.get_input_variable(var1_name)
                            f_set1 = var1.get_set(set1_name)
                            var2   = self.get_input_variable(var2_name)
                            f_set2 = var2.get_set(set2_name)

                            val = max(f_set1.eval(input_values[var1_name]), f_set2.eval(input_values[var2_name]))
                            operands.append(val)
                            operators.append(token)
                        
                        elif len(operands) == 3:
                            set_name = operands.pop()
                            var_name = operands.pop()
                            cval     = operands.pop()

                            var = self.get_input_variable(var_name)
                            set = var.get_set(var_name)
                            val = max(cval, set.eval(input_values[var_name]))
                            operands.append(val)
                            operators.append(token)
                        
                        else:
                            raise('Bad rule evaluation 3')

                    elif op == 'AND':
                        if len(operands) == 4:
                            set1_name, var1_name = operands.pop(), operands.pop()
                            set2_name, var2_name = operands.pop(), operands.pop()

                            var1   = self.get_input_variable(var1_name)
                            f_set1 = var1.get_set(set1_name)
                            var2   = self.get_input_variable(var2_name)
                            f_set2 = var2.get_set(set2_name)

                            val = min(f_set1.eval(input_values[var1_name]), f_set2.eval(input_values[var2_name]))
                            operands.append(val)
                            operators.append(token)

                    elif len(operands) == 3:
                            set_name = operands.pop()
                            var_name = operands.pop()
                            cval     = operands.pop()

                            var = self.get_input_variable(var_name)
                            set = var.get_set(var_name)
                            val = min(cval, set.eval(input_values[var_name]))
                            operands.append(val)
                            operators.append(token)
                        
                    else:
                        raise('Bad rule evaluation 4')
                else:
                    operators.append(token)
            else:
                operands.append(token)

        if len(operators) and operators[0] == 'THEN':
            if len(operands) == 3:
                operators.pop()
                set_name = operands.pop()
                var_name = operands.pop()
                val      = operands.pop()

                var   = self.get_output_variable(var_name)
                f_set = var.get_set(set_name)
                
                if _method == 'mamdani':
                    return f_set.fuzzy_cut(val)
                else:
                    return f_set.fuzzy_alpha_degree(val)
            
            elif len(operands) == 4:
                operators.pop()
                out_set_name = operands.pop()
                out_var_name = operands.pop()
                in_set_name  = operands.pop()
                in_var_name  = operands.pop()

                in_var = self.get_input_variable(in_var_name)
                in_set = in_var.get_set(in_set_name)
                val    = in_set.eval(input_values[in_var_name])

                out_var = self.get_output_variable(out_var_name)
                out_set = out_var.get_set(out_set_name)
                
                if _method == 'mamdani':
                    return out_set.fuzzy_cut(val)
                else:
                    return out_set.fuzzy_alpha_degree(val)

            else:
                raise('Bad rule evaluation 1') 
        else:
            raise('Bad rule evaluation 2')


