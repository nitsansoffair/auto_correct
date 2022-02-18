import os


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

if __name__ == '__main__':
    auto_correct = AutoCorrect()
    print(auto_correct.process_data("/data/shakespeare.txt"))