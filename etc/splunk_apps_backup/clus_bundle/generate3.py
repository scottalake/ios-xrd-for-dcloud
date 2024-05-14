import numpy as np

# Constants
mean = 1000            # The desired mean of the distribution
std_dev = 200          # The desired standard deviation
num_values = 5000      # The number of values to generate
ramp_up_down_time = 10 # The number of observations to ramp up or down

# Seed for reproducibility
np.random.seed(42)

# Generate a sine wave around the mean value
time = np.arange(num_values)
amplitude = std_dev / 2  # Adjust amplitude to control standard deviation
frequency = 1 / (2 * ramp_up_down_time)  # Frequency to match ramp up/down time
sine_wave = mean + amplitude * np.sin(2 * np.pi * frequency * time)

# Add random noise with the desired standard deviation
noise = np.random.normal(0, std_dev, num_values)

# Combine the sine wave and noise to achieve the target standard deviation overall
numbers = sine_wave + noise

# Ensure the mean of the generated numbers is approximately equal to the target mean
numbers += (mean - np.mean(numbers))

# Convert the generated numbers to integers
numbers = np.round(numbers).astype(int)

# Verify the statistics (optional)
actual_mean = np.mean(numbers)
actual_std = np.std(numbers)
print(f"Actual mean: {actual_mean}")
print(f"Actual standard deviation: {actual_std}")

# Save the generated numbers to a file with integer format
np.savetxt("numbers.csv", numbers, fmt='%i', delimiter=",")
