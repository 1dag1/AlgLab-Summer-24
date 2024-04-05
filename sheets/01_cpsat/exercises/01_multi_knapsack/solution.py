import itertools
import math
from typing import List

from data_schema import Instance, Item, Solution
from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver


class MultiKnapsackSolver:
    """
    This class can be used to solve the Multi-Knapsack problem
    (also the standard knapsack problem, if only one capacity is used).

    Attributes:
    - instance (Instance): The multi-knapsack instance
        - items (List[Item]): a list of Item objects representing the items to be packed.
        - capacities (List[int]): a list of integers representing the capacities of the knapsacks.
    - model (CpModel): a CpModel object representing the constraint programming model.
    - solver (CpSolver): a CpSolver object representing the constraint programming solver.
    """

    def __init__(self, instance: Instance):
        """
        Initialize the solver with the given Multi-Knapsack instance.

        Args:
        - instance (Instance): an Instance object representing the Multi-Knapsack instance.
        """
        self.items = instance.items
        self.capacities = instance.capacities
        self.model = CpModel()
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
        # TODO: Implement me!
        #Variable
        self.x = {}
        for i in range(len(self.capacities)):
            for j in range(len(self.items)):
        # self.x[i, j] = [self.model.NewBoolVar(f"x_{i}_{j}") for j in range(len(self.capacities))]
                self.x[i, j] = self.model.NewBoolVar(f"x_{i}_{j}")
        #Constraints
        for i in range(len(self.capacities)):
            self.model.Add(sum(self.x[i, j] * self.items[j].weight for j in range(len(self.items))) <= self.capacities[i])
            #self.model.Add(sum(x[i][j] * i.weight for x, i in zip(self.x, self.items)) <= self.capacities[j])
        for j in range(len(self.items)):
            self.model.Add(sum(self.x[i, j] for i in range(len(self.capacities))) <= 1)

        for j in range(len(self.items)):
            self.model.Maximize(sum(self.items[j].value * self.x[i, j] for j in range(len(self.items)) for i in range(len(self.capacities))))

    def solve(self, timelimit: float = math.inf) -> Solution:
        """
        Solve the Multi-Knapsack instance with the given time limit.

        Args:
        - timelimit (float): time limit in seconds for the cp-sat solver.

        Returns:
        - Solution: a list of lists of Item objects representing the items packed in each knapsack
        """
        # handle given time limit
        if timelimit <= 0.0:
            return Solution(knapsacks=[])  # empty solution
        elif timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        # TODO: Implement me!
        status = self.solver.Solve(self.model)

        tmp3 = range(len(self.capacities))
        knapsack = list()
        for i in range(len(self.capacities)):
            knapsack.append(list())
        k = 0
       # selected_values1 = [self.solver.Value(var) for var in x]
        for i in range(len(self.capacities)):
            for j in range(len(self.items)):
                tmp4 = self.solver.Value(self.x[i, j])
                if (self.solver.Value(self.x[i, j]) == 1):

                    knapsack[i].append(self.items[j])
                    k = k+1

        return Solution(knapsacks=knapsack)  # empty solution
