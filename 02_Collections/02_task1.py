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
# dict's random numbers of keys should be a letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
number_of_dicts = random.randint(2, 10)
random_dicts = []

for num in range(number_of_dicts):
    new_dict = generate_dictionary()
    random_dicts.append(new_dict)

print(f'List of random number of dicts: {len(random_dicts)} dictionaries.\n', random_dicts)


# 2. Get previously generated list of dicts and create one common dict:
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
working_dict = {}
for idx, dictionary in enumerate(random_dicts):
    dict_num = idx + 1

    for key, new_value in dictionary.items():
        # If the key already exists in the working directory then:
        if working_dict.get(key):
            # Update number of occurrences.
            working_dict[key]['occurrence'] += 1
            old_key_value = working_dict[key]['value']

            # If new value is bigger than the previous one than update
            # this value and dictionary number.
            if new_value > old_key_value:
                working_dict[key].update({'dict_num': dict_num, 'value': new_value})
        # If key doesn't exist in the working dictionary add new record.
        else:
            # Save key, dictionary number and value in the working dictionary.
            working_dict[key] = {
                'dict_num': dict_num,
                'value': new_value,
                'occurrence': 1
            }

common_dict = {}
for k, v in working_dict.items():
    # If key occurred more than once add to the key name dictionary number.
    if v['occurrence'] > 1:
        dict_num = working_dict[k]['dict_num']
        common_dict[f'{k}_{dict_num}'] = v['value']
    else:
        common_dict[k] = v['value']

print(f'Common dictionary: {len(common_dict)} keys.\n', common_dict)
