import random

from statistics import mean

# Create list of 100 random numbers from 0 to 1000
random_numbers = random.sample(range(0, 1000), 100)
print(random_numbers)

# Sort list from min to max (without using sort()).
sorted_random_numbers = []

# Calculate average for even and odd numbers.
# Odd number is when the result of dividing by modulo operator is not equal zero.
odd_numbers = [num for num in sorted_random_numbers if num % 2 != 0]
avg_odd_numbers = mean(odd_numbers)
even_numbers = [num for num in sorted_random_numbers if num % 2 == 0]
avg_even_numbers = mean(even_numbers)

# Print both average result in console.
print(f"Average of odd numbers: {avg_odd_numbers}\nAverage of even numbers: {avg_even_numbers}")

