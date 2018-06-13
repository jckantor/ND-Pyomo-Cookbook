from pyomo.environ import *
from pyomo.gdp import *

# Strip-packing example from http://minlp.org/library/lib.php?lib=GDP

# This model packs a set of rectangles without rotation or overlap within a
# strip of a given width, minimizing the length of the strip.

model = ConcreteModel()

model.RECTANGLES = Set(ordered=True, initialize=[0,1,2,3])

# Width and Lenght of each rectangle
model.Width = Param(model.RECTANGLES, initialize={0:6, 1:3, 2:4, 3:2})
model.Length = Param(model.RECTANGLES, initialize={0:6, 1:8, 2:5, 3:3})

model.StripWidth = Param(
    initialize=10,
    doc="Width of the strip"
)

# upperbound on length (default is sum of lengths of rectangles)
model.LengthUB = Param(
    initialize=sum(model.Length[i] for i in model.RECTANGLES))

# x (length) and y (width) coordinates of each of the rectangles
model.x = Var( model.RECTANGLES,
               bounds=(0, model.LengthUB),
               doc="rectangle corner x-position (position down length)")
def y_bounds(m, i):
    return (0, m.StripWidth-m.Width[i])
model.y = Var( model.RECTANGLES,
               bounds=y_bounds,
               doc="rectangle corner y-position (position across width)") 

# length of strip (this will be the objective)
model.MaxLength = Var(within=NonNegativeReals)

# generate the list of possible rectangle conflicts (which are any pair)
def rec_pairs_filter(model, i, j):
    return i < j
model.OVERLAP_PAIRS = Set(initialize=model.RECTANGLES * model.RECTANGLES,
    dimen=2, filter=rec_pairs_filter)

# strip length constraint
@model.Constraint(model.RECTANGLES)
def strip_ends_after_last_rec(model, i):
    return model.MaxLength >= model.x[i] + model.Length[i]

# minimize length
model.total_length = Objective(expr=model.MaxLength)

#
# Insert the no-overlap disjunctions here!
#

#
# Transform the model using the Big-M relaxation here!
#

#
# Solve and print the solution
#
SolverFactory('glpk').solve(model, tee=True)
for i in model.RECTANGLES:
    print("Rectangle %s: (%s, %s)" % (i, value(model.x[i]), value(model.y[i])))
model.total_length.display()
