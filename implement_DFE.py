import numpy as np


def implement_DFE(rx_signal_Noise, c_FF, c_FB, rx_sampled):
    """
    Implementation of MMSE-DFE equalizer, with corrections to match MATLAB behavior

    Parameters:
    rx_signal_Noise - The received signal with noise
    c_FF - Feedforward filter coefficients
    c_FB - Feedback filter coefficients
    rx_sampled - Sampled received signal

    Returns:
    Array of equalized output samples
    """
    output = []

    # Apply the MMSE-DFE filter using sliding window
    for i in range(len(rx_sampled)):
        idx_start = (i) * 2
        idx_end = idx_start + 8

        # Check if window is within bounds
        if idx_end <= len(rx_signal_Noise):
            # Get window for feedforward filter
            window = rx_signal_Noise[idx_start:idx_end]

            # Apply feedforward filter (similar to MMSE)
            ff_output = np.dot(c_FF.conj().flatten(), window)

            output.append(ff_output)
            # Only apply feedback after we have enough samples
            if i >= 2 and len(c_FB) > 0:
                # Use sign() of past outputs
                past_signs = np.sign(np.real(output[i-2:i])) + 1j * np.sign(np.imag(output[i-2:i]))

                # Apply feedback filter to past outputs
                fb_output = np.dot(c_FB.flatten(), past_signs)

                # Combine feedforward and feedback outputs
                output[i] = output[i] + fb_output

    return np.array(output, dtype=complex)