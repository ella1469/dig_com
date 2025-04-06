import numpy as np
import matplotlib.pyplot as plt


# PARAMETERS
# Set random seed for reproducibility
ID = 316105493
np.random.seed(ID)

# Basic system parameters
T = 1.0  # Symbol time (normalized)
alpha = 0.6  # Roll-off parameter for RRC pulse
num_symbols = 200  # Number of symbols to transmit
samples_per_symbol = 2  # Number of samples per symbol
Ts = T / samples_per_symbol  # Sample time
K = 8
col = 5

# Channel definition (impulse response)
f_n = np.array([-0.8, 0, 1, -0.3])  # Channel impulse response
u0 = np.array([0, 0, -0.8, 0, 1, -0.3, 0, 0])

# Signal-to-noise ratio vector for testing
Eb_N0_dB = np.arange(-5, 41, 5)  # List of Eb/N0 values in dB

# Noise variance calculation
N0_base = 0.4  # Base noise variance as specified in theory

# Create RRC pulse
span = 8  # Pulse length in symbol time units

# INITIALIZE
# Initialize result vectors
BER_NoEq = np.zeros(len(Eb_N0_dB))
BER_ZF = np.zeros(len(Eb_N0_dB))
BER_MMSE = np.zeros(len(Eb_N0_dB))
BER_DFE = np.zeros(len(Eb_N0_dB))

#CONSTANTS

# SIR values from theoretical analysis in part A
# These values are taken from the analysis in part A of the assignment
#TODO: verify correctens of this val
sir_zf_theory = 0.7336  # Value from part A
sir_mmse_theory = 2.3277  # Value from part A
sir_dfe_theory = 3.2686  # Value from part A

P_error_sir_zf_theory = 0.1959  # Value from part A
P_error_sir_mmse_theory = 0.0635  # Value from part A
P_error_sir_dfe_theory = 0.0353  # Value from part A

#TODO: verify correctens of this val
# Matched filter bound (calculated in part A)
SNR_MFB = 1.73 / 0.2  # ||u_0||^2 / N_0


# Theoretical bounds using SIR values calculated from code
theoretical_bound_ZF = np.zeros(len(Eb_N0_dB))
theoretical_bound_MMSE = np.zeros(len(Eb_N0_dB))
theoretical_bound_DFE = np.zeros(len(Eb_N0_dB))

# Theoretical bounds using SIR values from part A
theoretical_bound_ZF_theory = np.zeros(len(Eb_N0_dB))
theoretical_bound_MMSE_theory = np.zeros(len(Eb_N0_dB))
theoretical_bound_DFE_theory = np.zeros(len(Eb_N0_dB))
