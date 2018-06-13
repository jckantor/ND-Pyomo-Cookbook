from pyomo.environ import *

A = ['hammer', 'wrench', 'screwdriver', 'towel']
b = {'hammer':8, 'wrench':3, 'screwdriver':6, 'towel':11}
w = {'hammer':5, 'wrench':7, 'screwdriver':4, 'towel':3}
W_max = 14

model = ConcreteModel()
model.x = Var( A, within=Binary )
model.item_benefit = # TODO: DEFINE THE PYOMO PARAM HERE

def obj_rule(m):
    return sum( m.item_benefit[i]*m.x[i] for i in A )
model.obj = Objective(rule=obj_rule, sense = maximize )

def weight_rule(m):
    return sum( w[i]*m.x[i] for i in A ) <= W_max
model.weight = Constraint(rule=weight_rule)

opt = SolverFactory('glpk')

for wrench_benefit in range(1,11):
    model.item_benefit['wrench'] = wrench_benefit
    result_obj = opt.solve(model)

    # TODO: PRINT THE BENEFIT OF THE WRENCH FOR EACH ITERATION IN THE LOOP

