import random
from queue import PriorityQueue

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

#Function to generate an instance of k-SAT problem
def generateInstance(n, k, m):

  vars = []
  for i in range(n):
    vars.append((chr(i + 65)))

  problem = "(("
  clause = []

  for i in range(k * m):

    x = random.choice(vars)
    vars.remove(x)
    clause.append(x)

    if(i % k == k - 1):
      while len(clause) != 0:
        vars.append(clause.pop(0))

    y = random.random()
    if y < 0.5:
      problem += "~"
    
    problem += x

    if i % k == k - 1 and i != (k * m - 1):
      problem += ") and ("
    elif i != (k * m - 1):
      problem += " or "
  
  problem += "))"
      
  return problem

# Function to generate a random assignment of variables
def generateRandomAssignment(num_vars):
    return [random.randint(0, 1) for _ in range(num_vars)]

# Function to evaluate the fitness of a given assignment of variables
def evaluate(assignment, k, variables, posOrNeg):
    fitness = 0
    clauseEval = 0

    for i in range(len(variables)):
      if posOrNeg[i] == 'P':
        clauseEval = clauseEval or assignment[variables[i]] 
      else:
        clauseEval = clauseEval or (1 - assignment[variables[i]])
      
      if i % k == k - 1 and clauseEval == 1:
        fitness += 1
        clauseEval = 0
      
    return fitness


#function to solve 3-SAT using hill climbing approach
def hillClimbing(assignment, depth, k, variables, posOrNeg):
  d = 0  
  while d < depth:
    currentFitness = evaluate(assignment, k, variables, posOrNeg)

    if(currentFitness == len(variables)):
      return assignment
    
    change = '0'

    for c in assignment.keys():
      neighbour = assignment.copy()
      neighbour[c] = 1 - neighbour[c]
      
      neighbourFitness = evaluate(neighbour, k, variables, posOrNeg)
      if neighbourFitness > currentFitness:
        currentFitness = neighbourFitness
        change = c
  
    d += 1
    if change != '0':
      assignment[change] = 1 - assignment[change]

  return assignment

#function to solve 3-SAT using Beam Search
def beamSearch(assignment, k, variables, posOrNeg, b, steps):

  beam = PriorityQueue()
  current = assignment
  x = evaluate(current, k, variables, posOrNeg)
  beam.put(PrioritizedItem(-x, assignment))
  s = 0

  while (not beam.empty()) and s < steps:
    state = beam.get()
    current = state.item
    x = -state.priority

    if x == len(variables):
      return current

    for c in current.keys():
      neighbour = current.copy()
      neighbour[c] = 1 - neighbour[c]

      neighbourFitness = evaluate(neighbour, k, variables, posOrNeg)

      if beam.qsize() < b:
        beam.put(PrioritizedItem(-neighbourFitness, neighbour))
      else:
        copy = beam.get()
        if neighbourFitness > (-copy.priority):
          beam.put(PrioritizedItem(-neighbourFitness, neighbour))
        else:
          beam.put(copy)
      
      s += 1

  return current

# neigbour state is the one in which a random variable value is flipped
def neighbour1(assignment):
  c = random.choice(list(assignment))
  assignment[c] = 1 - assignment[c]
  return assignment


# neigbour state is the one in which value of any two variables is swapped
def neighbour2(assignment):
  c = random.choice(list(assignment))
  d = random.choice(list(assignment))

  while d == c:
    d = random.choice(list(assignment))
  
  x = assignment[c]
  assignment[c] = assignment[d]
  assignment[d] = x
  
  return assignment

# neigbour state is the one in which value of first variable is flipped
def neighbour3(assignment):
  x = list(assignment.keys())[0]
  assignment[x] = 1 - assignment[x]
  return assignment

def variableNeighbourhood(assignment, k, variables, posOrNeg, steps):
  s = 0
  current = assignment
  
  while s < steps:
    current = assignment
    x = evaluate(assignment, k, variables, posOrNeg)

    if x == len(variables):
      return current

    nbr1 = neighbour1(current.copy())
    nbr2 = neighbour2(current.copy())
    nbr3 = neighbour3(current.copy())

    fn1 = evaluate(nbr1, k, variables, posOrNeg)
    fn2 = evaluate(nbr2, k, variables, posOrNeg)
    fn3 = evaluate(nbr3, k, variables, posOrNeg)

    if max(fn1, fn2, fn3) > x:
      x = max(fn1, fn2, fn3)
      if x == fn1:
        current = nbr1
      elif x == fn2:
        current = nbr2
      else:
        x =  nbr3
    
    s += 1
  
  return current

    # for c in current.keys():
    #   neighbour = current.copy()
    #   neighbour[c] = 1 - neighbour[c]

    #   neighbourFitness = evaluate(neighbour, k, variables, posOrNeg)

    #   if beam.qsize() < b:
    #     beam.put(PrioritizedItem(-neighbourFitness, neighbour))
    #   else:
    #     copy = beam.get()
    #     if neighbourFitness > (-copy.priority):
    #       beam.put(PrioritizedItem(-neighbourFitness, neighbour))
    #     else:
    #       beam.put(copy)

n = 25
k = 3
m = 1000
problem = generateInstance(n,k,m)
numVars = set()
variables = []
posOrNeg = []

prevNeg = False

for i in range(len(problem)):
  if problem[i] == '~':
    prevNeg = True
  elif ord(problem[i]) >= 65 and ord(problem[i]) <= 90:
    if prevNeg == True:
      posOrNeg.append('N')
      prevNeg = False
    else:
      posOrNeg.append('P')

    variables.append(problem[i])
    numVars.add(problem[i])


values = generateRandomAssignment(len(numVars))
startState = dict()

index = 0
for c in numVars:
  startState[c] = values[index]
  index += 1

print(startState)
print("Starting State Fitness: ", evaluate(startState, k, variables, posOrNeg))
solution  = hillClimbing(startState.copy(), 100, k, variables, posOrNeg)
print("Hill Climbing Solution Fitness: ", evaluate(solution, k, variables, posOrNeg))
solution = beamSearch(startState.copy(), k, variables, posOrNeg, 3, 1000)
print("Beam Search Solution Fitness (Beam-Width = 3): ", evaluate(solution, k, variables, posOrNeg))
solution = beamSearch(startState.copy(), k, variables, posOrNeg, 4, 1000)
print("Beam Search Solution Fitness (Beam-Width = 4): ", evaluate(solution, k, variables, posOrNeg))


print("Neighbour 1: ", neighbour1(startState.copy()))
print("Neighbour 2: ", neighbour2(startState.copy()))
print("Neighbour 3: ", neighbour3(startState.copy()))

solution = variableNeighbourhood(startState.copy(), k, variables, posOrNeg, 1000)
print("Variable-Neigbourhood-Descent Fitness: ", evaluate(solution, k, variables, posOrNeg))
