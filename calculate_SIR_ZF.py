import numpy as np
from qfunc import qfunc

def calculate_SIR_ZF(c_zf, U, noise_variance=0.4):
    """
    Calculate Signal-to-Interference Ratio for ZF equalizer

    Parameters:
    c_zf : array_like
        Zero-Forcing equalizer coefficients
    U : array_like
        Matrix of signal vectors
    noise_variance : float
        Variance of noise (for white noise case)

    Returns:
    float
        Signal-to-Interference Ratio
    """
    # Create noise covariance matrix
    # In general, this could be any covariance matrix C_w
    # (not just diagonal as in the original implementation)
    C_w = noise_variance * np.eye(len(c_zf))

    # For colored noise, C_w would be a full matrix reflecting the correlation structure
    # For example, if we have autocorrelation like in the problem (0.4δ[k]):
    # Here we could build a more complex C_w if needed

    # Compute SIR using the general formula: 1 / (c_ZF^H * C_w * c_ZF)
    # This is valid for any noise covariance structure
    noise_contribution = np.dot(c_zf.conj().T, np.dot(C_w, c_zf))
    SIR = 1 / noise_contribution

    P_error = qfunc(np.sqrt(SIR))
    print(f"Probability of error (P_e) calculated: {P_error:.4f}")
    # For comparison with theoretical value
    theoretical_SIR = 0.1959 

    print(f"SIR_ZF theoretical: {theoretical_SIR:.4f}")

    return P_error