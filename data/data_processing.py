import numpy as np
import h5py


def _convert_count(c):
    return int(c.decode().replace(",", ""))


def _convert_percent(p):
    return float(p.decode().replace("%", ""))


def get_word_frequency_data(ascii_codes=True):
    arr = np.loadtxt(
        "data/frequency-alpha-alldicts.txt",
        skiprows=1,
        usecols=range(1, 5),
        converters={2: _convert_count, 3: _convert_percent, 4: _convert_percent},
        dtype=object,
    ).tolist()

    if not ascii_codes:
        return arr

    for row in arr:
        row[0] = [ord(c) - ord("a") for c in row[0].lower()]

    return arr


def save_population(pop_n: int, population: list[list[int]], scores: list[int]):
    with h5py.File("data/GK_pop_data.hdf5", "a") as f:
        if f'population_{pop_n}' in f:
            del f[f'population_{pop_n}']
        pop_group = f.create_group(f'population_{pop_n}')

        pop_group.create_dataset('population', data=population)
        pop_group.create_dataset('scores', data=scores)




def load_population(pop_n: int) -> tuple[list[list[int]], list[int]]:
    """
    Loads population

    Args:
        pop_n: the population number to load

    Returns:
        Tuple of population and scores (poulation, scores)
    """

    with h5py.File("data/GK_pop_data.hdf5", "r") as f:
        pop_group = f[f'population_{pop_n}']

        population = pop_group['population'][:]
        scores = pop_group['scores'][:]

    return population, scores
