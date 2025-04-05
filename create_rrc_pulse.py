import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

def create_rrc_pulse(beta, span, sps):
    """
    Create Root Raised Cosine pulse
    beta: roll-off parameter
    span: pulse length in symbol time units
    sps: samples per symbol
    """
    n = np.arange(-span * sps // 2, span * sps // 2 + 1)
    t = n / sps

    # Special values
    rrc = np.zeros(len(t))

    # t = 0
    rrc[t == 0] = 1.0 - beta + (4 * beta / np.pi)

    # t = ±Ts/(4*beta)
    idx = np.abs(np.abs(t) - 1 / (4 * beta)) < 1e-10
    if np.any(idx):
        rrc[idx] = (beta / np.sqrt(2)) * (
                (1 + 2 / np.pi) * np.sin(np.pi / (4 * beta)) + (1 - 2 / np.pi) * np.cos(np.pi / (4 * beta)))

    # t ≠ 0 and t ≠ ±Ts/(4*beta)
    idx = ~(np.abs(t) < 1e-10) & ~(np.abs(np.abs(t) - 1 / (4 * beta)) < 1e-10)
    rrc[idx] = (np.sin(np.pi * t[idx] * (1 - beta)) + 4 * beta * t[idx] * np.cos(np.pi * t[idx] * (1 + beta))) / (
            np.pi * t[idx] * (1 - (4 * beta * t[idx]) ** 2))

    # Normalize energy
    return rrc / np.sqrt(np.sum(rrc ** 2))



# if __name__ == "__main__":
#     # Internal testing
#     beta = 1  # Roll-off factor
#     span = 8     # Pulse length in symbol time units
#     sps = 8      # Samples per symbol

#     # Generate RRC pulse
#     rrc_pulse = create_rrc_pulse(beta, span, sps)

#     # Plot the pulse
#     plt.figure(figsize=(10, 6))
#     plt.plot(rrc_pulse, label=f"RRC Pulse (β={beta}, span={span}, sps={sps})")
#     plt.title("Root Raised Cosine (RRC) Pulse")
#     plt.xlabel("Samples")
#     plt.ylabel("Amplitude")
#     plt.grid(True)
#     plt.legend()
#     plt.show()