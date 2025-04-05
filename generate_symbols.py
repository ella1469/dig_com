import numpy as np

def generate_symbols(num_symbols):

    bits_I = np.random.randint(0, 2, num_symbols) * 2 - 1
    bits_Q = np.random.randint(0, 2, num_symbols) * 2 - 1
    symbols = (bits_I + 1j * bits_Q) / np.sqrt(2)

    return symbols

