import networkx

t = networkx.DiGraph()

# add root
t.add_node("root",
           variables=["y"],
           cost="stage_cost[1]")

# scenario 1
t.add_node("s1",
           variables=["x"],
           cost="stage_cost[2]")
t.add_edge("root", "s1",
           weight=0.4)

# scenario 2
t.add_node("s2",
           variables=["x"],
           cost="stage_cost[2]")
t.add_edge("root", "s2",
           weight=0.6)
