import os
import random


def generate_fixed_length_text(lim_words: int) -> list:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + "/../data/english_top_1000.txt"
    with open(file_path, "r") as file:
        content = file.read()
        words = content.split(sep='\n')
        generated_text = random.sample(population=words, k=lim_words)
        print(generated_text)
        return generated_text


generate_fixed_length_text(10)
