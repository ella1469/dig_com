import numpy as np
from params import *

def calculate_DFE_MMSE_equalizer(U, noise_variance):
    """
    Calculate MMSE-DFE equalizer coefficients
    """
    # Split U into future (including current) and past symbols
    U_f = U[:, 2:]  # Current and future symbols
    U_p = U[:, :2]  # Past symbols

    # Symbol variance (normalized to 1)
    sigma_b_squared = 1.0

    # Noise covariance matrix
    C_w = noise_variance * np.eye(U.shape[0])

    # Calculate R = sigma_b^2 * U_f * U_f^H + C_w
    R = sigma_b_squared * np.dot(U_f, U_f.T.conj()) + C_w

    # Calculate c_FF = R^(-1) * u_0
    c_FF_DFE = np.dot(np.linalg.inv(R), u0)

    # Calculate c_FB = -c_FF^H * U_p
    c_FB_DFE = -np.dot(c_FF_DFE.conj().T, U_p)


    return c_FF_DFE, c_FB_DFE
