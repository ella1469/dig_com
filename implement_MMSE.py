import numpy as np


def implement_MMSE(input_signal, h_MMSE, window_size=8):
    """
    Implementation of MMSE equalizer
    """
    # For each output sample, we create a sliding window of the input signal
    output_length = len(input_signal) - window_size + 1
    output = np.zeros(output_length, dtype=complex)

    # Apply the MMSE filter using sliding window
    for i in range(output_length):
        window = input_signal[i:i + window_size]
        output[i] = np.dot(h_MMSE.conj(), window)

    return output