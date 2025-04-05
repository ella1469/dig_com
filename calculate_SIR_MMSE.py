import numpy as np
from qfunc import qfunc
from params import *

def calculate_SIR_MMSE(c_MMSE, U, noise_variance=0.4):
    """
    Calculate Signal-to-Interference Ratio for MMSE equalizer
    """
    # Desired signal component
    signal_power = np.abs(np.dot(c_MMSE.conj().T, u0)) ** 2

    # Interference from other symbols
    interference_power = 0
    for i in range(U.shape[1]):
        if i != col//2:  # Skip the desired symbol
            interference_power += np.abs(np.dot(c_MMSE.conj().T, U[:, i])) ** 2

    # Noise contribution using noise_variance_matrix
    noise_variance_matrix = noise_variance * np.eye(len(c_MMSE))  # Create a diagonal matrix
    noise_power = np.real(c_MMSE.conj().T @ noise_variance_matrix @ c_MMSE)

    # Total SIR
    SIR = signal_power / (interference_power + noise_power)

    P_error = qfunc(np.sqrt(SIR))
    print(f"Probability of error (P_e) calculated: {P_error:.4f}")

    theoretical_SIR = 0.0635 

    print(f"SIR_ZF theoretical: {theoretical_SIR:.4f}")

    return P_error
