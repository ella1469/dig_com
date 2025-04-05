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
    MFB = np.zeros(len(Eb_N0_dB))
    for i in range(len(Eb_N0_dB)):
        Eb_N0 = 10 ** (Eb_N0_dB[i] / 10)
        MFB[i] = qfunc(np.sqrt(SNR_MFB * Eb_N0))

    # Calculate theoretical bounds
    theoretical_bound_ZF = np.zeros(len(Eb_N0_dB))
    theoretical_bound_MMSE = np.zeros(len(Eb_N0_dB))
    theoretical_bound_DFE = np.zeros(len(Eb_N0_dB))
    theoretical_bound_ZF_theory = np.zeros(len(Eb_N0_dB))
    theoretical_bound_MMSE_theory = np.zeros(len(Eb_N0_dB))
    theoretical_bound_DFE_theory = np.zeros(len(Eb_N0_dB))

    for i in range(len(Eb_N0_dB)):
        Eb_N0 = 10 ** (Eb_N0_dB[i] / 10)
        # Bounds using SIR from code
        theoretical_bound_ZF[i] = qfunc(np.sqrt(sir_zf * Eb_N0))
        theoretical_bound_MMSE[i] = qfunc(np.sqrt(sir_mmse * Eb_N0))
        theoretical_bound_DFE[i] = qfunc(np.sqrt(sir_dfe * Eb_N0))

        # Bounds using SIR from theoretical analysis (part A)
        theoretical_bound_ZF_theory[i] = qfunc(np.sqrt(sir_zf_theory * Eb_N0))
        theoretical_bound_MMSE_theory[i] = qfunc(np.sqrt(sir_mmse_theory * Eb_N0))
        theoretical_bound_DFE_theory[i] = qfunc(np.sqrt(sir_dfe_theory * Eb_N0))

    # Loop through signal-to-noise ratio values
    BER_NoEq = np.zeros(len(Eb_N0_dB))
    BER_ZF = np.zeros(len(Eb_N0_dB))
    BER_MMSE = np.zeros(len(Eb_N0_dB))
    BER_DFE = np.zeros(len(Eb_N0_dB))

    for i, Eb_N0_dB_val in enumerate(Eb_N0_dB):
        print(f"Processing Eb/N0 = {Eb_N0_dB_val} dB")

        # Calculate required noise power according to Eb/N0
        Eb_N0 = 10 ** (Eb_N0_dB_val / 10)
        N0 = N0_base / Eb_N0  # Scale noise variance based on Eb/N0

        # Generate correlated noise with appropriate variance
        noise = generate_correlated_noise(len(rx_signal_noiseless), 0.4 * N0)

        # Add noise to noiseless received signal
        rx_signal = rx_signal_noiseless + noise

        # Sample at appropriate points (every samples_per_symbol samples)
        # Need to account for filter delay and proper alignment
        delay = (len(f_n) - 1) // 2  # Approximate filter delay
        rx_sampled = rx_signal[delay::samples_per_symbol]
        rx_sampled = rx_sampled[:num_symbols]  # Truncate to original symbol length

        # Apply different equalizers
        # No equalizer - direct decision on samples
        decisions_NoEq = np.sign(np.real(rx_sampled)) / np.sqrt(2) + 1j * np.sign(np.imag(rx_sampled)) / np.sqrt(2)

        # ZF-LE using matrix approach
        eq_ZF = implement_ZF(rx_sampled, c_zf)
        decisions_ZF = np.sign(np.real(eq_ZF)) / np.sqrt(2) + 1j * np.sign(np.imag(eq_ZF)) / np.sqrt(2)

        # MMSE-LE using matrix approach
        eq_MMSE = implement_MMSE(rx_sampled, c_mmse)
        decisions_MMSE = np.sign(np.real(eq_MMSE)) / np.sqrt(2) + 1j * np.sign(np.imag(eq_MMSE)) / np.sqrt(2)

        # MMSE-DFE using matrix approach
        eq_DFE = implement_DFE(rx_sampled, c_ff_dfe, c_fb_dfe)
        decisions_DFE = np.sign(np.real(eq_DFE)) / np.sqrt(2) + 1j * np.sign(np.imag(eq_DFE)) / np.sqrt(2)

        # Calculate error probability (for QPSK check the components separately)
        errors_NoEq = np.sum(np.sign(np.real(symbols[:len(decisions_NoEq)])) != np.sign(np.real(decisions_NoEq))) + \
                      np.sum(np.sign(np.imag(symbols[:len(decisions_NoEq)])) != np.sign(np.imag(decisions_NoEq)))
        BER_NoEq[i] = errors_NoEq / (2 * len(decisions_NoEq))

        errors_ZF = np.sum(np.sign(np.real(symbols[:len(decisions_ZF)])) != np.sign(np.real(decisions_ZF))) + \
                    np.sum(np.sign(np.imag(symbols[:len(decisions_ZF)])) != np.sign(np.imag(decisions_ZF)))
        BER_ZF[i] = errors_ZF / (2 * len(decisions_ZF))

        errors_MMSE = np.sum(np.sign(np.real(symbols[:len(decisions_MMSE)])) != np.sign(np.real(decisions_MMSE))) + \
                      np.sum(np.sign(np.imag(symbols[:len(decisions_MMSE)])) != np.sign(np.imag(decisions_MMSE)))
        BER_MMSE[i] = errors_MMSE / (2 * len(decisions_MMSE))

        errors_DFE = np.sum(np.sign(np.real(symbols[:len(decisions_DFE)])) != np.sign(np.real(decisions_DFE))) + \
                     np.sum(np.sign(np.imag(symbols[:len(decisions_DFE)])) != np.sign(np.imag(decisions_DFE)))
        BER_DFE[i] = errors_DFE / (2 * len(decisions_DFE))

    # Plot error probability results
    plt.figure(figsize=(12, 8))

    # Add simulation results
    plt.semilogy(Eb_N0_dB, BER_NoEq, 'mo-', linewidth=2, label='No Equalizer')
    plt.semilogy(Eb_N0_dB, BER_ZF, 'bo-', linewidth=2, label='ZF-LE (Simulation)')
    plt.semilogy(Eb_N0_dB, BER_MMSE, 'go-', linewidth=2, label='MMSE-LE (Simulation)')
    plt.semilogy(Eb_N0_dB, BER_DFE, 'ko-', linewidth=2, label='MMSE-DFE (Simulation)')

    # Add theoretical bounds based on SIR from code
    plt.semilogy(Eb_N0_dB, theoretical_bound_ZF, 'b--', linewidth=1, label='ZF-LE (Code SIR)')
    plt.semilogy(Eb_N0_dB, theoretical_bound_MMSE, 'g--', linewidth=1, label='MMSE-LE (Code SIR)')
    plt.semilogy(Eb_N0_dB, theoretical_bound_DFE, 'k--', linewidth=1, label='MMSE-DFE (Code SIR)')

    # Add theoretical bounds based on SIR from theory (part A)
    plt.semilogy(Eb_N0_dB, theoretical_bound_ZF_theory, 'b-.', linewidth=1, label='ZF-LE (Theory SIR)')
    plt.semilogy(Eb_N0_dB, theoretical_bound_MMSE_theory, 'g-.', linewidth=1, label='MMSE-LE (Theory SIR)')
    plt.semilogy(Eb_N0_dB, theoretical_bound_DFE_theory, 'k-.', linewidth=1, label='MMSE-DFE (Theory SIR)')

    # Add matched filter bound
    plt.semilogy(Eb_N0_dB, MFB, 'r--', linewidth=1, label='Matched Filter Bound')

    # Add titles and labels
    plt.grid(True)
    plt.xlabel('Eb/N0 [dB]')
    plt.ylabel('Bit Error Rate (BER)')
    plt.title('Performance of Different Equalizers')
    plt.legend(loc='lower left')
    plt.savefig('equalizer_performance_with_theory.png', dpi=300)
    plt.show()

    # Print result summary for both code-based and theory-based bounds
    print(f"Result summary for Eb/N0 = 10 dB:")
    print(f"No Equalizer: {BER_NoEq[5]:.6f}")
    print(f"ZF-LE (Simulation): {BER_ZF[5]:.6f}")
    print(f"MMSE-LE (Simulation): {BER_MMSE[5]:.6f}")
    print(f"MMSE-DFE (Simulation): {BER_DFE[5]:.6f}")
    print(f"ZF-LE (Code SIR): {theoretical_bound_ZF[5]:.6f}")
    print(f"MMSE-LE (Code SIR): {theoretical_bound_MMSE[5]:.6f}")
    print(f"MMSE-DFE (Code SIR): {theoretical_bound_DFE[5]:.6f}")
    print(f"ZF-LE (Theory SIR): {theoretical_bound_ZF_theory[5]:.6f}")
    print(f"MMSE-LE (Theory SIR): {theoretical_bound_MMSE_theory[5]:.6f}")
    print(f"MMSE-DFE (Theory SIR): {theoretical_bound_DFE_theory[5]:.6f}")
    print(f"Matched Filter Bound: {MFB[5]:.6f}")


if __name__ == "__main__":
    main()