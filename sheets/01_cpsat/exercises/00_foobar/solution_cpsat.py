from data_schema import Instance, Solution
from ortools.sat.python import cp_model


def solve(instance: Instance) -> Solution:
    """
    Implement your solver for the problem here!
    """
    numbers = instance.numbers
    model = cp_model.CpModel()
    
    #variables
    x = [model.NewBoolVar(f"x_{i}") for i in range(len(numbers))]
    y = [model.NewBoolVar(f"y_{j}") for j in range(len(numbers))]
    
    #constraints
    model.Add(sum(x) == 1)
    model.Add(sum(y) == 1)

    #objective
    model.Maximize(sum(n * numbers[i] for n, i in zip(x, range(len(numbers)))) - sum(m * numbers[k] for m, k in zip(y, range(len(numbers)))))

    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    status = solver.Solve(model)
    assert status == cp_model.OPTIMAL

    selected_values1 = [solver.Value(var) for var in x]
    selected_values2 = [solver.Value(var) for var in y]

    solNum1 = []
    solNum2 = []
    for i in range(len(numbers)):
        if (selected_values1[i]  == 1):
            solNum1 = instance.numbers[i]
        if (selected_values2[i] == 1):
            solNum2 = instance.numbers[i]

    numbers[0] = solNum1
    numbers[-1] = solNum2

    return Solution(
        number_a=numbers[0],
        number_b=numbers[-1],
        distance=abs(numbers[0] - numbers[-1]),
    )
