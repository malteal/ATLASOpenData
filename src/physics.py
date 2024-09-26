
import numpy as np


def theta_to_eta(theta:float) -> float:
    return -1*np.log(np.tan(theta/2))

def delta_R(jet_eta:float, jet_phi:float, cnsts_eta:float, cnsts_phi:float) -> float:
    deta = jet_eta - cnsts_eta
    dphi = jet_phi - cnsts_phi
    return np.sqrt(deta**2 + dphi**2)

def qOverP_to_pT(qOverP: float, phi: float,
                 abs_bool: bool = True) -> float:
    """
    Converts qOverP to pT using the given formula.

    Parameters:
    qOverP (float): The qOverP value.
    phi (float): The phi value.
    abs_bool (bool, optional): If True, returns the absolute value of the result. 
                               If False, returns the result without taking the absolute value. 
                               Defaults to True.

    Returns:
    float: The pT value calculated using the given formula.
    """
    p = 1 / qOverP
    if abs_bool:
        return np.abs(np.sin(phi) * p)
    else:
        return np.cos(phi) * p
