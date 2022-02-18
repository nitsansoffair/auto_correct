import os

import numpy as np


class AutoCorrect:
    def __init__(self):
        pass

    def clean(self, word, array):
        word_new = ''
        for w in word:
            delete = False
            for char in array:
                if char == w:
                    delete = True
            if not delete:
                word_new += w
        return word_new

    def process_data(self, file_name):
        words_array = []
        f = open(os.getcwd() + f"{file_name}", "r")
        text = f.read().lower()
        lines = text.split('\n')
        for line in lines:
            words = line.split(' ')
            for word in words:
                words_split = word.split('-')
                for word in words_split:
                    word = self.clean(word, [' ', '', ':', ';', ',', '.', '(', ')', '?', ']', '[', '}', '{', '!', "'", '<', '>', '*', '+', '/', '@', '#', '$', '%', '^', '&', '~', '='])
                    if len(word) > 0 and not word.isnumeric():
                        words_array.append(word)
        return words_array

    def get_count(self, word_l):
        word_count_dict = {}
        for word in word_l:
            word_count_dict[word] = 1 if word not in word_count_dict.keys() else word_count_dict[word] + 1
        return word_count_dict

    def get_probs(self, word_count_dict):
        probs = {}
        for word in word_count_dict.keys():
            probs[word] = word_count_dict[word] / np.sum(list(word_count_dict.values()))
        return probs

    def delete_letter(self, word, verbose=False):
        delete_l = []
        for index in range(len(word)):
            delete_l.append(word[:index] + word[index + 1:])
        return delete_l

    def switch_letter(self, word, verbose=False):
        switch_l = []
        for index in range(len(word) - 1):
            switch_l.append(word[:index] + word[index + 1] + word[index] + word[index + 2:])
        return switch_l

    def replace_letter(self, word, verbose=False):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        replace_l = []
        for index in range(len(word)):
            for letter in letters:
                word_replaced = word[:index] + letter + word[index + 1:]
                if word_replaced not in replace_l + [word]:
                    replace_l.append(word_replaced)
        return sorted(replace_l)

    def insert_letter(self, word, verbose=False):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        insert_l = []
        for index in range(len(word)):
            for letter in letters:
                insert_l.append(word[:index] + letter + word[index:])
        return insert_l

if __name__ == '__main__':
    auto_correct = AutoCorrect()
    word_l = auto_correct.process_data('/../data/shakespeare.txt')
    word_count_dict = auto_correct.get_count(word_l)
    auto_correct.delete_letter(word="cans", verbose=True)
    auto_correct.switch_letter(word="eta", verbose=True)
    auto_correct.replace_letter(word='can', verbose=True)
    auto_correct.insert_letter('at', True)