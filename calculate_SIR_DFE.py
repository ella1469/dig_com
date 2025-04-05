import numpy as np


def calculate_SIR_DFE(h_FF_DFE, U_f, noise_variance=0.4):
    """
    Calculate Signal-to-Interference Ratio for DFE equalizer
    Assumes perfect feedback (no error propagation)
    """
    # Desired signal component
    u_0 = U_f[:, 0]  # First column of U_f is the current symbol
    signal_power = np.abs(np.dot(h_FF_DFE.conj().T, u_0)) ** 2

    # Interference from future symbols
    interference_power = 0
    for i in range(1, U_f.shape[1]):  # Skip the first column (current symbol)
        interference_power += np.abs(np.dot(h_FF_DFE.conj().T, U_f[:, i])) ** 2

    # Noise contribution
    noise_power = noise_variance * np.linalg.norm(h_FF_DFE) ** 2

    # Total SIR
    SIR = signal_power / (interference_power + noise_power)

    # השוואה לערך התיאורטי (אם יש)
    print(f"SIR_DFE calculated: {SIR:.4f}")

    return SIR