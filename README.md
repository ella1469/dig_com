# Digital Communication Equalizer Simulation

This project simulates the performance of various equalizers (ZF, MMSE, and MMSE-DFE) in a digital communication system. It evaluates their bit error rate (BER) performance under different signal-to-noise ratio (SNR) conditions and compares the results with theoretical bounds.

## Project Structure

```
.
├── [`calculate_DFE_MMSE_equalizer.py`](calculate_DFE_MMSE_equalizer.py )
├── [`calculate_MMSE_equalizer.py`](calculate_MMSE_equalizer.py )
├── [`calculate_SIR_DFE.py`](calculate_SIR_DFE.py )
├── [`calculate_SIR_MMSE.py`](calculate_SIR_MMSE.py )
├── [`calculate_SIR_ZF.py`](calculate_SIR_ZF.py )
├── [`calculate_ZF_equalizer.py`](calculate_ZF_equalizer.py )
├── [`create_rrc_pulse.py`](create_rrc_pulse.py )
├── [`create_u.py`](create_u.py )
├── [`equalizer_performance_with_theory.png`](equalizer_performance_with_theory.png )
├── [`generate_correlated_noise.py`](generate_correlated_noise.py )
├── [`generate_symbols.py`](generate_symbols.py )
├── [`implement_DFE.py`](implement_DFE.py )
├── [`implement_MMSE.py`](implement_MMSE.py )
├── [`implement_ZF.py`](implement_ZF.py )
├── [`main.py`](main.py )
├── [`params.py`](params.py )
├── [`qfunc.py`](qfunc.py )
└── .vscode/
```

### Key Files

- **`main.py`**: The main script that runs the simulation and generates the BER performance plot.
- **`params.py`**: Contains system parameters such as channel impulse response, noise variance, and SNR values.
- **`qfunc.py`**: Implements the Q-function used for theoretical BER calculations.
- **`generate_symbols.py`**: Generates QPSK symbols for transmission.
- **`create_rrc_pulse.py`**: Creates a root-raised cosine (RRC) pulse for pulse shaping.
- **`generate_correlated_noise.py`**: Generates noise with a specified autocorrelation.
- **`implement_ZF.py`**, **`implement_MMSE.py`**, **`implement_DFE.py`**: Implement the ZF, MMSE, and MMSE-DFE equalizers, respectively.
- **`calculate_ZF_equalizer.py`**, **`calculate_MMSE_equalizer.py`**, **`calculate_DFE_MMSE_equalizer.py`**: Calculate the coefficients for the respective equalizers.
- **`calculate_SIR_ZF.py`**, **`calculate_SIR_MMSE.py`**, **`calculate_SIR_DFE.py`**: Calculate the Signal-to-Interference Ratio (SIR) for the respective equalizers.

### Output

The simulation generates a plot (`equalizer_performance_with_theory.png`) showing the BER performance of the equalizers compared to theoretical bounds.

## How to Run

1. Install the required Python libraries:
   ```sh
   pip install numpy scipy matplotlib
   ```

2. Run the main script:
   ```sh
   python main.py
   ```

3. The script will generate a plot (`equalizer_performance_with_theory.png`) and display the BER results in the console.

## Dependencies

- Python 3.6+
- NumPy
- SciPy
- Matplotlib

## Features

- Simulates the performance of ZF, MMSE, and MMSE-DFE equalizers.
- Generates theoretical and simulated BER curves.
- Supports QPSK modulation and root-raised cosine pulse shaping.
- Includes noise generation with specified autocorrelation.

## License

This project is for educational purposes and does not include a specific license.

## Acknowledgments

This project is based on a digital communication system simulation and includes theoretical analysis for equalizer performance.