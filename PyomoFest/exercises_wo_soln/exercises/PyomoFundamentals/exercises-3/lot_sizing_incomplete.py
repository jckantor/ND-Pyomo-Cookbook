from pyomo.environ import *

model = ConcreteModel()
model.T = RangeSet(5)    # time periods

i0 = 5.0           # initial inventory
c = 4.6            # setup cost
h_pos = 0.7        # inventory holding cost
h_neg = 1.2        # shortage cost
P = 5.0            # maximum production amount

# demand during period t
d = {1: 5.0, 2:7.0, 3:6.2, 4:3.1, 5:1.7}


# TODO: WRITE CODE FOR THE MODEL HERE

# solve the problem
solver = SolverFactory('glpk')
solver.solve(model)

# print the results
for t in model.T:
    print('Period: {0}, Prod. Amount: {1}'.format(t, value(model.x[t]))) 

