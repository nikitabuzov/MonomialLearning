from pyeda.boolalg.picosat import satisfy_one
from pyeda.boolalg.picosat import satisfy_all
from pyeda.boolalg.bfarray import exprvar
from pyeda.inter import *
import numpy as np

# Import data
X = np.load('X_2term.npy')
Y = np.load('Y_2term.npy')

# SAT Encoding
clauses = 1
eq1 = 1
eq2 = 1
eq3 = 1
eq4 = 1
eq5 = 1
literal1 = 1
k=195
n=200
mon_len = 1

# Encode hypothesis
for j in range(100):
    one_hot_1 = And(Or(exprvar('N1_'+str(j)),exprvar('P1_'+str(j)),exprvar('Z1_'+str(j))),Or(Not(exprvar('N1_'+str(j))),Not(exprvar('P1_'+str(j)))),Or(Not(exprvar('N1_'+str(j))),Not(exprvar('Z1_'+str(j)))),Or(Not(exprvar('P1_'+str(j))),Not(exprvar('Z1_'+str(j)))))
    one_hot_2 = And(Or(exprvar('N2_'+str(j)),exprvar('P2_'+str(j)),exprvar('Z2_'+str(j))),Or(Not(exprvar('N2_'+str(j))),Not(exprvar('P2_'+str(j)))),Or(Not(exprvar('N2_'+str(j))),Not(exprvar('Z2_'+str(j)))),Or(Not(exprvar('P2_'+str(j))),Not(exprvar('Z2_'+str(j)))))
    clauses = And(one_hot_1,one_hot_2)
# Encode positive and negative samples
for i in range(300):
    # Positive samples
    if Y[i]==1:
        tmp_clause_1 = 1
        tmp_clause_2 = 1
        for j in range(100):
            if X[i,j]==1:
                new_literal_1 = Not(exprvar('N1_'+str(j)))
                new_literal_2 = Not(exprvar('N2_'+str(j)))
            if X[i,j]==0:
                new_literal_1 = Not(exprvar('P1_'+str(j)))
                new_literal_2 = Not(exprvar('P2_'+str(j)))
            tmp_clause_1 = And(tmp_clause_1,new_literal_1)
            tmp_clause_2 = And(tmp_clause_2,new_literal_2)
            tmp_clause = Or(tmp_clause_1,tmp_clause_2)
            tmp_clause = tmp_clause.to_cnf()
        clauses = And(clauses,tmp_clause)
    # Negative samples
    if Y[i]==0:
        tmp_clause_1 = 0
        tmp_clause_2 = 0
        for j in range(100):
            if X[i,j]==1:
                new_literal_1 = exprvar('N1_'+str(j))
                new_literal_2 = exprvar('N2_'+str(j))
            if X[i,j]==0:
                new_literal_1 = exprvar('P1_'+str(j))
                new_literal_2 = exprvar('P2_'+str(j))
            tmp_clause_1 = Or(tmp_clause_1,new_literal_1)
            tmp_clause_2 = Or(tmp_clause_2,new_literal_2)
            tmp_clause = And(tmp_clause_1,tmp_clause_2)
        clauses = And(clauses,tmp_clause)

# Encode monomial length (l=5)

Z=[]
for i in range(100):
    Z1 = exprvar('Z1_'+str(i))
    Z2 = exprvar('Z2_'+str(i))
    Z.append(Z1)
    Z.append(Z2)

eq1 = And(Or(Z[0],Not(exprvar('S0_0'))),Or(exprvar('S0_0'),Not(Z[0])))

for j in range(1,k):
    literal = Not(exprvar('S0_'+str(j)))
    eq2 = And(eq2,literal)

for i in range(1,n):
    literal = Or(Not(Z[i]),Not(exprvar('S'+str(i-1)+'_'+str(k))))
    eq3 = And(eq3,literal)

for i in range(1,n-1):
    for j in range(1,k):
        literal0 = And(Or(Z[i],exprvar('S'+str(i-1)+'_'+str(j)),Not(exprvar('S'+str(i)+'_'+str(j)))),Or(exprvar('S'+str(i-1)+'_'+str(j-1)),exprvar('S'+str(i-1)+'_'+str(j)),Not(exprvar('S'+str(i)+'_'+str(j)))),Or(Not(exprvar('S'+str(i-1)+'_'+str(j))),exprvar('S'+str(i)+'_'+str(j))),Or(Not(Z[i]),Not(exprvar('S'+str(i-1)+'_'+str(j-1))),exprvar('S'+str(i)+'_'+str(j))))
        literal1 = And(literal1,literal0)
    literal = And(Or(Z[i],exprvar('S'+str(i-1)+'_0'),Not(exprvar('S'+str(i)+'_0'))),Or(Not(Z[i]),exprvar('S'+str(i)+'_0')),Or(Not(exprvar('S'+str(i-1)+'_0')),exprvar('S'+str(i)+'_0')),literal1)
    eq4 = And(eq4,literal)

eq5 = And(Or(exprvar('Z1_99'),exprvar('S'+str(n-2)+'_'+str(k-1))),Or(exprvar('S'+str(n-2)+'_'+str(k-2)),exprvar('S'+str(n-2)+'_'+str(k-1))))


# AND all clauses to create CNF
mon_len = And(eq1,eq2,eq3,eq4,eq5)
cnf = And(clauses,mon_len)

# Run SAT Solver
sats = cnf.satisfy_one()

# Format and save the monomial result
monomial_1 = ''
monomial_2 = ''
for key, value in sats.items() :
    for i in range(100):
        if key==exprvar('Z1_'+str(i)):
            if value==0:
                for key1, value1 in sats.items():
                    if key1==exprvar('P0_'+str(i)):
                        if value1==0:
                            monomial_1 += '~x'+str(i)
                    if key1==exprvar('N0_'+str(i)):
                        if value1==0:
                            monomial_1 += 'x'+str(i)
for key, value in sats.items() :
    for i in range(100):
        if key==exprvar('Z2_'+str(i)):
            if value==0:
                for key1, value1 in sats.items():
                    if key1==exprvar('P1_'+str(i)):
                        if value1==0:
                            monomial_2 += '~x'+str(i)
                    if key1==exprvar('N1_'+str(i)):
                        if value1==0:
                            monomial_2 += 'x'+str(i)
print(monomial_1)
print(monomial_2)

result = 'f = ' + monomial_1 + ' + ' + monomial_2
np.save('2term.npy',result)
