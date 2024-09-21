import string
import re


def create_sentence_from_last_words(text: str) -> str:
    """
    Create sentence form the last words of given list of text lines.
    :param text: text lines in the form of list
    :return: sentence made of last words
    """
    list_of_sentences = [line for line in text.split('\n')]
    list_of_last_words = []

    for sentence in list_of_sentences:
        # If line is not made of whitespaces get last word from the sentence
        # and append to the new sentence.
        if not set(sentence).issubset(string.whitespace):
            # Retrieve last word from the sentence and add to last_words_sentence.
            last_word_start_position = sentence.rfind(' ') + 1
            last_word = sentence[last_word_start_position:-1]
            list_of_last_words.append(last_word)

    sentence_from_last_words = ' '.join(list_of_last_words)

    return sentence_from_last_words.capitalize() + '.'


def normalize_text(text: str) -> str:
    """
    Normalizes given text to the form where each sentence starts with
    the capital letter.
    :param text: text to normalize
    :return: normalized text
    """
    lines = text.lower().split('.')

    for line_index, line in enumerate(lines):
        for char in line:
            if char not in string.whitespace:
                line = line.replace(char, char.upper(), 1)
                break

        lines[line_index] = line

    return '.'.join(lines)


def fix_iz(text: str) -> str:
    """
    Replace 'iz' with 'is' when it's a mistake.
    :param text: text to fix
    :return: fixed text
    """
    return re.sub(r'(?<![“”"])\biz\b(?![“”"])', 'is', text)


def count_whitespaces(text: str):
    """
    Prints number of found whitespaces in the given text.
    :param text: text to analyze
    """
    whitespaces = 0
    for char in homework:
        if char in string.whitespace:
            whitespaces += 1

    print(f'Whitespaces found in text: {whitespaces}')


homework = """ tHis iz your homeWork, copy these Text to variable.



 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

count_whitespaces(homework)
homework = normalize_text(homework)
homework = fix_iz(homework)

# Extract sentence made of last words and add to the text.
last_words_sentence = create_sentence_from_last_words(homework)
homework += f'\n{last_words_sentence}'
print("FORMATTED TEXT:\n", homework)
