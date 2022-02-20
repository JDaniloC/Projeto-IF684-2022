import csv

def real_edges_from_csv_file(real_edges_file: str) -> dict:
    """
    Reads the csv file and returns a dict of edges 
    with the real distance between the nodes.
        real_edges_file: str = csv path
    
    Returns:
        real_edges: dict = { 
            from_station: [ (to_station, distance), ...], 
            to_station: [ (from_station, distance), ...]
            ...
        }
        where the from_station and to_station are the nodes
        and the distance is the real distance between them
    """
    real_edges = {}
    with open(real_edges_file, newline = "") as csvfile:
        real_lines = csv.DictReader(csvfile)

        for line in real_lines:
            distance = float(line["cost"])
            from_station = line["from"]
            to_station = line["to"]

            if from_station not in real_edges:
                real_edges[from_station] = []
            real_edges[from_station].append((to_station, distance))
                
            if to_station not in real_edges:
                real_edges[to_station] = []
            real_edges[to_station].append((from_station, distance))
            
    return real_edges

def direct_edges_from_csv_file(direct_edges_file: str) -> dict:
    """
    Reads the csv file and returns a dict of edges 
    with the euclidean distance between the nodes.
        direct_edges_file: csv path
    
    Returns:
        direct_edges: dict = { 
            (from_station, to_station): distance, ...
        }
        where the from_station and to_station are the nodes
        and the distance is the direct distance between them
    """

    direct_edges = {}
    with open(direct_edges_file, newline = "") as csvfile:
        direct_lines = csv.DictReader(csvfile)

        for line in direct_lines:
            distance = float(line["cost"])
            from_station = line["from"]
            to_station = line["to"]

            direct_edges[(from_station, to_station)] = distance
    
    return direct_edges

def nodes_from_csv_file(nodes_file: str) -> dict:
    """
    Reads the csv file and returns a dict of nodes.
        nodes_file: csv path
    
    Returns:
        nodes: dict = {
            node: {
                "color": str
                "stations": [
                    (station, x, y), ...
                ]
            }, ...
        }
        where the node is the name of the route
        and the station is the station name
        and the x and y are the coordinates of the station
    """
    nodes = {}
    with open(nodes_file, newline = "") as csvfile:
        node_list = csv.DictReader(csvfile)

        for node in node_list:
            route = node["route"]
            color = node["color"]
            station = node["station"]
            x = float(node["x"])
            y = float(node["y"])
            if route not in nodes:
                nodes[route] = {
                    "color": color,
                    "stations": []
                }
            nodes[route]["stations"].append(
                (station, x, y)
            )
    
    return nodes