import os

import numpy as np
from numpy import unique


class AutoCorrect:
    def __init__(self):
        pass

    def process_data(self, file_name):
        legal_words = []
        lines = open(os.getcwd() + f"{file_name}", "r").read().lower().split('\n')
        for line in lines:
            processed = [word.split('-') for word in line.split(' ')]
            for processed_words in processed:
                for processed_word in processed_words:
                    legal_word = processed_word
                    for token in " \"':;,.()[]{}<>+*/=~!@#$%^&*?":
                        legal_word = legal_word.replace(token, '')
                    if not legal_word.isnumeric() and len(legal_word) > 0:
                        legal_words.append(legal_word)
        return legal_words

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

    def edit_one_letter(self, word, allow_switches=True):
        return set(unique(self.insert_letter(word) + self.delete_letter(word) + self.replace_letter(word) + self.switch_letter(word)))

    def edit_two_letters(self, word, allow_switches=True):
        edit_two_set = []
        edit_one_set = self.edit_one_letter(word)
        for word in edit_one_set:
            edit_two_set += self.edit_one_letter(word)
        return set(edit_two_set)

    def edit_n_letters(self, edit_set, word, n=1):
        if n == 1:
            return self.edit_one_letter(word)
        edit_set_next = []
        for edit_word in edit_set:
            edit_set_next.append(self.edit_one_letter(edit_word))
        return self.edit_n_letters(edit_set_next, word, n - 1)

    def get_corrections(self, word, probs, vocab, n=2, verbose=False):
        if word in vocab:
            return [word]
        edit_probs_total = {}
        for edit_distance in range(1, n):
            edit_probs = {edit_word: probs[edit_word] for edit_word in self.edit_n_letters([], word, n=edit_distance).intersection(vocab)}
            edit_probs_total.update(edit_probs)
        max_probs = sorted(list(edit_probs_total.values()))[len(edit_probs_total.values()) - n:]
        edit_words = []
        for index in range(len(edit_probs_total.keys())):
            edit_word, edit_word_prob = list(edit_probs_total.keys())[index], list(edit_probs_total.values())[index]
            if edit_word_prob in max_probs:
                edit_words.append((edit_word, edit_word_prob))
        return sorted(edit_words, key=lambda edit_tuple: edit_tuple[1], reverse=True)

    def min_edit_distance(self, source, target, ins_cost=1, del_cost=1, rep_cost=2):
        rows, columns = len(source), len(target)
        distances = np.zeros((rows + 1, columns + 1), dtype=int)
        for row in range(0, rows + 1):
            distances[row, 0] = row * ins_cost
        for column in range(0, columns + 1):
            distances[0, column] = column * del_cost
        for row in range(1, rows + 1):
            for column in range(1, columns + 1):
                r_cost = 0 if source[row - 1] == target[column - 1] else rep_cost
                distances[row, column] = min(distances[row - 1, column - 1] + r_cost, distances[row - 1, column] + ins_cost, distances[row, column - 1] + del_cost)
        return distances, distances[rows, columns]

if __name__ == '__main__':
    auto_correct = AutoCorrect()
    vocab = auto_correct.process_data('/data/shakespeare.txt')
    word_count_dict = auto_correct.get_count(vocab)
    probs = auto_correct.get_probs(word_count_dict)
    auto_correct.delete_letter(word="cans", verbose=True)
    auto_correct.switch_letter(word="eta", verbose=True)
    auto_correct.replace_letter(word='can', verbose=True)
    auto_correct.insert_letter('at', True)
    auto_correct.edit_one_letter('can', True)
    auto_correct.edit_two_letters("at")
    auto_correct.edit_two_letters("at")
    auto_correct.get_corrections("dys", probs, vocab, 2, verbose=True)
    auto_correct.min_edit_distance('star', 'stack', ins_cost=2, del_cost=2, rep_cost=3)