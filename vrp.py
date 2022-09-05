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

if len(sys.argv) < 2:
    print('Usage: vrp.py 0 (fake data) or 1 (real data)')
    sys.exit(1)
type = int(sys.argv[1])


n_pessoas=[]
points = []

nPoints = 0  # number of rows in the input file
nFields = 7  # number of columns in the input file

# number of points
N = 0

# number of vehicles K
K = 3

# numero de periodos
P = 3

# porcetagem de pessoas atendidas
porcentagem = 0.5

if type==1:

    with open('localizacoes_all.csv') as csv_file:
        # reading the csv file: logradouro, bairro, cep, numeroPacientes, endereco, latitude, longitude
        
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            # print(row)
            if row[5]=='' or row[6]=='':
                continue
            points.append(location.Location(int(nPoints), row[0], row[1], row[2], int(row[3]), row[4], float(row[6]), float(row[7])))
            nPoints += 1
        
    # distanceMatrix = np.zeros((nPoints, nPoints))
    distanceMatrix = [[0]*nPoints for _ in range(nPoints)]

    for i in range(nPoints):
        n_pessoas.append(points[i].numeroPacientes)
        for j in range(nPoints):
            if i != j:
                p1 = (points[i].coordenada1, points[i].coordenada2)
                p2 = (points[j].coordenada1, points[j].coordenada2)
                # 100* to normalize the distance
                # distanceMatrix[i][j] = distance.euclidean(p1, p2)
                distanceMatrix[i][j] = round(100*math.sqrt((points[i].coordenada1-points[j].coordenada1)**2 + (points[i].coordenada2-points[j].coordenada2)**2),2) 

    print('nPoints = ', nPoints)
    N = nPoints
else:

# print(distanceMatrix)

# input()

# Create n random points

# N = nPoints
    N = 30

    distanceMatrix = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(i):
            randomValue = random.randint(0, 100)
            distanceMatrix[i][j] = randomValue
            distanceMatrix[j][i] = randomValue
            
        
    # generate random n_pessoas array
    n_pessoas = [random.randint(1, 50) for i in range(N)]
    
   

# # for i in range(n):
# #     for j in range(n):
# #         dist[i,j] = round(dist[i,j], 3)

# print(matrix)

model = gp.Model()

model.setParam("NodefileStart", 0.5)
model.setParam("Method", 0)
model.setParam("Threads", 1)
model.setParam("NoRelHeurTime", 300)
model.setParam("MIPFocus", 1)
model.setParam("Presolve", 0)









# sum of all n_pessoass
sumn_pessoas = sum(n_pessoas)
# print('sum n_pessoas = ', sumn_pessoas)

if type==0:
     # capacity of each vehicle
    CAP = math.floor(sumn_pessoas/(0.9*K))
else:
    CAP = 1000


# CAP = 1000
# print('capacity = ', CAP)

# create variables x[i,j,k], where k is the vehicle index
# x[i,j,k] is 1 if the edge (i,j) is in the kth route
# x[i,j,k] is 0 otherwise

# Create variables

# Variable x_ijk is equal to 1 if vehicle k uses edge(i, j), otherwise 0, , for i, j ∈ V,i != j and k ∈ K
x = model.addVars(N, N, K, P, vtype=GRB.BINARY, name="x")

# yik is set to 1 if vehicle k visits node i, otherwise it is equal to 0, for i ∈ V,k ∈ K. 
y = model.addVars(N, vtype=GRB.BINARY, name="y")


# constraints

# todo veiculo deve partir da origem (ponto 0) e retornar a origem
constraint1 = model.addConstrs(gp.quicksum(
    x[i, 0, k, p] for i in range(1, N)) == 1 for k in range(K) for p in range(P))
constraint2 = model.addConstrs(gp.quicksum(
    x[0, i, k, p] for i in range(1, N)) == 1 for k in range(K) for p in range(P))    
        

# caso um nó 'i' seja visitado, este deve ser visitado por exatamente um veiculo
constraint3 = model.addConstrs(gp.quicksum(x[i, j, k,p] for j in range(
    0, N) if i != j for k in range(K) for p in range(P)) == y[i] for i in range(1, N))

constraint4 = model.addConstrs(gp.quicksum(x[i, j, k,p] for i in range(
    0, N)for k in range(K) for p in range(P)) == y[j] for j in range(1, N))

constraint5 = model.addConstrs(gp.quicksum(x[i, m, k,p] for i in range(
    0, N)) - gp.quicksum(x[m, j, k,p] for j in range(0, N)) == 0 for m in range(1, N) for k in range(K) for p in range(P))

# capacity constraint
constraint6 = model.addConstrs(gp.quicksum(n_pessoas[i]*x[i, j, k,p]for i in range(
    0, N) for j in range(0, N)) <= CAP for k in range(K) for p in range(P))

# restricao de atendimento minimo
expr=0
for i in range(N):
    expr += n_pessoas[i]*y[i]

model.addConstr(expr >= porcentagem*sumn_pessoas)

model.update()


# fo minimizando a distancia percorrida. Penalizando de acordo com o periodo de atendimento




# penalidades de acordo com o período. Quando mais tarde, maior a penalidade
penalidades = []
# coeficiente de penalidade de acordo com o numero de pontos
M = N
for p in range(P):
    penalidades.append(p*M)

objDistancia = 0
for p in range(P):
    for k in range(K):
        for i in range(N):
            for j in range(N):
                if i != j:
                    objDistancia += penalidades[p]*distanceMatrix[i][j]*x[i, j, k, p]


# coeficiente_c = -1
# coeficiente_d = 1



model.setObjective(objDistancia, GRB.MINIMIZE)

model.optimize()

# print route for each vehicle
n_cobertos=0
n_pessoas_atendidas=0
distancia_percorrida=0

print('\n------------------------------\nNo de pontos: ', N)
print('No de pessoas = ', sumn_pessoas)
print('No de periodos = ', P)
print('Numero de veiculos: ', K)
print('Capacidade de cada veiculo = ', CAP)



for p in range(P):
    print('\n\n------------------------------\nPeriodo:',p,'\n------------------------------')
    for k in range(K):
        print('\tRota do veículo ', k)
        for i in range(N):
            for j in range(N):
                if x[i, j, k, p].x > 0.000001:
                    distancia_percorrida = distancia_percorrida + distanceMatrix[i][j]
                    print('\t%d ' % i, end='')

        print()

for i in range(N):
    if y[i].x > 0.000001:
        n_pessoas_atendidas+=n_pessoas[i]
        n_cobertos = n_cobertos + 1


print('\n------------------------------')
print('Número de pontos cobertos = ', n_cobertos)
print('Número de pessoas atendidas = ', n_pessoas_atendidas)
print('Distância percorrida total = ', distancia_percorrida)