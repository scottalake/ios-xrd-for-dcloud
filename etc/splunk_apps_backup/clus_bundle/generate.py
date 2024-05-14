import random

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
generated_values = []

# Generate the values over the specified number of iterations
for _ in range(iterations):
    increment = weighted_random_number()
    current_value += increment
    generated_values.append(current_value)

# Output the results
for value in generated_values:
    print(value)
