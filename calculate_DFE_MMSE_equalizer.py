import numpy as np
from params import *

def calculate_DFE_MMSE_equalizer(U, noise_variance=0.4):
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

    theoretical_ff_dfe = np.array([0, 0, -0.468, 0, 0.3386, -0.175, 0.119, -0.0928])
    theoretical_fb_dfe = np.array([0,  0.468])
    print(f"DFE-FF equalizer calculated: {c_FF_DFE}")
    print(f"DFE-FF equalizer theoretical: {theoretical_ff_dfe}")
    print(f"Difference FF: {np.linalg.norm(c_FF_DFE - theoretical_ff_dfe)}")
    print(f"DFE-FB equalizer calculated: {c_FB_DFE}")
    print(f"DFE-FB equalizer theoretical: {theoretical_fb_dfe}")

    return c_FF_DFE, c_FB_DFE
