from utils import nodes_from_csv_file, real_edges_from_csv_file
from generator import SVGEditor

if __name__ == "__main__":
    editor = SVGEditor("assets/image.svg", "Paris Metro Map", 
                       "Intelligent Systems project")
    nodes = nodes_from_csv_file("assets/nodes.csv")
    real_costs = real_edges_from_csv_file("assets/real_cost.csv")
    for route_name, infos in nodes.items():
        color = infos["color"]
        stations = infos["stations"]
        route_id = editor.add_new_route(route_name, color, stations)
        editor.link_points(route_id, color, stations, real_costs)

    editor.save("result.svg")