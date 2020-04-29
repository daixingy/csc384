#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
import operator
'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''

def ord_mrv(csp):
    #IMPLEMENT
    variable = csp.get_all_unasgn_vars()

    mrv = variable[0]
    min_dsize = mrv.cur_domain_size()

    for var in variable:
        if var.cur_domain_size() < min_dsize:
            mrv = var
            min_dsize = var.cur_domain_size()

    return mrv

def val_lcv(csp,var):
    #IMPLEMENT 
    lst = {}
    cons = csp.get_cons_with_var(var)
    for d in var.cur_domain():
        var.assign(d)
        num_pruned = 0
        for c in cons:
            variables = c.get_unasgn_vars()
            for V in variables:
                for i in V.cur_domain():
                    if not c.has_support(V, i):
                        num_pruned += 1
        var.unassign()
        lst[num_pruned] = d

    lcv = []
    for k, v in lst.items():
        lcv.append(v)

    return lcv
