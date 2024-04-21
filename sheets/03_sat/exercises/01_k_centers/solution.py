import math
from typing import Dict, Iterable, List

import networkx as nx
from ortools.math_opt.python import solution
from pysat.solvers import Solver as SATSolver



class KCentersSolver:
    def __init__(self, graph: nx.Graph) -> None:
        """
        Creates a solver for the k-centers problem on the given networkx graph.
        The graph is not necessarily complete, so not all nodes are neighbors.
        The distance between two neighboring nodes is a numeric value (int / float), saved as
        an edge data parameter called "weight".
        There are multiple ways to access this data, and networkx also implements
        several algorithms that automatically make use of this value.
        Check the networkx documentation for more information!
        """
        self.graph = graph
        self.numNodes = self.graph.number_of_nodes()
        self.distanceMatrix = dict(nx.all_pairs_dijkstra_path_length(graph))
        self.UpperBound = None

        # TODO: Implement me!

    def solve_heur(self, k: int) -> List[int]:
        """
        Calculate a heuristic solution to the k-centers problem.
        Returns the k selected centers as a list of ints.
        (nodes will be ints in the given graph).
        """
        # TODO: Implement me!
        centers = []

        #First Center
        centers.append(1)


        maxDistSol = None
        maxDist = 0
        numCenters = 1

        while numCenters < k:
            for node in range(1, self.numNodes + 1):
                dijkstraSol = nx.multi_source_dijkstra(self.graph, centers, node)
                minDistfromCenters = dijkstraSol[0]
                if (minDistfromCenters > maxDist):
                    maxDistNode = node
                    maxDist = minDistfromCenters
                    self.UpperBound = dijkstraSol[0]
            centers.append(maxDistNode)
            numCenters += 1
            maxDist = 0


        for node in range(1, self.numNodes + 1):
            dijkstraSol = nx.multi_source_dijkstra(self.graph, centers, node)
            minDistfromCenters = dijkstraSol[0]
            if (minDistfromCenters > maxDist):
                maxDist = minDistfromCenters
                self.UpperBound = minDistfromCenters
        return centers

    def solve(self, k: int) -> List[int]:
        """
        For the given parameter k, calculate the optimal solution
        to the k-centers solution and return the selected centers as a list.
        """
        sat = SATSolver("MiniCard")
        centers = self.solve_heur(k)

        # TODO: Implement me!
        allNodes = set(x for x in range(1, self.graph.number_of_nodes() + 1))

        variables = [x for x in allNodes]

        sat.add_atmost(variables, k)
        while sat.solve():

            maxDist2 = 0
            for node in range(1, self.numNodes + 1):
                dijkstraSol = nx.multi_source_dijkstra(self.graph, centers, node)
                minDistfromCenters = dijkstraSol[0]
                if (minDistfromCenters > maxDist2):

                    maxDist2 = minDistfromCenters
                    self.UpperBound = dijkstraSol[0]

            maxDistNode= None

            nodesInRadius = []
            for node1 in range(1, self.numNodes + 1):
                for node2 in range(1, self.numNodes + 1):
                    nodeDistance = self.distanceMatrix[node1][node2]

                    if (nodeDistance < self.UpperBound - 0.000001):
                        nodesInRadius.append(node2)
                sat.add_clause(nodesInRadius)
                nodesInRadius.clear()



            if sat.solve():
                centers.clear()
                solution = sat.get_model()
                for x in solution:
                    if x > 0:
                        centers.append(x)
                continue


            else:
               return centers

