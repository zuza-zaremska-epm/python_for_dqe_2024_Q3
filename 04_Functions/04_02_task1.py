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
    """
    Create working dictionary with kaye and details about number of occurrences
    in different dictionaries, max value found and max value source dictionary.
    :param list_of_dicts: list of random number of dictionaries
    :return: collection of keys with their details
    Schema: {
        'g': {'occurrence': 2, 'dict_num': 3, 'value': 5},
        'b': {'occurrence': 1, 'dict_num': 1, 'value': 1},
        'd': {'occurrence': 8, 'dict_num': 1, 'value': 9},
    }
    """
    working_dict = {}
    for number, dictionary in enumerate(list_of_dicts):
        dict_num = number + 1

        for letter, new_value in dictionary.items():
            if working_dict.get(letter):
                working_dict[letter]['occurrence'] += 1
                old_letter_value = working_dict[letter]['value']
                if new_value > old_letter_value:
                    working_dict[letter].update(
                        {'dict_num': dict_num, 'value': new_value})
            else:
                working_dict[letter] = {
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
    for letter, value in working_dict.items():
        if value['occurrence'] > 1:
            dict_num = working_dict[letter]['dict_num']
            common_dict[f'{letter}_{dict_num}'] = value['value']
        else:
            common_dict[letter] = value['value']

    print(f'Common dictionary: {len(common_dict)} keys.\n', common_dict)
    return common_dict


list_of_random_dicts = generate_list_of_dicts()
common_dictionary = generate_common_dict(list_of_random_dicts)
