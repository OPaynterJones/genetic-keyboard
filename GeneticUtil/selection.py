import random


def tornament_selection(pop_size: int, n: int) -> list[int]:
    """
    Get i random selections from a population.

    Args:
        n: number of random selections to make from population.

    Returns:
        List of integer indices of random samples from population
    """

    return random.sample(range(0, pop_size), n)


def elitist_selection(scores: list[int], n: int) -> list[int]:
    """
    Select a certin number of individuals from the population that have the top n scores.

    Args:
        scores: scores of the respective individuals from the population.
        n: the number of individuals to select from the top of the population when sorted by score

    Returns:
        list of integer indeces of the top n individuals from the given population
    """

    sorted_scores = sorted(zip(scores, range(len(scores))))

    return [i for score, i in sorted_scores[:n]]


def roulette_wheel_selection(scores: list[int], n: int) -> list[int]:
    """
    Select n individuals from a population with a chance of selction proportionate to their fitness.

    Args:
        scores: list of scores of the population
        n: number of "random" selections to make

    Returns:
        list of indices of the individuals that have been selected
    """

    inversed_scores = [1 / score for score in scores]

    total_fitness = sum(inversed_scores)

    selected = set()

    while len(selected) < n:
        fitness_threshold = random.uniform(0, total_fitness)
        running_total = 0
        for index, score in enumerate(inversed_scores):
            running_total += score
            if running_total > fitness_threshold:
                selected.add(index)
                break

    return list(selected)
