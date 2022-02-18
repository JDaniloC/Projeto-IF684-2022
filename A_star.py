import heapq

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
        if v1 not in h_costs:
            h_costs[v1] = [(v2, float(dis))]
        else:
            h_costs[v1].append((v2, float(dis)))
            
        if v2 not in h_costs:
            h_costs[v2] = [(v1, float(dis))]
        else:
            h_costs[v2].append((v1,float(dis)))