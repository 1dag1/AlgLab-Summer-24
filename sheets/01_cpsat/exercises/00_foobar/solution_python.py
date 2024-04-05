from data_schema import Instance, Solution


def solve(instance: Instance) -> Solution:
    """
    Implement your solver for the problem here!
    """
    numbersToCheck = instance.numbers
    minimum = min(numbersToCheck)
    maximum = max(numbersToCheck)
    instance.numbers[0] = minimum
    instance.numbers[-1] = maximum

    numbers = instance.numbers
    return Solution(
        number_a=numbers[0],
        number_b=numbers[-1],
        distance=abs(numbers[0] - numbers[-1]),
    )
