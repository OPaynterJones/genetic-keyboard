from data.data_processing import (
    get_word_frequency_data,
    save_population,
    load_population,
)
from GeneticUtil import metrics, selection
import Keyboard
import itertools
import random


metrics.SAME_FINGER = 1.2
metrics.HAND_SWAP = 0.1
metrics.NO_ROLL = 0.7
metrics.NOT_ADJACENT = 0.1
metrics.FINGER_ORDER_FITNESS_MAX = 11
metrics.FINGER_ORDER_WEIGHTING = 0
metrics.DISTANCE_WEIGHTING = 1


# ------------------------------------------------------------

word_frequency = get_word_frequency_data()
words = [row[0] for row in word_frequency if row[3] < 70]
frequencies = [row[2] for row in word_frequency if row[3] < 70]

POP_SIZE = 150

generation = 0
population = [Keyboard.util.get_random_keyboard() for _ in range(POP_SIZE)]

qwerty_score = metrics.score_population([Keyboard.templates.QWERTY], words, frequencies)[0]


while generation < 1000:
    population_scores = metrics.score_population(population, words, frequencies)
    sorted_scores = list(sorted(zip(population_scores, range(len(population)))))

    print(f"GENERATION {generation} SCORED")
    Keyboard.util.print_keyboard(population[sorted_scores[0][1]])
    print(f"{sorted_scores[0][0]}, a {(qwerty_score - sorted_scores[0][0]) * 100 /qwerty_score}% decrease")


    # get best 2 keyboards
    best_keyboards = selection.elitist_selection(population_scores, int(POP_SIZE * 0.1))
    chosen_keyboards = selection.roulette_wheel_selection(
        population_scores, int(POP_SIZE * 0.5)
    )

    parents = [population[k] for k in set(best_keyboards + chosen_keyboards)]

    print("PARENTS SELECTED")

    # Generate new 228 children by crossover with each parent
    new_pop = [population[k] for k in best_keyboards]  # keep top 3 keyboards
    crossover_options = list(itertools.permutations(range(len(parents)), 2))
    while len(new_pop) < POP_SIZE:
        k1, k2 = random.choice(crossover_options)
        new_pop.append(
            Keyboard.util.cross_over(parents[k1], parents[k2], crossover_rate=0.8) # had at 13 with mutation at 1/10 and was jumping all over place
        )  # low crossover

    print("NEW POP CREATED")

    for i, keyboard in enumerate(new_pop):
        new_pop[i] = Keyboard.util.mutate(
            keyboard, mutation_rate=1 / 13, mutation_distance=2.5
        )  # encourage creativity

    print("MUTATED")

    save_population(generation, population, population_scores)
    print("PROGRESS SAVED")
    population = new_pop

    generation += 1
