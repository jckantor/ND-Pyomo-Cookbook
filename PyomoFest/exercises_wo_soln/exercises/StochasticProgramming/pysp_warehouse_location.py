from warehouse_location import model

def pysp_instance_creation_callback(scenario_name, node_list):
    scenario = model.clone()
    assert scenario_name in ("s1","s2")
    if scenario_name == "s2":
        w = "Harlingen"
        for c in ["NYC", "LA", "Chicago"]:
            scenario.d[w,c] = scenario.d[w,c].value + 1000
    return scenario
