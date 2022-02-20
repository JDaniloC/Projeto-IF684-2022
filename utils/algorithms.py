from . import real_edges_from_csv_file, direct_edges_from_csv_file
import heapq, datetime

def A_star(edges: dict, h_costs: dict, start_node: str, 
           end_node: str, verbose: bool = False) -> tuple:
    frontier = []
    visited = set()

    # Heap used for the frontier, values are always (f_cost, h_cost, g_cost, node)
    heapq.heappush(frontier, (0, 0, 0, end_node))

    # Dictionary used to find and store the shortest path, each node points to the previous node and stores g_cost
    previous_dict = {}
    previous_dict[end_node] = (None, 0)
    frontiers = []

    while frontier:
        frontiers.append(list(map(
            lambda x: (x[-1], round(x[0], 2)
        ), frontier)))
        f_cost, h_cost, g_cost, current_node = heapq.heappop(frontier)
        visited.add(current_node)

        if verbose:
            print(f_cost, h_cost, g_cost, current_node)

        if current_node == start_node:
            result = []

            while current_node:
                result.append(current_node)
                current_node = previous_dict[current_node][0]          

            return result, previous_dict[start_node][1], frontiers

        children = edges.get(current_node)

        for child_node, edge_cost in children:
            if child_node in visited:
                continue
            
            child_g_cost = g_cost + edge_cost
            if child_node == start_node:
                child_h_cost = 0
            else:
                child_h_cost = h_costs.get((child_node, start_node)) or h_costs.get((start_node, child_node))
            child_f_cost = child_g_cost + child_h_cost
            
            if child_node in previous_dict:
                if child_g_cost > previous_dict[child_node][1]:
                    continue
            previous_dict[child_node] = (current_node, child_g_cost)
            heapq.heappush(frontier, (child_f_cost, child_h_cost, child_g_cost, child_node))

def best_first_search(edges: dict, h_costs: dict, start_node: str, 
                      end_node: str, verbose: bool = False) -> tuple:
    frontier = []
    visited = set()

    # Heap used for the frontier, values are always (h_cost, g_cost, node)
    heapq.heappush(frontier, (0, 0, end_node))

    # Dictionary used to find and store the shortest path, each node points to the previous node and stores g_cost
    previous_dict = {}
    previous_dict[end_node] = (None, 0)
    frontiers = []

    while frontier:
        frontiers.append(list(map(
            lambda x: (x[-1], round(x[0], 2)
        ), frontier)))
        h_cost, g_cost, current_node = heapq.heappop(frontier)
        visited.add(current_node)

        if verbose:
            print(h_cost, g_cost, current_node)

        if current_node == start_node:
            result = []

            while current_node:
                result.append(current_node)
                current_node = previous_dict[current_node][0]          

            return result, previous_dict[start_node][1], frontiers

        children = edges.get(current_node)

        for child_node, edge_cost in children:
            if child_node in visited:
                continue
            
            child_g_cost = g_cost + edge_cost
            if child_node == start_node:
                child_h_cost = 0
            else:
                child_h_cost = h_costs.get((child_node, start_node)) or h_costs.get((start_node, child_node))
            
            if child_node in previous_dict:
                if child_g_cost > previous_dict[child_node][1]:
                    continue
            previous_dict[child_node] = (current_node, child_g_cost)
            heapq.heappush(frontier, (child_h_cost, child_g_cost, child_node))

def breadth_first_search(edges: dict, start_node: str, 
                         end_node: str, verbose: bool = False) -> tuple:
    frontier = []
    visited = set()

    # list used for the frontier, values are always (g_cost, node) (no priority)
    frontier.append((0, end_node))

    # Dictionary used to find and store the shortest path, each node points to the previous node and stores g_cost
    previous_dict = {}
    previous_dict[end_node] = (None, 0)
    frontiers = []

    visited.add(end_node)

    while frontier:
        frontiers.append(list(map(
            lambda x: (x[-1], round(x[0], 2)
        ), frontier)))
        g_cost, current_node = frontier.pop(0)
        
        if verbose:
            print(g_cost, current_node)

        if current_node == start_node:
            result = []

            while current_node:
                result.append(current_node)
                current_node = previous_dict[current_node][0]          

            return result, previous_dict[start_node][1], frontiers

        children = edges.get(current_node)

        for child_node, edge_cost in children:
            if child_node in visited:
                continue
            
            visited.add(child_node)
            child_g_cost = g_cost + edge_cost
            previous_dict[child_node] = (current_node, child_g_cost)
            frontier.append((child_g_cost, child_node))           

def greedy_search(edges: dict, start_node: str, end_node: str, 
                  verbose: bool = False) -> tuple:
    frontier = []
    visited = set()

    # Heap used for the frontier, values are always (proximity, g_cost, node)
    heapq.heappush(frontier, (0, 0, end_node))

    # Dictionary used to find and store the shortest path, each node points to the previous node and stores g_cost
    previous_dict = {}
    previous_dict[end_node] = (None, 0)
    frontiers = []

    while frontier:
        frontiers.append(list(map(
            lambda x: (x[-1], round(x[0], 2)
        ), frontier)))
        proximity, g_cost, current_node = heapq.heappop(frontier)
        
        if verbose:
            print(proximity, g_cost, current_node)

        visited.add(current_node)

        if current_node == start_node:
            result = []

            while current_node:
                result.append(current_node)
                current_node = previous_dict[current_node][0]          

            return result, previous_dict[start_node][1], frontiers

        children = edges.get(current_node)

        for child_node, edge_cost in children:
            if child_node in visited:
                continue

            child_g_cost = g_cost + edge_cost
            child_proximity = edge_cost
            
            previous_dict[child_node] = (current_node, child_g_cost)
            heapq.heappush(frontier, (child_proximity, child_g_cost, child_node))             

def dijkstra(edges: dict, start_node: str, end_node: str, 
             verbose: bool = False) -> tuple:
    frontier = []
    visited = set()

    # Heap used for the frontier, values are always (g_cost, node)
    heapq.heappush(frontier, (0, end_node))

    # Dictionary used to find and store the shortest path, each node points to the previous node and stores g_cost
    previous_dict = {}
    previous_dict[end_node] = (None, 0)
    frontiers = []

    while frontier:
        frontiers.append(list(map(
            lambda x: (x[-1], round(x[0], 2)
        ), frontier)))
        g_cost, current_node = heapq.heappop(frontier)
        visited.add(current_node)

        if verbose:
            print(g_cost, current_node)

        if current_node == start_node:
            result = []

            while current_node:
                result.append(current_node)
                current_node = previous_dict[current_node][0]          

            return result, previous_dict[start_node][1], frontiers

        children = edges.get(current_node)

        for child_node, edge_cost in children:
            if child_node in visited:
                continue
            
            child_g_cost = g_cost + edge_cost

            if child_node in previous_dict:
                if child_g_cost > previous_dict[child_node][1]:
                    continue
            previous_dict[child_node] = (current_node, child_g_cost)
            heapq.heappush(frontier, (child_g_cost, child_node))

def calculate_time(stations: list, lines: dict, 
    velocity: float, distance: float) -> float:
    """
    Calculates the time to travel from one station to another.
    """

    if len(stations) <= 1: return 0

    station_changes = 0
    current_line = None

    for key, values in lines.items():
        lines[key]["stations"] = set(map(lambda x: x[0], values["stations"]))

    for index in range(len(stations) - 1):
        next_station = stations[index + 1]
        if current_line is None or (
            next_station not in lines[current_line]["stations"]
        ):
            for line, values in lines.items():
                if (stations[index] in values["stations"] and 
                    next_station in values["stations"]):
                    if current_line is not None:
                        station_changes += 1
                    current_line = line
                    break

    time_in_hours = distance / velocity
    time_in_minutes = 4 * station_changes + time_in_hours * 60
    return str(datetime.timedelta(minutes = time_in_minutes))

if __name__ == "__main__":
    edges = real_edges_from_csv_file("assets/real_cost.csv")
    h_costs = direct_edges_from_csv_file("assets/direct_cost.csv")
    
    result_list, result_distance = A_star(edges=edges, h_costs=h_costs, start_node="E1", end_node="E14", verbose=True)
    print("A_star:", result_distance)
    print(" -> ".join(result_list), end="\n\n")

    result_list, result_distance = breadth_first_search(edges=edges, start_node="E1", end_node="E14", verbose=True)
    print("breadth_first_search:", result_distance)
    print(" -> ".join(result_list), end="\n\n")

    result_list, result_distance = best_first_search(edges=edges, h_costs=h_costs, start_node="E1", end_node="E14", verbose=True)
    print("best_first_search:", result_distance)
    print(" -> ".join(result_list), end="\n\n")

    result_list, result_distance = greedy_search(edges=edges, start_node="E1", end_node="E14", verbose=True)
    print("greedy_search:", result_distance)
    print(" -> ".join(result_list), end="\n\n")

    result_list, result_distance = dijkstra(edges=edges, start_node="E1", end_node="E14", verbose=True)
    print("dijkstra:", result_distance)
    print(" -> ".join(result_list), end="\n\n")
            