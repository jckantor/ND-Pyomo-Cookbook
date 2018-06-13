# warehouse_location.py: Warehouse location determination problem
from pyomo.environ import *

model = ConcreteModel(name="(WL)")

W = ['Harlingen', 'Memphis', 'Ashland']
C = ['NYC', 'LA', 'Chicago', 'Houston']
d = {('Harlingen', 'NYC'): 1956, \
     ('Harlingen', 'LA'): 1606, \
     ('Harlingen', 'Chicago'): 1410, \
     ('Harlingen', 'Houston'): 330, \
     ('Memphis', 'NYC'): 1096, \
     ('Memphis', 'LA'): 1792, \
     ('Memphis', 'Chicago'): 531, \
     ('Memphis', 'Houston'): 567, \
     ('Ashland', 'NYC'): 485, \
     ('Ashland', 'LA'): 2322, \
     ('Ashland', 'Chicago'): 324, \
     ('Ashland', 'Houston'): 1236 }
P = 2

model.x = Var(W, C, bounds=(0,1))
model.y = Var(W, within=Binary)

@model.Objective()
def obj(m):
    return sum(d[w,c]*m.x[w,c] for w in W for c in C)

@model.Constraint(C)
def one_per_cust(m, c):
    return sum(m.x[w,c] for w in W) == 1

# TODO: ADD DECORATOR HERE
def warehouse_active(m, w, c):
    return m.x[w,c] <= m.y[w]

# TODO: ADD DECORATOR HERE
def num_warehouses(m):
    return sum(m.y[w] for w in W) <= P

SolverFactory('glpk').solve(model)

model.y.pprint()
model.x.pprint()

