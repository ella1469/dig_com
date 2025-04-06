import numpy as np
from params import *

def calculate_MMSE_equalizer(U, noise_variance=0.4):
    """
    Calculate MMSE equalizer coefficients
    """

    # Symbol variance (normalized to 1)
    sigma_b_squared = 1.0

    # Noise covariance matrix
    C_w = noise_variance * np.eye(U.shape[0])

    # Calculate R = sigma_b^2 * U * U^H + C_w
    R = sigma_b_squared * np.dot(U, U.T.conj()) + C_w

    # Calculate p = sigma_b^2 * u_0
    p = sigma_b_squared * u0

    # Calculate c_MMSE = R^(-1) * p
    c_MMSE = np.dot(np.linalg.inv(R), p)

    theoretical_mmse = np.array([-0.09298, -0.05692, -0.24757, -0.10603, 0.43381, -0.22538, 0.15261, -0.11904])
    print(f"MMSE equalizer calculated: {c_MMSE}")
    print(f"MMSE equalizer theoretical: {theoretical_mmse}")
    print(f"Difference: {np.linalg.norm(c_MMSE - theoretical_mmse)}")

    return c_MMSE