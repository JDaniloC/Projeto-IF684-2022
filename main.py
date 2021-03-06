from utils import (SVGEditor, nodes_from_csv_file, real_edges_from_csv_file,
                   direct_edges_from_csv_file, calculate_time, A_star, dijkstra,
                   best_first_search, breadth_first_search, greedy_search, 
                   depth_first_search)
from flask import Flask, request, render_template


app = Flask(__name__)
TITLE = "IF684 | Paris Metro Map"
VELOCITY = 30

@app.route('/')
def index():
    return render_template('index.html', title = TITLE)

@app.route('/api/v1/')
def get_shortest_path():
    req = request.args
    result = {'route': 'null'}, 400
    algorithm = req.get('algo', 'astar')
    
    algorithms = {
        "astar": A_star,
        "dijkstra": dijkstra,
        "greedy": greedy_search,
        "dfs": depth_first_search,
        "best": best_first_search,
        "bfs": breadth_first_search,
    }

    params = {
        "edges": real_costs, 
        "h_costs": direct_costs,
        "start_node": req["start"], 
        "end_node": req["end"],
    }

    route, distance, frontiers = algorithms[algorithm](**params)
    total_time = calculate_time(route, nodes, VELOCITY, distance)
    if route != None: 
        result = {
            "route": route, 
            "frontiers": frontiers,
            "total_time": total_time,
        }, 200
    
    return result


if __name__ == "__main__":
    editor = SVGEditor("assets/image.svg", TITLE, "Intelligent Systems project")
    nodes = nodes_from_csv_file("assets/nodes.csv")
    real_costs = real_edges_from_csv_file("assets/real_cost.csv")
    direct_costs = direct_edges_from_csv_file("assets/direct_cost.csv")
    for route_name, infos in nodes.items():
        color = infos["color"]
        stations = infos["stations"]
        route_id = editor.add_new_route(route_name, color, stations)
        editor.link_points(route_id, color, stations, real_costs)

    editor.save("templates/image.svg")
    app.run(debug = True)