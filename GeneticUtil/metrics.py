import Keyboard
import itertools

SAME_FINGER = 1
HAND_SWAP = 0.2
NO_ROLL = 0.6
NOT_ADJACENT = 0.1
FINGER_ORDER_FITNESS_MAX = 7
FINGER_ORDER_WEIGHTING = 1
DISTANCE_WEIGHTING = 1


def finger_order_fitness(key_order: list[int]) -> float:
    """
    Calculates the penealty of a certain finger order based on keys pressed.

    Hypothetical "perfect" finger order is no consecutive use of the same finger, all one hand, and "rolling" between adjacent fingers. This will return 0 as no penalty has been applied. Penalty will increase towards 1 as finger order gets further from this perfect order.

    Args:
        key_order: list of integers that describe which the keys being pressed; integers in [0, 29]

    Returns:
        float according to the penalty of provided finger order, scaled to be included in [0, p_max]. 
    """

    # edge case for single letter words

    key_order = [k for k, g in itertools.groupby(key_order)]  # remove duplicate from key presses

    finger_order = Keyboard.util.keys_to_fingers(key_order)

    if len(finger_order) <= 1:
        return 0

    penalty = 0
    previous_roll_trend = finger_order[1] - finger_order[0]  # calculate first trend

    for i in range(1, len(finger_order)):
        current_finger = finger_order[i]
        previous_finger = finger_order[i - 1]

        # same finger 
        if current_finger == previous_finger:
            penalty += SAME_FINGER
        else:
            # hand swap
            if previous_finger < 4 and 3 < current_finger:  # hand swap has occured
                penalty += HAND_SWAP
            # roll trend
            current_roll_trend = current_finger - previous_finger  # calculate whether roll is going left or right (postitive is right)
            if previous_roll_trend * current_roll_trend < 0:  # change in roll direction. Doesn't also penalise for same finger
                penalty += NO_ROLL
            previous_roll_trend = current_roll_trend
            # not adjacent
            if abs(current_roll_trend) > 1:
                penalty += NOT_ADJACENT

    # scale to be between 1 and p_max and return
    max_penalty = (SAME_FINGER + HAND_SWAP + NO_ROLL + NOT_ADJACENT) * (len(finger_order) - 1)

    return penalty * FINGER_ORDER_FITNESS_MAX / max_penalty


def distance_fitness(key_order: list[int]) -> float:
    """
    Calcualtes the penalty of a certain sequence of key presses based on distance travelled by the fingers.

    Hypothetical "perfect' finger placement is all on home row, with no movement of the fingers of off those keys. Penatly will increase twoards 1 as distance grows away from 0.

    Args:
        key_order: list of integers that describe which keys are being pressed in what order

    Returns:
        float according tot he penantly of provided key_order.
    """
    distance = 0
    current_finger_pos = [10, 11, 12, 13, 16, 17, 18, 19]  # all fingers on home row
    for destination_key in key_order:
        finger = Keyboard.keys.KEY_FINGERS[destination_key]
        distance += Keyboard.keys.KEY_DISTANCES[(current_finger_pos[finger]), destination_key]
        current_finger_pos[finger] = destination_key

    return distance


def score_population(pop: list[list[int]], words: list[list[int]], frequencies: list[float]) -> list[int]:
    """
    Score the given population against the distance and finger_order metrics.

    Args: 
        pop: the population of keyboards to be scored.
        words: list of words, formatted as a list of integers [0, 25] that represent letters a->b
        frequencies: list of frequencies of the given words
    
    Returns: 
        A list of scores for the respective keyboard layouts.
    """
    scores = []
    for individual in pop:
        score = 0
        for word, frequency in zip(words, frequencies):
            key_order = [individual[letter] for letter in word]
            finger_order_penalty = finger_order_fitness(key_order) * FINGER_ORDER_WEIGHTING
            distance_penalty = distance_fitness(key_order) * DISTANCE_WEIGHTING
            score += (finger_order_penalty + distance_penalty) * frequency
        scores.append(score)
    return scores
