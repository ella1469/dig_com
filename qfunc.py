import numpy as np
from scipy.special import erfc

def qfunc(x):
    """
    Implementation of Q function
    """
    return 0.5 * erfc(x / np.sqrt(2))
