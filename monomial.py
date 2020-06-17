from pyeda.boolalg.picosat import satisfy_one
from pyeda.boolalg.picosat import satisfy_all
from pyeda.boolalg.bfarray import exprvar
from pyeda.inter import *
import numpy as np

# Import data
X = np.load('X_monomialV3.npy')
Y = np.load('Y_monomialV3.npy')

# SAT Encoding
clauses = 1
eq1 = 1
eq2 = 1
eq3 = 1
eq4 = 1
eq5 = 1
literal1 = 1
k=95
n=100
# Encode hypothesis
for j in range(100):
    one_hot = And(Or(exprvar('N'+str(j)),exprvar('P'+str(j)),exprvar('Z'+str(j))),Or(Not(exprvar('N'+str(j))),Not(exprvar('P'+str(j)))),Or(Not(exprvar('N'+str(j))),Not(exprvar('Z'+str(j)))),Or(Not(exprvar('P'+str(j))),Not(exprvar('Z'+str(j)))))
    clauses = And(clauses,one_hot)
# Encode positive and negative samples
for i in range(1500):
    # Positive samples
    if Y[i]==1:
        tmp_clause = 1
        for j in range(100):
            if X[i,j]==1:
                new_literal = Not(exprvar('N'+str(j)))
            if X[i,j]==0:
                new_literal = Not(exprvar('P'+str(j)))
            tmp_clause = And(tmp_clause,new_literal)
        clauses = And(clauses,tmp_clause)
    # Negative samples
    if Y[i]==0:
        tmp_clause = 0
        for j in range(100):
            if X[i,j]==1:
                new_literal = exprvar('N'+str(j))
            if X[i,j]==0:
                new_literal = exprvar('P'+str(j))
            tmp_clause = Or(tmp_clause,new_literal)
        clauses = And(clauses,tmp_clause)

# Encode monomial length (l=5)
eq1 = And(Or(exprvar('Z0'),Not(exprvar('S0_0'))),Or(exprvar('S0_0'),Not(exprvar('Z0'))))
for j in range(1,k):
    literal = Not(exprvar('S0_'+str(j)))
    eq2 = And(eq2,literal)
for i in range(1,n):
    literal = Or(Not(exprvar('Z'+str(i))),Not(exprvar('S'+str(i-1)+'_'+str(k))))
    eq3 = And(eq3,literal)
for i in range(1,n-1):
    for j in range(1,k):
        literal0 = And(Or(exprvar('Z'+str(i)),exprvar('S'+str(i-1)+'_'+str(j)),Not(exprvar('S'+str(i)+'_'+str(j)))),Or(exprvar('S'+str(i-1)+'_'+str(j-1)),exprvar('S'+str(i-1)+'_'+str(j)),Not(exprvar('S'+str(i)+'_'+str(j)))),Or(Not(exprvar('S'+str(i-1)+'_'+str(j))),exprvar('S'+str(i)+'_'+str(j))),Or(Not(exprvar('Z'+str(i))),Not(exprvar('S'+str(i-1)+'_'+str(j-1))),exprvar('S'+str(i)+'_'+str(j))))
        literal1 = And(literal1,literal0)
    literal = And(Or(exprvar('Z'+str(i)),exprvar('S'+str(i-1)+'_0'),Not(exprvar('S'+str(i)+'_0'))),Or(Not(exprvar('Z'+str(i))),exprvar('S'+str(i)+'_0')),Or(Not(exprvar('S'+str(i-1)+'_0')),exprvar('S'+str(i)+'_0')),literal1)
    eq4 = And(eq4,literal)
eq5 = And(Or(exprvar('Z'+str(n-1)),exprvar('S'+str(n-2)+'_'+str(k-1))),Or(exprvar('S'+str(n-2)+'_'+str(k-2)),exprvar('S'+str(n-2)+'_'+str(k-1))))

# AND all clauses to create CNF
mon_len = And(eq1,eq2,eq3,eq4,eq5)
cnf = And(clauses,mon_len)

# Run SAT Solver
sats = cnf.satisfy_one()

# Format and save the monomial result
monomial = ''
for key, value in sats.items() :
    for i in range(100):
        if key==exprvar('Z'+str(i)):
            if value==0:
                for key1, value1 in sats.items():
                    if key1==exprvar('P'+str(i)):
                        if value1==0:
                            monomial += '~x'+str(i)
                    if key1==exprvar('N'+str(i)):
                        if value1==0:
                            monomial += 'x'+str(i)

result = 'f = ' + monomial
np.save('monomial.npy',result)
