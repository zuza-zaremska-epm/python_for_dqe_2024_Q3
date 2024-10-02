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


def append_last_words_sentence(text: str) -> str:
    """
    Creates a new sentence from last words of each sentence in the given text
    and adds it at the end of the text.
    :param text: text to generate the sentence
    :return: text with added sentence
    """
    last_words_sentence = create_sentence_from_last_words(text)
    text += f'\n{last_words_sentence}'

    return text


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
    Replace 'iz' with 'is' when it's not enclosed in the double quotes.
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
    for char in string.whitespace:
        whitespaces += text.count(char)

    print(f'Whitespaces found in text: {whitespaces}')


def text_refiner(text: str) -> str:
    """
    Refines the given text to normalize letter cases and correct mistakes.
    :param text: text to refine
    :return: refined text
    """
    text = normalize_text(text)
    text = fix_iz(text)

    return text


homework = """ tHis iz your homeWork, copy these Text to variable.



 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

count_whitespaces(homework)
homework = text_refiner(homework)
homework = append_last_words_sentence(homework)
print(homework)
