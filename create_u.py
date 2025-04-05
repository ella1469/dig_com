import numpy as np

def create_u_matrix(u0, K, col):
    """
    Create U matrix based on the theoretical f[n] values
    """

    U = np.zeros((K, col))
    center = col // 2
    for i in range(col):
        shift = (i - center) * 2  # שים לב להזזה של 2
        if shift < 0:
            U[:shift, i] = u0[-shift:]
        elif shift > 0:
            U[shift:, i] = u0[:-shift]
        else:
            U[:, i] = u0


    return U