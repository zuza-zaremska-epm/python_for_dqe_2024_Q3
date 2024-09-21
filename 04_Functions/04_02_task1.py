import random

from string import ascii_lowercase as letters
from typing import List


def generate_dictionary() -> dict:
    """
    Generator of the dictionary with random number of keys (lowercase letters)
    and assigned random value from 0 to 100 to each value.
    :return: random collection of letters and assigned values
    """
    number_of_keys = random.randint(1, len(letters))
    keys = random.sample(letters, number_of_keys)

    return {key: random.randint(0, 100) for key in keys}


def generate_list_of_dicts() -> List[dict]:
    """
    Generate list of random number of dictionaries (from 2 yo 10),
    where letters are keys and values are numbers from 0 to 100.
    :return: list of random number of dictionaries
    Example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
    """
    number_of_dicts = random.randint(2, 10)
    list_of_dicts = [generate_dictionary() for number in range(number_of_dicts)]
    print(f'List of random number of dicts: {number_of_dicts} dictionaries.')
    print(list_of_dicts)

    return list_of_dicts


def create_working_dictionary(list_of_dicts: List[dict]) -> dict:
    working_dict = {}
    for idx, dictionary in enumerate(list_of_dicts):
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
                    working_dict[key].update(
                        {'dict_num': dict_num, 'value': new_value})
            # If key doesn't exist in the working dictionary add new record.
            else:
                # Save key, dictionary number and value in the working dictionary.
                working_dict[key] = {
                    'dict_num': dict_num,
                    'value': new_value,
                    'occurrence': 1
                }

    return working_dict


def generate_common_dict(list_of_dicts: List[dict]) -> dict:
    """
    From the given list of dictionaries create one common dict where:
    1. If dicts have same key, we will take max value, and rename key
    with dict number with max value.
    2. If key is only in one dict - take it as is.
    :param list_of_dicts: list of random number of dictionaries
    :return: common dictionary
    Example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
    """
    common_dict = {}

    working_dict = create_working_dictionary(list_of_dicts)
    for k, v in working_dict.items():
        # If key occurred more than once add to the key name dictionary number.
        if v['occurrence'] > 1:
            dict_num = working_dict[k]['dict_num']
            common_dict[f'{k}_{dict_num}'] = v['value']
        else:
            common_dict[k] = v['value']

    print(f'Common dictionary: {len(common_dict)} keys.\n', common_dict)
    return common_dict


list_of_random_dicts = generate_list_of_dicts()
common_dictionary = generate_common_dict(list_of_random_dicts)
