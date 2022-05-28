from pysat.solvers import Minisat22
from pysat.card import *
from os import path
import sys
import math
if len(sys.argv) < 2 or not path.exists(sys.argv[1]):  
    print("Give sudoku file.")
    exit()
f = open(sys.argv[1], "r")
lines = f.readlines()
# Init sudoku and check if it is valid
N = -1
n = -1
isSudoku = True
sudoku = []
for line in lines:
    row = line.split()
    if(len(row) > 0):
        if(N == -1):
            N = len(row)
        elif(len(row) != N):
            isSudoku = False
        for num in row:
            num = int(num)
            if(num > N or num < 0):
                print("eh")
                isSudoku = False
                break
        if(not isSudoku):
            break
        sudoku.append(row)
if not isSudoku or N != len(sudoku) or math.pow(int(math.sqrt(N)), 2) != N:
    print("Give valid sudoku file. Valid empty sudoku has size of NxN, has only integers and all integers are from range {0, 1, ..., N-1, N}.")    
    exit()
n = int(math.sqrt(N))
'''
Encode sudoku problem into CNF where: 
- x_ij=k = 1 iff cell (i,j) has value k where i=1, ..., N and j=1, ..., N 
- variables 1...N<=>x_11=1...N, N+1...2n<=>x_21=1...N and so on, so variable x_ij=k is variable ((j-1)*N+i-1)*N+k
'''
instance = CNF()
# every cell takes exactly one value
for j in range(1, N+1):
    for i in range(1, N+1):
        # every cell is at least one integer from range {1, 2, ..., N-1, N} or what is already filled
        if(int(sudoku[j-1][i-1])==0):
            clause = [];
            for k in range(1, N+1):
                clause.append(((j-1)*N+i-1)*N+k)
            instance.append(clause)
        else:
            instance.append([((j-1)*N+i-1)*N+int(sudoku[j-1][i-1])]) 
        # pairwise for x_ij=k for k=1...N
        variables = []
        for k in range(1, N+1):
            variables.append(((j-1)*N+i-1)*N+k)
        instance.extend(CardEnc.atmost(lits=variables, bound=1, encoding=EncType.pairwise).clauses)
# every column has at most one of each values
for k in range(1, N+1):
    for i in range(1, N+1):
        # pairwise x_ij=k for j=1...N
        variables = []
        for j in range(1, N+1):
            variables.append(((j-1)*N+i-1)*N+k)
        instance.extend(CardEnc.atmost(lits=variables, bound=1, encoding=EncType.pairwise).clauses)
# every row has at most one of each values
for k in range(1, N+1):
    for j in range(1, N+1):
        # at most one x_ij=k for i=1...N
        variables = []
        for i in range(1, N+1):
            variables.append(((j-1)*N+i-1)*N+k)
        instance.extend(CardEnc.atmost(lits=variables, bound=1, encoding=EncType.pairwise).clauses)
# every subgrid has at most one of each values
for k in range(1, N+1):
    #pairwise x_ij=k for (i, j) in subgrid((bi, bj))
    for bj in range(0, n):
        for bi in range(0, n):
            variables = []
            for j in range(bj*n+1, (bj+1)*n+1):
                for i in range(bi*n+1, (bi+1)*n+1):
                    variables.append(((j-1)*N+i-1)*N+k)
            instance.extend(CardEnc.atmost(lits=variables, bound=1, encoding=EncType.pairwise).clauses)
solver = Minisat22(bootstrap_with=instance.clauses)
# Solve CNF and print solution if sudoku is solvable
if(solver.solve()):
    model = solver.get_model()
    i = 0
    j = 0
    for x in model:
        if(x>0):
            sudoku[j][i] = x - ((j)*N+i)*N
            i += 1
            if(i == N):
                i = 0
                j += 1
    for row in sudoku:
        print(" ".join(map(str,row)))
else:
    print("Given sudoku is not solvable")
    print(instance.clauses)
