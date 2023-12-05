from .keys import KEY_FINGERS, KEY_DISTANCES
import random


def print_keyboard(letter_key_locations: list[int]):
    """
    Prints given keyboard.

    Args:
        letter_key_locations:
            The keyboard layout in terms of the keys assigned to each letter. 26 elements long.
    """

    key_letters = [" "] * 30

    for letter, key in enumerate(letter_key_locations):
        if key >= 0:
            key_letters[key] = chr(ord("a") + letter)

    print(
        f""" 
            ,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,
            |1/2| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | + | ' | <-    |
            |---'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-----|
            |     | {key_letters[0]} | {key_letters[1]} | {key_letters[2]} | {key_letters[3]} | {key_letters[4]} | {key_letters[5]} | {key_letters[6]} | {key_letters[7]} | {key_letters[8]} | {key_letters[9]} | ] | ^ |     |
            |-----',--',--',--',--',--',--',--',--',--',--',--',--'|    |
            | Caps | {key_letters[10]} | {key_letters[11]} | {key_letters[12]} | {key_letters[13]} | {key_letters[14]} | {key_letters[15]} | {key_letters[16]} | {key_letters[17]} | {key_letters[18]} | {key_letters[19]} | [ | * |    |
            |----,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'---'----|
            |    | < | {key_letters[20]} | {key_letters[21]} | {key_letters[22]} | {key_letters[23]} | {key_letters[24]} | {key_letters[25]} | {key_letters[26]} | {key_letters[27]} | {key_letters[28]} | {key_letters[29]} |          |
            |----'-,-',--'--,'---'---'---'---'---'---'-,-'---',--,------|
            | ctrl |  | alt |                          |altgr |  | ctrl |
            '------'  '-----'--------------------------'------'  '------' 
"""
    )


def keys_to_fingers(key_order: list[int]) -> list[int]:
    """
    Transforms an order of key presses into an order of finger presses.

    Args:
        key_order: which keys are pressed in which order, keys from [0, 29]

    Returns:
        List of integers representing which fingers are used to push the given keys, from [0, 7]
    """

    return [KEY_FINGERS[k] for k in key_order]


def get_random_keyboard() -> list[int]:
    """
    Generate a random keyboard.

    Returns:
        A random list of length 26 of integers in [0, 29].
    """

    return random.sample(range(30), 26)


def is_valid_layout(layout: list[int]) -> bool:
    """
    Checks if keyboard layout is valid
    """
    if not len(set(layout)) == 26:  # check for length and duplicates
        return False

    if not all((isinstance(x, int) for x in layout)):
        return False

    for key in layout:
        if not 0 <= key < 30:  # check keys are right
            return False

    return True


def cross_over(k_a: list[int], k_b: list[int], crossover_rate=0.75) -> list[int]:
    """
    Crossover function for two keyboards.

    Implements a varition of the partially mapped crossover (PMX) algorithm to merge two keyboards, A and B. A should generally be the superior keyboard, as PMX will preserve more of this keyboard

    Args:
        k_a: keyboard A to crossover with B. Generally the superior keyboard layout,
        k_b: keyboard B to crossover with A.
        k_a_pres_minimum: chance of a gene being taken from A - the higher the crossover the rate the more k_a influences the child

    Returns:
        New keyboard that's a crossover of A and B.
    """

    

    available_keys = set(range(30))
    available_letters = set(range(26))
    child = [-1] * 26

    genes_from_a = []
    for gene in range(26): 
        if random.random() < crossover_rate: 
            genes_from_a.append(gene)

    # copy random genes from A
    for gene_i in genes_from_a:
        child[gene_i] = k_a[gene_i]
        available_keys.remove(k_a[gene_i])
        available_letters.remove(gene_i)

    # try to fill in the rest from B if key hasn't already been filled by A
    for i, key in enumerate(child):
        if key < 0:
            if k_b[i] in available_keys:
                child[i] = k_b[i]
                available_keys.remove(k_b[i])
                available_letters.remove(i)

    for letter in available_letters:
        intended_location = k_b[letter]  # place has been filled in new keyboard
        # look for minimum distance
        min_distance = float("inf")
        closest_key = -1
        for key in available_keys:
            distance = KEY_DISTANCES[(intended_location, key)]
            if distance < min_distance:
                min_distance = distance
                closest_key = key

        child[letter] = closest_key
        available_keys.remove(closest_key)

    return child


def mutate(keyboard: list[int], mutation_rate: float = 1/26, mutation_distance=1.7) -> list[int]: 
    """ 
    Mutates given keybaord. 

    Mutates a given keyboard by swapping keys based on the probablity hyperparameter.

    Args: 
        mutation_rate: the probability of a key swapping with another key
        mutation_distance: the distance around the key that's mutating that can be swapped with it. (1 key radius < 1.7; 2 key radius < 2.5)
    Returns: 
        potentially mutated keyboard
    """

    for letter, current_key in enumerate(keyboard): 
        if random.random() < mutation_rate: # swap key
            close_keys = [key for key in range(30) if KEY_DISTANCES[(current_key, key)] < mutation_distance]
            mutating_to = random.choice(close_keys)
            if mutating_to in keyboard: 
                keyboard[letter], keyboard[keyboard.index(mutating_to)] = mutating_to, current_key
            else: 
                keyboard[letter] = mutating_to

    return keyboard
    
