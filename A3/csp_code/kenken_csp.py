#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools

def binary_ne_grid(kenken_grid):
    ##IMPLEMENT
    list_variables = []
    variables=[]
    tuples = []
    row=[]
    col=[]
    N = kenken_grid[0][0]
    csp = CSP("binary_ne_grid")

    setup_variable(csp, N, list_variables, variables, tuples, row, col, "binary")

    check_binary(csp, list_variables, tuples)

    return csp,variables

    

def nary_ad_grid(kenken_grid):
    ##IMPLEMENT 
    list_variables = []
    variables=[]
    tuples = []
    row=[]
    col=[]
    N = kenken_grid[0][0]
    csp = CSP("nary_ad_grid")

    setup_variable(csp, N, list_variables, variables, tuples, row, col, "Alldiff")

    nary(csp, N, row, col, tuples)

    return csp,variables

    

def kenken_csp_model(kenken_grid):
    ##IMPLEMENT
    list_variables = []
    variables=[]
    tuples = []
    row=[]
    col=[]
    N = kenken_grid[0][0]
    csp = CSP("kenken")

    setup_variable(csp, N, list_variables, variables, tuples, row, col, "binary")

    for cage in kenken_grid:
        all_cell=[]
        all_domain=[]
        if len(cage)!=1:
            operation = cage[-1]
            target_value = cage[-2]
            for i in range(len(cage)-2):
                row_index = int(str(cage[i])[0]) - 1
                col_index = int(str(cage[i])[1]) - 1
                all_domain.append(variables[row_index][col_index].domain())
                all_cell.append(variables[row_index][col_index])

            cons = Constraint("Cage #" + str(kenken_grid.index(cage)), all_cell)
            comb_domain = list(itertools.product(*all_domain))
            cons.add_satisfying_tuples(satisfying_tuples(comb_domain, operation, target_value))
            csp.add_constraint(cons)

    check_binary(csp, list_variables, tuples)
    # nary(csp, N, row, col, tuples)

    return csp, variables

#############################################################################################
#helper
def setup_variable(csp, N, list_variables, variables, tuples, row, col, type):
    #helper function: set up all variables and satisfying tuples for the csp
    domain = []
    for i in range(1, N + 1, 1):
        domain.append(i)
        if type == "Alldiff":
            row.append([])
            col.append([])

    for row in range(1,N+1,1):
        row_list = []
        for column in range(1,N+1,1):
            new_var_name = str(row) + str(column)
            new_var = Variable(new_var_name, domain)
            if type == "Alldiff":
                row[row-1].append(new_var)
                col[column-1].append(new_var)
            row_list.append(new_var)
            list_variables.append(new_var)
            csp.add_var(new_var)
            if row != column and type == "binary":
                tuples.append((row,column))
        variables.append(row_list)
    if type == "Alldiff":
        for item in list(itertools.permutations(domain,N)):
            tuples.append(item)

def check_binary(csp, list_variables, tuples):
    #helper function: constraint for binary not equal
    check_cons = []
    for i in list_variables:
        var1 = i.name
        for j in list_variables:
            var2=j.name
            if var1 != var2:
                if ((var1[0] == var2[0]) or (var1[1] == var2[1])) and ((var1,var2) not in check_cons and (var2,var1) not in check_cons):
                    cons = Constraint(var1 + "," + var2,[i,j])
                    cons.add_satisfying_tuples(tuples)
                    check_cons.append((var1,var2))
                    csp.add_constraint(cons)
    return csp

def nary(csp, N, row, col, tuples):
    #helper function: constraint for n-ary all different
    for i in range(1, N+1):
        row_cons = Constraint("row #" + str(i), row[i-1])
        col_cons = Constraint("column #" + str(i), col[i-1])
        row_cons.add_satisfying_tuples(tuples)
        col_cons.add_satisfying_tuples(tuples)
        csp.add_constraint(row_cons)
        csp.add_constraint(col_cons)

def satisfying_tuples(comb_domain, operation, target_value):
    #helper function: find satisfying tuples based on the operation and target value.
    satisfying_tuples = []
    for d in comb_domain:
        if operation == 0:
            summ = 0
            for val in d:
                summ = summ + val
            if summ == target_value:
                satisfying_tuples.append(d)

        elif (operation == 1):
            permut_d = list(itertools.permutations(d))
            for val in permut_d:
                sub = val[0]
                for i in range(1, len(val)):
                    sub = sub - val[i]
                if sub == target_value:
                    satisfying_tuples.append(d)

        elif (operation == 2):
            permut_d = list(itertools.permutations(d))
            for val in permut_d:
                div = val[0]
                for n in range(1, len(val)):
                    div = div/val[n]
                if (div == target_value):
                    satisfying_tuples.append(d)

        elif (operation == 3):
            Mult = 1
            for val in d:
                Mult = Mult * val
            if (Mult == target_value):
                satisfying_tuples.append(d)

    return satisfying_tuples

#############################################################################################