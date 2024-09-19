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

