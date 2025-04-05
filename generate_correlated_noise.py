import numpy as np

def generate_correlated_noise(length, N0, corr_function=None):
    """
    Generate noise with appropriate autocorrelation
    N0: noise power spectral density (scales with Eb/N0)
    """
    # Generate complex white Gaussian noise
    # תיקון: ליצירת רעש עם אוטוקורלציה של 0.4δ[k]
    noise_real = np.random.normal(0, np.sqrt(N0 / 2), length)
    noise_imag = np.random.normal(0, np.sqrt(N0 / 2), length)
    white_noise = noise_real + 1j * noise_imag

    if corr_function is None or len(corr_function) <= 1:
        return white_noise
    else:
        # Filter the noise to get the desired autocorrelation
        return signal.lfilter(corr_function, [1.0], white_noise)

