import numpy as np
from params import *
from qfunc import qfunc
from scipy import signal
import matplotlib.pyplot as plt
from create_u import create_u_matrix
from implement_ZF import implement_ZF
from implement_DFE import implement_DFE
from implement_MMSE import implement_MMSE
from generate_symbols import generate_symbols
from calculate_SIR_ZF import calculate_SIR_ZF
from calculate_SIR_DFE import calculate_SIR_DFE
from calculate_SIR_MMSE import calculate_SIR_MMSE
from calculate_ZF_equalizer import calculate_ZF_equalizer
from calculate_MMSE_equalizer import calculate_MMSE_equalizer
from generate_correlated_noise import generate_correlated_noise
from calculate_DFE_MMSE_equalizer import calculate_DFE_MMSE_equalizer


def main():
    # Generate QPSK symbols
    symbols = generate_symbols(num_symbols)
    #symbols[0] = 0
    
    # Create upsampled symbol sequence
    symbols_upsampled = np.zeros(samples_per_symbol * num_symbols, dtype=complex)
    symbols_upsampled[::samples_per_symbol] = symbols

    # Apply complete system response directly
    # (f_n already includes TX filter, channel and RX filter effects)
    rx_signal_noiseless = signal.convolve(symbols_upsampled, f_n)

    # Create U matrix from theoretical f[n] values
    U = create_u_matrix(u0, K, col)

    # Calculate equalizer coefficients using U matrix
    c_zf = calculate_ZF_equalizer(U)
    c_mmse = calculate_MMSE_equalizer(U, N0_base)
    c_ff_dfe, c_fb_dfe = calculate_DFE_MMSE_equalizer(U, N0_base)

    # Calculate SIR values using the code
    sir_zf = calculate_SIR_ZF(c_zf, U, N0_base)
    sir_mmse = calculate_SIR_MMSE(c_mmse, U, N0_base)
    sir_dfe = calculate_SIR_DFE(c_ff_dfe, U[:, 2:], N0_base)


    # Matched filter bound (calculated in part A)
    #TODO: chek this 4 lines???
    MFB = np.zeros(len(Eb_N0_dB))
    for i in range(len(Eb_N0_dB)):
        Eb_N0 = 10 ** (Eb_N0_dB[i] / 10)
        MFB[i] = qfunc(np.sqrt(SNR_MFB * Eb_N0))


    for i in range(len(Eb_N0_dB)):
        Eb_N0 = 10 ** (Eb_N0_dB[i] / 10)
        # Bounds using SIR from code
        theoretical_bound_ZF[i] = qfunc(np.sqrt(sir_zf))
        theoretical_bound_MMSE[i] = qfunc(np.sqrt(sir_mmse))
        theoretical_bound_DFE[i] = qfunc(np.sqrt(sir_dfe))

        # Bounds using SIR from theoretical analysis (part A)
        theoretical_bound_ZF_theory[i] = qfunc(np.sqrt(sir_zf_theory))
        theoretical_bound_MMSE_theory[i] = qfunc(np.sqrt(sir_mmse_theory))
        theoretical_bound_DFE_theory[i] = qfunc(np.sqrt(sir_dfe_theory))

    # Loop through signal-to-noise ratio values
    BER_NoEq = np.zeros(len(Eb_N0_dB))
    BER_ZF = np.zeros(len(Eb_N0_dB))
    BER_MMSE = np.zeros(len(Eb_N0_dB))
    BER_DFE = np.zeros(len(Eb_N0_dB))



if __name__ == "__main__":
    main()