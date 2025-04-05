import numpy as np

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

    # Select the column vector corresponding to the desired symbol
    u_0 = U_f[:, 0]  # First column of U_f is the current symbol

    # Calculate c_FF = R^(-1) * u_0
    h_FF_DFE = np.dot(np.linalg.inv(R), u_0)

    # Calculate c_FB = -c_FF^H * U_p
    h_FB_DFE = -np.dot(h_FF_DFE.conj().T, U_p)

    # בדיקת התוצאה לעומת הערך התיאורטי המצופה
    theoretical_ff_dfe = np.array([-0.0705, -0.04308, -0.187, -0.0715, 0.570, -0.171, 0, 0])
    theoretical_fb_dfe = np.array([0.456])
    print(f"DFE-FF equalizer calculated: {h_FF_DFE}")
    print(f"DFE-FF equalizer theoretical: {theoretical_ff_dfe}")
    print(f"Difference FF: {np.linalg.norm(h_FF_DFE - theoretical_ff_dfe)}")
    print(f"DFE-FB equalizer calculated: {h_FB_DFE}")
    print(f"DFE-FB equalizer theoretical: {theoretical_fb_dfe}")

    return h_FF_DFE, h_FB_DFE
