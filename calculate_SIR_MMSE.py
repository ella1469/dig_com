import numpy as np

def calculate_SIR_MMSE(h_MMSE, U, noise_variance=0.4):
    """
    Calculate Signal-to-Interference Ratio for MMSE equalizer
    """
    # Desired signal component
    u_0 = U[:, 2]  # The middle column corresponds to the current symbol
    signal_power = np.abs(np.dot(h_MMSE.conj().T, u_0)) ** 2

    # Interference from other symbols
    interference_power = 0
    for i in range(U.shape[1]):
        if i != 2:  # Skip the desired symbol
            interference_power += np.abs(np.dot(h_MMSE.conj().T, U[:, i])) ** 2

    # Noise contribution
    noise_power = noise_variance * np.linalg.norm(h_MMSE) ** 2

    # Total SIR
    SIR = signal_power / (interference_power + noise_power)

    # השוואה לערך התיאורטי (אם יש)
    print(f"SIR_MMSE calculated: {SIR:.4f}")

    return SIR
