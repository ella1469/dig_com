import numpy as np



def implement_DFE(input_signal, h_FF, h_FB, window_size=8):
    """
    Implementation of DFE (Decision Feedback Equalizer)
    """
    print(f"Feedback taps: {h_FB}")  # הדפסת ערכי הפילטר לבדיקה

    L_FF = len(h_FF)
    L_FB = len(h_FB)
    output_length = len(input_signal) - window_size + 1
    output = np.zeros(output_length, dtype=complex)

    # Store past decisions for feedback
    past_decisions = np.zeros(L_FB, dtype=complex)

    # Loop through each output sample
    for i in range(output_length):
        # Feedforward part
        window = input_signal[i:i + window_size]
        ff_out = np.dot(h_FF.conj(), window)

        # Feedback part
        fb_out = np.dot(h_FB, past_decisions)

        # Combine both parts
        output[i] = ff_out + fb_out

        # Make decision for QPSK with proper normalization
        decision_real = np.sign(np.real(output[i])) / np.sqrt(2)
        decision_imag = np.sign(np.imag(output[i])) / np.sqrt(2)
        decision = decision_real + 1j * decision_imag

        # Shift past decisions and add new one
        if L_FB > 0:
            past_decisions = np.roll(past_decisions, 1)
            past_decisions[0] = decision

    return output