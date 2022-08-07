# vehicle routing problem with gurobi
#
# # Solve a vehicle routing problem with gurobi
#
from logging import captureWarnings
import sys
import math
import random
from itertools import combinations
import gurobipy as gp
import csv
from gurobipy import *
# from numpy import matrix
import location
import math


# Parse argument

# if len(sys.argv) < 2:
#     print('Usage: tsp.py npoints')
#     sys.exit(1)
# N = int(sys.argv[1])



points = []

nPoints = 0  # number of rows in the input file
nFields = 7  # number of columns in the input file



# with open('localizacoes_all.csv') as csv_file:
#     # reading the csv file: logradouro, bairro, cep, numeroPacientes, endereco, latitude, longitude
    
#     csv_reader = csv.reader(csv_file, delimiter=';')
#     for row in csv_reader:
#         # print(row)
#         if row[5]=='' or row[6]=='':
#             continue
#         points.append(location.Location(int(nPoints), row[0], row[1], row[2], int(row[3]), row[4], float(row[6]), float(row[7])))
#         nPoints += 1
    
# # distanceMatrix = np.zeros((nPoints, nPoints))
# distanceMatrix = [[0]*nPoints for _ in range(nPoints)]
# n_pessoas=[]

# for i in range(nPoints):
#     n_pessoas.append(points[i].numeroPacientes)
#     for j in range(nPoints):
#         if i != j:
#             p1 = (points[i].coordenada1, points[i].coordenada2)
#             p2 = (points[j].coordenada1, points[j].coordenada2)
#             # 100* to normalize the distance
#             # distanceMatrix[i][j] = distance.euclidean(p1, p2)
#             distanceMatrix[i][j] = round(100*math.sqrt((points[i].coordenada1-points[j].coordenada1)**2 + (points[i].coordenada2-points[j].coordenada2)**2),2) 

# print('nPoints = ', nPoints)



# print(distanceMatrix)

# input()

# Create n random points

# N = nPoints
N = 10

distanceMatrix = [[0]*N for _ in range(N)]
for i in range(N):
    for j in range(i):
        randomValue = random.randint(0, 100)
        distanceMatrix[i][j] = randomValue
        distanceMatrix[j][i] = randomValue

# # for i in range(n):
# #     for j in range(n):
# #         dist[i,j] = round(dist[i,j], 3)

# print(matrix)

model = gp.Model()



# number of vehicles K
K = 3

# numro de periodos
P = 3

# generate random n_pessoas array
n_pessoas=[]
n_pessoas = [random.randint(1, 10) for i in range(N)]

# sum of all n_pessoass
sumn_pessoas = sum(n_pessoas)
print('sum n_pessoas = ', sumn_pessoas)

# capacity of each vehicle
CAP = math.floor(sumn_pessoas/(0.7*K))
# CAP = 1000
print('capacity = ', CAP)

# create variables x[i,j,k], where k is the vehicle index
# x[i,j,k] is 1 if the edge (i,j) is in the kth route
# x[i,j,k] is 0 otherwise

# Create variables

# Variable x_ijk is equal to 1 if vehicle k uses edge(i, j), otherwise 0, , for i, j ∈ V,i != j and k ∈ K
x = model.addVars(N, N, K, vtype=GRB.BINARY, name="x")

# yik is set to 1 if vehicle k visits node i, otherwise it is equal to 0, for i ∈ V,k ∈ K. 
y = model.addVars(N, vtype=GRB.BINARY, name="y")


# constraints
constraint1 = model.addConstrs(gp.quicksum(
    x[i, 0, k] for i in range(1, N)) == 1 for k in range(K))
constraint2 = model.addConstrs(gp.quicksum(
    x[0, i, k] for i in range(1, N)) == 1 for k in range(K))



        
        

constraint3 = model.addConstrs(gp.quicksum(x[i, j, k] for j in range(
    0, N) if i != j for k in range(K)) == y[i] for i in range(1, N))
constraint4 = model.addConstrs(gp.quicksum(x[i, j, k] for i in range(
    0, N)for k in range(K)) == y[j] for j in range(1, N))
constraint5 = model.addConstrs(gp.quicksum(x[i, m, k] for i in range(
    0, N)) - gp.quicksum(x[m, j, k] for j in range(0, N)) == 0 for m in range(1, N) for k in range(K))

# capacity constraint
constraint6 = model.addConstrs(gp.quicksum(n_pessoas[i]*x[i, j, k]for i in range(
    0, N) for j in range(0, N)) <= CAP for k in range(K) for n in range(3))


model.update()


# fo minimizando a distancia percorrida e maximizando o numero de pessoas atendidas

objCobertura=0
for i in range(N):
    objCobertura += n_pessoas[i]*y[i]

objDistancia = 0
for k in range(K):
    for i in range(N):
        for j in range(N):
            if i != j:
                objDistancia += distanceMatrix[i][j]*x[i, j, k]


coeficiente_c = -1
coeficiente_d = 1

model.setObjective(coeficiente_c*objCobertura + coeficiente_d*objDistancia, GRB.MINIMIZE)

model.optimize()

# print route for each vehicle
n_cobertos=0
n_pessoas_atendidas=0
distancia_percorrida=0
for k in range(K):
    print('Rota do veículo ', k)
    for i in range(N):
        for j in range(N):
            if x[i, j, k].x > 0.000001:
               
                distancia_percorrida = distancia_percorrida + distanceMatrix[i][j]
               
                print('%d ' % i, end='')

    print()

for i in range(N):
    if y[i].x > 0.000001:
        n_pessoas_atendidas+=n_pessoas[i]
        n_cobertos = n_cobertos + 1


print('\n-----------------------------------------')
print('Número de pontos cobertos = ', n_cobertos)
print('Número de pessoas atendidas = ', n_pessoas_atendidas)
print('Distância percorrida total = ', distancia_percorrida)