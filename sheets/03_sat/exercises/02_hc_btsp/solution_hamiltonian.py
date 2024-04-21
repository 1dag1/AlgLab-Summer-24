import itertools
from typing import List, Optional, Tuple

import networkx as nx
from pysat.solvers import Solver as SATSolver


class HamiltonianCycleModel:
    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph
        self.solver = SATSolver("Minicard")
        self.assumptions = []
        self.num_vertices = len(self.graph)
        # TODO: Implement me!


    def solve(self) -> Optional[List[Tuple[int, int]]]:
        """
        Solves the Hamiltonian Cycle Problem. If a HC is found,
        its edges are returned as a list.
        If the graph has no HC, 'None' is returned.
        """
        # TODO: Implement me!
        clauses = []
        # Each vertex must appear in the cycle
        for v in range(self.num_vertices):
            clause = []
            for i in range(self.num_vertices):
                clause.append((v * self.num_vertices) + i + 1)
            clauses.append(clause)

        # No two vertices in the cycle can appear at the same position
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if i != j:
                    for k in range(self.num_vertices):
                        clauses.append([-((i * self.num_vertices) + j + 1), -((j * self.num_vertices) + k + 1)])
                        clauses.append([-((j * self.num_vertices) + i + 1), -((k * self.num_vertices) + j + 1)])

        # No two vertices in the cycle can be adjacent if there's no edge between them
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if not self.graph.has_edge(i, j) and i != j:
                    for k in range(self.num_vertices - 1):
                        clauses.append([-((i * self.num_vertices) + k + 1), -((j * self.num_vertices) + k + 2)])


        for clause in clauses:
            self.solver.add_clause(clause)

        if self.solver.solve():
            cycle = []
            for v in range(self.num_vertices):
                for i in range(self.num_vertices):
                    if self.solver.get_model()[v * self.num_vertices + i] > 0:
                        cycle.append(i)
                        break
            return cycle
        else:
            return None