import os
import random
from constants import WORDS_PATH


def generate_fixed_length_text(lim_words: int) -> list:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + WORDS_PATH
    with open(file_path, "r") as file:
        content = file.read()
        words = content.split(sep='\n')
        generated_text = random.sample(population=words, k=lim_words)
        return generated_text


def text_with_fixed_column_size(text: list, lim_column: int) -> list:
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
    res = 0
    for word in text:
        res += len(word)
    return res
