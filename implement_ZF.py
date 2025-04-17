import numpy as np

def implement_ZF(rx_signal_Noise, c_zf, rx_sampled):
    """
    Implementation of Zero Forcing equalizer
    """
    # For each output sample, we create a sliding window of the input signal
    output = []

    # Apply the ZF filter using sliding window
    for i in range(len(rx_sampled)):
        idx_start = (i) * 2
        idx_end = idx_start + 8

        # Check if window is within bounds
        if idx_end <= len(rx_signal_Noise):
            # Get window
            window = rx_signal_Noise[idx_start:idx_end]
            # Apply ZF filter
            output.append(np.complex128(np.dot(c_zf.conj(), window)))

    return np.array(output, dtype=complex)
