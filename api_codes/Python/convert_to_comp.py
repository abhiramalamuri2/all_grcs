'''
import numpy as np
import matplotlib.pyplot as plt

# Load the raw samples from the file
samples = np.fromfile('output.dat', dtype=np.complex64)  # Assuming the samples are stored as 32-bit complex
inital_samples = samples[300:3000]

# Display the first few samples
print(inital_samples)



# Plot real part of the signal
plt.figure()
plt.plot(np.real(inital_samples), label="Real")
plt.plot(np.imag(inital_samples), label="Imaginary")
plt.legend()
plt.title("Real and Imaginary parts of received samples")
plt.show()
'''

import numpy as np
import matplotlib.pyplot as plt

# Load the raw samples from the file
samples = np.fromfile('output.dat', dtype=np.complex64)  # Assuming the samples are stored as 32-bit complex

# Zoom in to show only 4-5 periods of the sine wave
# Number of samples per period = Sampling rate / Frequency = 25000 / 10000 = 2.5 samples per period
# For 5 periods, you'll need roughly 12-13 samples
samples_to_display = samples[100:150]  # Displaying the first 25 samples (to give 10+ periods at 2.5 samples per period)

# Scale down the amplitude if necessary
scaled_samples = samples_to_display / np.max(np.abs(samples_to_display)) * 0.1  # Scale down by factor of 0.5

# Plot real part of the signal
plt.figure()
plt.plot(np.real(scaled_samples), label="Real")
plt.plot(np.imag(scaled_samples), label="Imaginary")
plt.legend()
plt.title("Real and Imaginary parts of received samples (Zoomed In)")
plt.show()


