import random
import matplotlib.pyplot as plt

# Function to generate a weighted random number based on specified ranges
def weighted_random_number():
    ranges = [(1, 10), (11, 24), (25, 35), (200,300)]
    weights = [15, 35, 35, 15]
    selected_range = random.choices(ranges, weights=weights, k=1)[0]
    return random.randint(*selected_range)

# Starting seed number
current_value = 60000

# Number of iterations
iterations = 500

# List to hold the generated values
generated_values = [current_value]

# Generate the values over the specified number of iterations
for _ in range(iterations):
    increment = weighted_random_number()
    current_value += increment
    generated_values.append(current_value)

# Calculate differences between successive values
differences = [j - i for i, j in zip(generated_values[:-1], generated_values[1:])]

# Generate a time sequence (1 unit per observation)
time_sequence = list(range(1, iterations + 1))

# Plot the differences over time
plt.plot(time_sequence, differences, marker='o')
plt.title('Differences in Observations Over Time')
plt.xlabel('Time (Arbitrary Units)')
plt.ylabel('Difference in Observation Value')
plt.grid(True)
#plt.show()
plt.savefig('differences_over_time.png')

