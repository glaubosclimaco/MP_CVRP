# vehicle routing problem with gurobi
#
# # Solve a vehicle routing problem with gurobi
#
import sys
import math
import random
from itertools import combinations
import gurobipy as gp

from gurobipy import *
from numpy import matrix


# Parse argument

if len(sys.argv) < 2:
    print('Usage: tsp.py npoints')
    sys.exit(1)
N = int(sys.argv[1])

# Create n random points

random.seed(1)
points = [(random.randint(0, 100), random.randint(0, 100)) for i in range(N)]

# Dictionary of Euclidean distance between each pair of points

# rows = 5
# cols = 5

# dist = [[0]*cols for _ in range(rows)]
# print(f'matrix with dimension {rows} x {cols} is {dist}')

dist = {(i, j):
        round(
            math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2))), 0)
        for i in range(N) for j in range(i)}

# generate random symmetric matrix of distances between all pairs of points (i,j) and (j,i)
# dist = {(i, j):
#         round(
matrix = [[0]*N for _ in range(N)]
for i in range(N):
    for j in range(i):
        randomValue = random.randint(0, 100)
        matrix[i][j] = randomValue
        matrix[j][i] = randomValue

# for i in range(n):
#     for j in range(n):
#         dist[i,j] = round(dist[i,j], 3)

print(matrix)

model = gp.Model()

# number of vehicles K
K = 3
# capacity of each vehicle
CAP = 10

# create variables x[i,j,k], where k is the vehicle index
# x[i,j,k] is 1 if the edge (i,j) is in the kth route
# x[i,j,k] is 0 otherwise

# Create variables
x = model.addVars(N, N, K, vtype=GRB.BINARY, name="x")
z = model.addVars(K, vtype=GRB.BINARY, name="z")


# constraints
constraint1 = model.addConstrs(gp.quicksum(
    x[i, 0, k] for i in range(1, N)) == 1 for k in range(K))
constraint2 = model.addConstrs(gp.quicksum(
    x[0, i, k] for i in range(1, N)) == 1 for k in range(K))


# constraint 3
# for i in range(1, N):
#     for k in range(K):
#         model.addConstr(gp.quicksum(x[i, j, k] for j in range(1, N)) == 1)


constraint3 = model.addConstrs(gp.quicksum(x[i, j, k] for i in range(
    0, N) if i != j for k in range(K)) == 1 for j in range(1, N))
constraint4 = model.addConstrs(gp.quicksum(x[i, j, k] for j in range(
    0, N)for k in range(K)) == 1 for i in range(1, N))
constraint5 = model.addConstrs(gp.quicksum(x[i, m, k] for i in range(
    0, N)) - gp.quicksum(x[m, j, k] for j in range(0, N)) == 0 for m in range(1, N) for k in range(K))

# capacity constraint
# constraint6 = model.addConstrs(gp.quicksum(q[i][n]*x[i, j, k]for i in range(
#     0, N) for j in range(0, N)) <= CAP for k in range(K) for n in range(3))


model.update()


model.setObjective(gp.quicksum(matrix[i][j]*x[i, j, k] for i in range(0, N)
                   for j in range(0, N) for k in range(K)), GRB.MINIMIZE)


model.optimize()

# print route for each vehicle
for k in range(K):
    print('Route for vehicle', k)
    for i in range(N):
        for j in range(N):
            if x[i, j, k].x > 0.5:
                print('%d ' % i, end='')

    print()
