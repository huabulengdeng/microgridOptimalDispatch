from importFile import *
from pyomo.bilevel import *
from microgrid_Model import *
M = ConcreteModel()
M.x = Var(bounds=(0,None))
M.sub = SubModel()
M.sub.y = Var(bounds=(0,None))
M.sub.z = Var(bounds=(0,None))
M.sub.o = Objective(expr=M.sub.y - M.sub.z)
M.sub.c1 = Constraint(expr=- M.x - M.sub.y <= -3)
M.sub.c2 = Constraint(expr=-2*M.x + M.sub.y <= 0)
M.sub.c3 = Constraint(expr= 2*M.x + M.sub.y <= 12)
M.sub.c4 = Constraint(expr= 3*M.x - 2 *M.sub.y <= 4)
M.o = Objective(expr=M.x - 4*M.sub.y)
xfrm = TransformationFactory('bilevel.linear_mpec')
xfrm.apply_to(M,options={'submodel': 'sub'})
xfrm = TransformationFactory('mpec.simple_disjunction')
xfrm.apply_to(M)
xfrm = TransformationFactory('gdp.bigm')
xfrm.apply_to(M, default_bigM=1000)
solver = SolverFactory('gurobi')
res = solver.solve(M)

print(res)
