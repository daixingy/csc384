#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the LunarLockout  domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

#import os for time functions
from search import * #for search engines
from lunarlockout import LunarLockoutState, Direction, lockout_goal_state #for LunarLockout specific classes and problems
import math

#LunarLockout HEURISTICS
def heur_trivial(state):
    '''trivial admissible LunarLockout heuristic'''
    '''INPUT: a LunarLockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''       
    summ = 0
    escape = ((state.width-1)/2, (state.width-1)/2)
    if len(state.xanadus) > 2:
      for i in range(len(state.xanadus)):
        summ += math.sqrt(abs(state.xanadus[i][0] - escape[0])**2 + abs(state.xanadus[i][1] - escape[1])**2)
    else:
      summ = math.sqrt(abs(state.xanadus[0] - escape[0])**2 + abs(state.xanadus[1] - escape[1])**2)

    return summ

def heur_L_distance(state):
    #IMPLEMENT
    '''L distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #Write a heuristic function that uses mahnattan distance to estimate distance between the current state and the goal.
    #Your function should return a sum of the L distances between each xanadu and the escape hatch.
    summ = 0
    escape = ((state.width-1)/2, (state.width-1)/2)
    if isinstance(state.xanadus[0], int):
      xanadus_lst = [state.xanadus]
    else:
      xanadus_lst = state.xanadus
    
    for i in xanadus_lst:
        summ += abs(i[0] - escape[0]) + abs(i[1] - escape[1])

    return summ

def heur_alternate(state):
#IMPLEMENT
    '''a better lunar lockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
    #Your function should return a numeric value for the estimate of the distance to the goal.

    #first set up heur to L distance
    heur = heur_L_distance(state)

    #Check is there one xanadus or multiple
    if isinstance(state.xanadus[0], int):
      xanadus_lst = [state.xanadus]
    else:
      xanadus_lst = state.xanadus

    #if the state is a dead state, then return infinite directly
    if check_deadlock(xanadus_lst, state):
      return float('inf')

    #if there is no more xanadus in the state, then return 0 
    if len(state.xanadus) == 0:
      return 0

    #check if there are four robots blocking the escape hatch.
    if check_surrounding(state):
      heur += 100

    #check if there is a robots standing on the escape hatch
    if ((state.width-1)/2, (state.width-1)/2) in state.robots:
      heur += 100

    #for all xanadus in the game
    for target in xanadus_lst:
      #if there only need one more step to win
      if check_win(target, state):
        if check_blocking(target, state):
          return 0.00000000000001
      #check if there is a robot block the way
      if check_blocking(target, state):
        heur += 100
      #check if no robots be in the same row or coloum with the xanadus
      if check_coloum_and_row(target, state):
        heur += 100

    return heur

####################################################################################
#helper
def check_surrounding(state):
  up = ((state.width-1)/2 - 1, (state.width-1)/2)
  down = ((state.width-1)/2 + 1, (state.width-1)/2)
  left = ((state.width-1)/2, (state.width-1)/2 - 1)
  right = ((state.width-1)/2, (state.width-1)/2 + 1)

  if (up in state.robots) and (down in state.robots) and (left in state.robots) and (right in state.robots):
    return True
  else:
    return False

def check_blocking(target, state):
  if target[0] == (state.width-1)/2:
    for robot in state.robots:
      if robot[0] == (state.width-1)/2:
        if (target[1] < robot[1] < (state.width-1)/2) or (target[1] > robot[1] > (state.width-1)/2):
          return True
    return False

  elif target[1] == (state.width-1)/2:
    for robot in state.robots:
      if robot[1] == (state.width-1)/2:
        if (target[0] < robot[0] < (state.width-1)/2) or (target[0] > robot[0] > (state.width-1)/2):
          return True
    return False

def check_win(target, state):
  if target[0] == (state.width-1)/2:
    if target[1] < (state.width-1)/2:
      if ((state.width-1)/2, (state.width-1)/2+1) in state.robots:
        return True
    if target[1] > (state.width-1)/2:
      if ((state.width-1)/2, (state.width-1)/2-1) in state.robots:
        return True
    return False

  if target[1] == (state.width-1)/2:
    if target[0] < (state.width-1)/2:
      if ((state.width-1)/2+1, (state.width-1)/2) in state.robots:
        return True
    if target[0] > (state.width-1)/2:
      if ((state.width-1)/2-1, (state.width-1)/2) in state.robots:
        return True
    return False

def check_coloum_and_row(target, state):
  success = 0
  if isinstance(state.xanadus[0], int):
    for robot in state.robots:
      if robot[0] == target[0] or robot[1] == target[1]:
        success += 1
    if success == 0:
      return True
    return False
  else:
    for robot in state.robots:
      if robot[0] == target[0] or robot[1] == target[1]:
        success += 1
    for xanadu in state.xanadus:
      if xanadu[0] == target[0] or xanadu[1] == target[1]:
        success += 1
    if success == 1:
      return True
    return False


def check_deadlock(xanadus_lst, state):
  for target in xanadus_lst:
    deadlock = 0
    x, y = target[0], target[1]
    for rest in xanadus_lst:
      if rest[0] < x and rest[1] < y:
        deadlock += 1
    for rest in state.robots:
      if rest[0] < x and rest[1] < y:
        deadlock += 1
    if deadlock == len(xanadus_lst) + len(state.robots) - 1:
      return True

  for target in xanadus_lst:
    deadlock = 0
    x, y = target[0], target[1]
    for rest in xanadus_lst:
      if rest[0] > x and rest[1] > y:
        deadlock += 1
    for rest in state.robots:
      if rest[0] > x and rest[1] > y:
        deadlock += 1
    if deadlock == len(xanadus_lst) + len(state.robots) - 1:
      return True
  return False

####################################################################################

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + (weight * sN.hval)

def anytime_weighted_astar(initial_state, heur_fn, weight=4., timebound = 1):
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  
  #set up search engine with stratergy set to custom
  SE = SearchEngine('custom', 'full')
  wraped_fval_function = (lambda sN: fval_function(sN, weight))
  SE.init_search(initial_state, goal_fn=lockout_goal_state, heur_fn=heur_fn, fval_function=wraped_fval_function)

  #Calculate time left after first search on the initial state
  start_time = os.times()[0]
  goal = SE.search(timebound)
  time_remain = timebound - (os.times()[0] - start_time)
  
  #If a goal is found
  i = 1
  if goal:
    while time_remain > 0:
      start_time = os.times()[0]
      #Search for new goal with less G, H, F value if there are time left.
      new_goal = SE.search(time_remain, costbound=(float('inf'), float('inf'), goal.gval + heur_fn(goal)))
      time_remain -= os.times()[0] - start_time
      if new_goal:
        goal = new_goal
    return goal
  #Goal is not found, return False
  else:
    return False

def anytime_gbfs(initial_state, heur_fn, timebound = 1):
  #IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''

  #set up search engine with best first search
  SE = SearchEngine("best_first", "full")
  SE.init_search(initial_state, goal_fn=lockout_goal_state, heur_fn=heur_fn)

  #Calculate time left after first search on the initial state
  start_time = os.times()[0]
  goal = SE.search(timebound)
  time_remain = timebound - (os.times()[0] - start_time)

  #If a goal is found
  if goal:
    while time_remain > 0 and not SE.open.empty:
      start_time = os.times()[0]
      #Search for new goal with less G_value if there are time left.
      new_goal = SE.search(time_remain, costbound=(goal.gval, float('inf'), float('inf')))
      time_remain -= os.times()[0] - start_time
      if new_goal:
        goal = new_goal
    return goal
  #Goal is not found, return False
  else:
    return False

PROBLEMS = (
  #5x5 boards: all are solveable
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 1))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 2))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 3))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 1))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 2))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 3))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 4))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 0))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 1))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (0, 2),(0,4),(2,0),(4,0)),((4, 4))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 0))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 1))),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 3))),
  #7x7 BOARDS: all are solveable
  LunarLockoutState("START", 0, None, 7, ((4, 2), (1, 3), (6,3), (5,4)), ((6, 2))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (4, 2), (2,6)), ((4, 6))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (3, 1), (4, 1), (2,6), (4,6)), ((2, 0),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((1, 2), (0 ,2), (2 ,3), (4, 4), (2, 5)), ((2, 4),(3, 1),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 2), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 1), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (0 ,2), (1 ,2), (6, 4), (2, 5)), ((2, 0),(3, 0),(4, 0))),
  )

if __name__ == "__main__":

  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #1 second time limit for each problem
  print("*************************************")  
  print("Running A-star")  


  # for i in range(len(PROBLEMS)): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

  #   print("*************************************")  
  #   print("PROBLEM {}".format(i))
    
  #   s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

  #   # print("*******RUNNING A STAR*******") 
  #   se = SearchEngine('astar', 'full')
  #   se.init_search(s0, lockout_goal_state, heur_alternate)
  #   final = se.search(timebound) 

  #   if final:
  #     # final.print_path()
  #     solved += 1
  #   else:
  #     unsolved.append(i)    
  #   counter += 1

  # if counter > 0:  
  #   percent = (solved/counter)*100

  # print("*************************************")  
  # print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  # print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  # print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; 
  print("Running Anytime Weighted A-star")   

  for i in range(len(PROBLEMS)):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]  
    weight = 1000
    final = anytime_weighted_astar(s0, heur_alternate, weight, timebound)

    if final:
      # final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; 
  print("Running Anytime GBFS")   

  for i in range(len(PROBLEMS)):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]  
    final = anytime_gbfs(s0, heur_alternate, timebound)

    if final:
      # final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************")   



  

