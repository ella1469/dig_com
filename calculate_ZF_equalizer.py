import numpy as np

def calculate_ZF_equalizer(U):
    """
    Calculate Zero Forcing equalizer coefficients
    """
    # Select the vector e (index of the desired symbol)
    col = U.shape[1]
    e = np.zeros(col)
    e[col//2] = 1  # The third column corresponds to the current symbol b[n]

    # Calculate U^H * U
    UH_U = np.dot(U.T.conj(), U)

    # Calculate (U^H * U)^(-1)
    UH_U_inv = np.linalg.inv(UH_U)

    # Calculate (U^H * U)^(-1) * e
    temp = np.dot(UH_U_inv, e)

    # Calculate U * (U^H * U)^(-1) * e
    c_zf = np.dot(U, temp)

    theoretical_zf = np.array([-0.1578, -0.5253, -0.3412, -0.7158, 0.4202, -1.0227, 0, -1.1208])
    print(f"ZF equalizer calculated: {c_zf}")
    print(f"ZF equalizer theoretical: {theoretical_zf}")
    print(f"Difference: {np.linalg.norm(c_zf - theoretical_zf)}")

    return c_zf
