'utils'


from pathlib import Path
import uproot
import numpy as np


def get_all_files(path:str, extension:str) -> list:
    """
    Get all files in a directory with a specific extension.

    Parameters:
    path (str): The path to the directory.
    extension (str): The extension of the files.

    Returns:
    list: A list of all files in the directory with the given extension.
    """
    return list(Path(path).rglob(extension))


def create_root_keys(vars_dict: dict) -> list:
    """
    Generate a list of keys based on the input dictionary. Each key in the dictionary
    is combined with its corresponding list elements to form new keys.

    Parameters:
    vars_dict (dict): A dictionary where each key is associated with a list of elements.

    Returns:
    list: A list of strings where each string is a combination of a dictionary key and its list elements.

    Raises:
    NotImplementedError: If any list in the dictionary is empty, the function raises a NotImplementedError.

    Example:
    >>> vars_dict = {
    ...     "key1": ["a", "b"],
    ...     "key2": ["c"],
    ...     "key3": []
    ... }
    >>> try:
    ...     result = create_root_keys(vars_dict)
    ... except NotImplementedError as e:
    ...     print(e)
    NotImplementedError: Empty list not implemented yet
    """
    vars_lst = []
    vars_lst_all = []

    for key, lst in vars_dict.items():
        if len(lst) == 0:
            vars_lst_all.append(key)
            raise NotImplementedError('Empty list not implemented yet')
        else:
            vars_lst.extend([f'{key}.{i}' for i in lst])

    return vars_lst, vars_lst_all

def load_root(root_paths: list | str, variable_list: list, tree_name: str):
    """
    Retrieve data from ROOT files.

    Parameters:
    root_paths (list): List of paths to search for ROOT files.
    variable_list (list): List of variables to extract from the ROOT files.
    tree_name (str): Name of the tree within the ROOT files to extract data from.

    Returns:
    dict: Dictionary containing the extracted data arrays.
    """
    if isinstance(root_paths, str):
        root_paths = list(Path(root_paths).rglob("*.root*"))[:1]
    
    selected_vars, all_vars = create_root_keys(variable_list)
    
    for root_path in root_paths:
        root_tree = uproot.open(root_path)[tree_name]
        root_tree_keys = root_tree.keys()
        
        all_vars = [key for key in root_tree_keys if np.isin(all_vars, key.split('.')[0]).any() & (('/') not in key)]
        
        tree_data = root_tree.arrays(selected_vars + all_vars)

    return tree_data