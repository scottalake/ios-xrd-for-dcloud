import csv

# Replace this with the path to your CSV file
csv_file_path = 'seed_data2.csv' #note this file is gone but it just had the diffs, not the timestamps


def analyze_file(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        rates = [int(row[0]) for row in reader]

    # Calculate differences between successive observations
    differences = [j - i for i, j in zip(rates[:-1], rates[1:])]

    # Calculate average difference
    average_difference = sum(differences) / len(differences)

    # Find the top N largest increases
    top_n = 5  # Change this value to get more or less top increases
    largest_increases = sorted(differences, reverse=True)[:top_n]

    return average_difference, largest_increases

# Run the analysis
average_diff, top_increases = analyze_file(csv_file_path)

# Print the results
print(f'Average difference between observations: {average_diff}')
print(f'Top {len(top_increases)} largest increases: {top_increases}')
