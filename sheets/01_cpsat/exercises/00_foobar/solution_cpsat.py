from data_schema import Instance, Solution
from ortools.sat.python import cp_model


def solve(instance: Instance) -> Solution:
    """
    Implement your solver for the problem here!
    """
    numbers = instance.numbers
    model = cp_model.CpModel()

    x = [model.NewBoolVar(f"x_{i}") for i in range(len(numbers))]
    y = [model.NewBoolVar(f"y_{j}") for j in range(len(numbers))]
    model.Add(sum(x) == 1)
    model.Add(sum(y) == 1)

    for i in range(len(numbers)):
        for j in range(len(numbers)):
            tmp = y[1]
            tmp2 = x[1]
            model.Maximize((x[i] * (numbers[i] - numbers [j])

    #for i in range(len(numbers))) - sum(y[i] * numbers[i] for i in range(len((numbers)))))




    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    status = solver.Solve(model)
    assert status == cp_model.OPTIMAL



    selected_values1 = [solver.Value(var) for var in x]
    selected_values2 = [solver.Value(var) for var in y]


    for i in range(len(numbers)):
        if (selected_values1[i]  == 1):
            numbers[0] = instance.numbers[i]
        if (selected_values2[i] == 1):
            numbers[1] = instance.numbers[i]




    return Solution(
        number_a=numbers[0],
        number_b=numbers[-1],
        distance=abs(numbers[0] - numbers[-1]),
    )
