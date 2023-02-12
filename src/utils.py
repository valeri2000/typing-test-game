"""File containing different utility functions
"""

import os
import random
from constants import WORDS_PATH


def generate_fixed_length_text(lim_words: int) -> list:
    """Method which generates text from file with words with certain number of words

    Args:
        lim_words (int): wanted number of words in the generated text

    Returns:
        list: sequence of the words in the generated text
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + WORDS_PATH
    with open(file_path, "r", encoding='utf-8') as file:
        content = file.read()
        words = content.split(sep='\n')
        generated_text = random.sample(population=words, k=lim_words)
        return generated_text


def text_with_fixed_column_size(text: list, lim_column: int) -> list:
    """Method which makes each row of text with a maximum width size

    Args:
        text (list): sequence of words in the text
        lim_column (int): maximum width (as number of symbols) for a row

    Returns:
        list: list of rows consisting the words which are limited to certain width
    """

    res_text = []
    curr_column, curr_line = 0, ''
    for word in text:
        if len(word) + curr_column + 1 > lim_column:
            res_text.append(curr_line)
            curr_line = word + ' '
            curr_column = len(word) + 1
        else:
            curr_line += word + ' '
            curr_column += len(word) + 1
    curr_line = curr_line[:-1]
    res_text.append(curr_line)
    return res_text


def total_characters_in_text(text: list) -> int:
    """Method which counts symbol in a sequence of words

    Args:
        text (list): sequence of the words in the text

    Returns
        int: total number of symbols
    """

    return sum(len(word) for word in text)
