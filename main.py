from utils import (SVGEditor, nodes_from_csv_file, real_edges_from_csv_file,
                   direct_edges_from_csv_file, A_star)
from flask import Flask, request, render_template


app = Flask(__name__)
TITLE = "IF684 | Paris Metro Map"

@app.route('/')
def index():
    return render_template('index.html', title = TITLE)

@app.route('/api/v1/')
def get_shortest_path():
    req = request.args
    result = {'route': 'null'}, 400
    
    route, distance = A_star(edges = real_costs, 
        h_costs = direct_costs, start_node = req['start'], 
        end_node = req['end'], verbose = True)
    if route != None: 
        result = {
            "route": route, 
            "distance": distance
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
    app.run(debug=True)