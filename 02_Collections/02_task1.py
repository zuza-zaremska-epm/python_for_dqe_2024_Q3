import random

from string import ascii_lowercase as letters


def generate_dictionary() -> dict:
    """
    Generator of the dictionary with random number of keys (lowercase letters)
    and assigned random value from 0 to 100 to each value.
    :return: random collection of letters and assigned values
    """
    # As each key need to be unique, max number of keys must be equal total number of available letters.
    number_of_keys = random.randint(1, len(letters))
    keys = random.sample(letters, number_of_keys)

    # For each key assign some random value from 0 to 100.
    return {key: random.randint(0, 100) for key in keys}


# 1. Create a list of random number of dicts (from 2 to 10)
# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
number_of_dicts = random.randint(2, 10)
random_dicts = []

for num in range(number_of_dicts):
    new_dict = generate_dictionary()
    random_dicts.append(new_dict)

print(f'Number of dictionaries: {number_of_dicts}')
print('List of random number of dicts:', random_dicts)



# 2. get previously generated list of dicts and create one common dict:
#
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
# Each line of code should be commented with description.
#
# Commit script to git repository and provide link as home task result.

