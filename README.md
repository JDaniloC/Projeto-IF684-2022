# IF684 A* at Paris Station
Project with the goal to find the shortest path between two stations in the Paris Metro, using the A* algorithm, generating a map of the stations and their routes.

## How to install

Run the following command in your terminal, to install the python dependencies:

```bash
pip install -r requirements.txt
```

## CSV files

The `real_cost.csv` file contains the information about the **real routes** between the stations, with the cost to go from one station to another. The `direct_cost.csv` file contains the information about the **euclidean distance** between all stations.