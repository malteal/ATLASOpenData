
import numpy as np

def merge_dict_of_lists(sample:dict[list]):
    """
    return a dictionary with the same keys as the input dictionary, but the values are concatenated arrays.
    
    and a list of the cumulative lengths of the arrays in the input dictionary.
    """
    # merge tracks
    # Initialize an empty dictionary with the same keys
    merged = {key: np.array([]) for key in sample[0].keys()}

    # Concatenate arrays for each key
    for d in sample:
        for key in d:
            merged[key] = np.concatenate((merged[key], d[key]))
    
    # Calculate the cumulative lengths of the arrays
    keys = list(sample[0].keys())

    lengths = [len(i[keys[0]]) for i in sample]

    culens = [0] + list(np.cumsum(lengths))
    
    return merged, culens
