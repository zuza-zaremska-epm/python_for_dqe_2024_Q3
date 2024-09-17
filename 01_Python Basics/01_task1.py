import random

from statistics import mean

# Create list of 100 random numbers from 0 to 1000
random_numbers = random.sample(range(0, 1000), 100)

# Sort list from min to max (without using sort()).
for idx_1 in range(0, len(random_numbers)):
    # Compare only numbers on the right side from current (idx_1) index.
    for idx_2 in range(idx_1 + 1, len(random_numbers)):
        # If number from the index equal idx_1 is bigger or equal to number
        # from the index equal idx_2 swap them by places.
        # Example: if at index 2 there is number 3, and at index 5 there is number 2 - swap.
        if random_numbers[idx_1] >= random_numbers[idx_2]:
            random_numbers[idx_1], random_numbers[idx_2] = random_numbers[idx_2], random_numbers[idx_1]

# Calculate average for even and odd numbers.
# Odd number is when the result of dividing by modulo operator is not equal zero.
odd_numbers = [num for num in random_numbers if num % 2 != 0]
avg_odd_numbers = mean(odd_numbers)
even_numbers = [num for num in random_numbers if num % 2 == 0]
avg_even_numbers = mean(even_numbers)

# Print both average result in console.
print(f"Average of odd numbers: {avg_odd_numbers}\nAverage of even numbers: {avg_even_numbers}")

