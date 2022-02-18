import heapq

if __name__ == "__main__":
    real = open("real.csv", "r")
    diretas = open("diretas.csv", "r")

    graph = {}
    distances_direct = {}

    for line in real:
        v1, v2, dis = line.strip().split(',')
        if v1 not in graph:
            graph[v1] = [(v2, float(dis))]
        else:
            graph[v1].append((v2,float(dis)))
            
        if v2 not in graph:
            graph[v2] = [(v1, float(dis))]
        else:
            graph[v2].append((v1,float(dis)))
            
    for line in diretas:
        v1, v2, dis = line.strip().split(',')
        if v1 not in distances_direct:
            distances_direct[v1] = [(v2, float(dis))]
        else:
            distances_direct[v1].append((v2,float(dis)))
            
        if v2 not in distances_direct:
            distances_direct[v2] = [(v1, float(dis))]
        else:
            distances_direct[v2].append((v1,float(dis)))
            
    
