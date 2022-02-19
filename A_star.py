import heapq
import sys    

def A_star(edges: dict, h_costs: dict, start_node: str, end_node: str):
    frontier = []
    visited = set()

    heapq.heappush(frontier, (0, 0, 0, start_node))

    previous_dict = {}
    previous_dict[start_node] = (None, 0)

    while frontier:
        f_cost, h_cost, g_cost, current_node = heapq.heappop(frontier)
        visited.add(current_node)

        if current_node == end_node:
            print("Path Found")
            print(previous_dict)
            return

        print(current_node, f_cost)

        children = edges.get(current_node)

        for child_node, edge_cost in children:
            if child_node in visited:
                continue
            
            child_g_cost = g_cost + edge_cost
            if child_node == end_node:
                child_h_cost = 0
            else:
                child_h_cost = h_costs.get((child_node, end_node)) or h_costs.get((end_node, child_node))
            child_f_cost = child_g_cost + child_h_cost
            
            if child_node in previous_dict:
                if child_g_cost > previous_dict[child_node][1]:
                    continue
            previous_dict[child_node] = (current_node, child_g_cost)
            heapq.heappush(frontier, (child_f_cost, child_h_cost, child_g_cost, child_node))


if __name__ == "__main__":
    # File with the edges of the graph (non directed)
    edges_file = open("assets/edges.csv", "r")

    # File with the straight line heuristic distances between all nodes
    h_costs_file = open("assets/h_costs.csv", "r")

    edges = {}
    h_costs = {}

    for line in edges_file:
        v1, v2, dis = line.strip().split(',')
        if v1 not in edges:
            edges[v1] = [(v2, float(dis))]
        else:
            edges[v1].append((v2,float(dis)))
            
        if v2 not in edges:
            edges[v2] = [(v1, float(dis))]
        else:
            edges[v2].append((v1, float(dis)))
            
    for line in h_costs_file:
        v1, v2, dis = line.strip().split(',')
        h_costs[(v1,v2)] = float(dis)
    
    print(edges)

    print(h_costs)

    A_star(edges=edges, h_costs=h_costs, start_node="E1", end_node="E14")