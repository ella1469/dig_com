import numpy as np
from qfunc import qfunc
from params import *

def calculate_SIR_DFE(c_FF_DFE, c_f, noise_variance=0.4):
    """
    Calculate Signal-to-Interference Ratio for DFE equalizer
    Assumes perfect feedback (no error propagation)
    """
    # Desired signal component
    signal_power = np.abs(np.dot(c_FF_DFE.conj().T, u0)) ** 2

    # Interference from future symbols
    interference_power = 0
    for i in range(1, c_f.shape[1]):  # Skip the first column (current symbol)
        interference_power += np.abs(np.dot(c_FF_DFE.conj().T, c_f[:, i])) ** 2

    # Noise contribution
    noise_power = noise_variance * np.linalg.norm(c_FF_DFE) ** 2

    # Total SIR
    SIR = signal_power / (interference_power + noise_power)

    P_error = qfunc(np.sqrt(SIR))
    print(f"Probability of error (P_e) calculated: {P_error:.4f}")

    theoretical_SIR = 0.0353
    print(f"SIR_DFE theoretical: {theoretical_SIR:.4f}")


    return P_error