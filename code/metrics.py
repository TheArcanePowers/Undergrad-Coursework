from collections import OrderedDict  # for part 2.4. Python 3.7 has ordered dictionaries, but this is considered better by industry plus increases compatibility
# #!EXTRA# Following imports are for bar chart
import matplotlib.pyplot as plt


# PART 2
class Metrics():
    """A class to represent the metrics for a given message.

    Attributes
        raw_message (str): Message to be analyzed.
        total_words (int): Number of total words used in message.
        num_words (int): Number of unique words used in message.
        min_word_len (int): Length of shortest word in message.
        max_word_len (int): Length of longest word in message.

    Methods
        export_metrics(filepath="" (optional)): Writes metrics to metrics.txt.
        print_sorted_words(): Print (up to) the five most frequently occuring words.
    """

    def __init__(self, raw_message):
        """Initialize and generate metrics.

        Args:
            raw_message (str): the raw message which will get analyzed.
        """
        self.sort_words_been_called = False  # #!EXTRA#
        # PART 2.1
        raw_message = raw_message.strip().lower()  # Imposing lower to ensure words with different capitalization are counted
        words = raw_message.split(" ")
        self.clean_words = []
        for item in words:  # Should have just used regex, but not included in the exercises so didn't want to lose out on marks
            clean_word = [char for char in item if char.isalpha()]  # Should check if each char is in the alphabet, and if so add it
            clean_word = "".join(clean_word)
            self.clean_words.append(clean_word)
        # Analysis
        self.total_words = len(self.clean_words)
        self.unique_words = set(self.clean_words)  # useful for part 2.3
        self.num_words = len(self.unique_words)  # sets are unique
        self.min_word_len = min(self.clean_words, key=len)
        self.max_word_len = max(self.clean_words, key=len)
        # Analysis: most common letter
        temp_dictionary = {}
        for word in self.clean_words:
            for char in word:
                if char in temp_dictionary:
                    temp_dictionary[char] += 1
                else:
                    temp_dictionary[char] = 1
        self.common_char = max(temp_dictionary, key=temp_dictionary.get)

    def print_metrics(self):  # Debug
        """Write metrics to console."""
        print(self.total_words, self.num_words, self.min_word_len, self.max_word_len, self.common_char)

    # Part 2.2
    def export_metrics(self, filepath=""):
        """Write metrics to file.

        Args:
            filepath (str, optional): Relative file location prepended to metrics.txt to write to. Defaults to "".
        """
        with open(f"{filepath}metrics.txt", "w") as f:
            f.write(f"total number of words: {self.total_words}\n")
            f.write(f"number of unique words: {self.num_words}\n")
            f.write(f"minimum word length: {self.min_word_len}\n")
            f.write(f"maximum word length: {self.max_word_len}\n")
            f.write(f"most common letter: {self.common_char}\n")

    # PART 2.3
    def sort_words(self):
        """Print (up to) the five most frequently occuring words."""
        self.sort_words_been_called = True  # #!EXTRA#  Like this I know if it has been called, if not I call it to gen self.word_dictionary
        if len(self.unique_words) <= 5:
            print(self.unique_words)
            return
        else:
            temp_dictionary = {}
            for word in self.clean_words:
                if word in temp_dictionary:
                    temp_dictionary[word] += 1
                else:
                    temp_dictionary[word] = 1
        n = 1
        while len(temp_dictionary) > 5:
            temp_dictionary = {char: freq for char, freq in temp_dictionary.items() if freq != n}  # Iterates over whole dictionary, recreating it except for values with a key equal to n. n starts at 1, and increments each time until list is less than 6
            n += 1
        list_of_words = list(temp_dictionary.keys())  # told to return a list. without list() would return dict_keys object which is close but not quite a list
        # PART 2.4
        ordered_dict = OrderedDict(sorted(temp_dictionary.items(), key=lambda x: x[1], reverse=True))  # https://docs.python.org/3/howto/sorting.html
        self.word_dictionary = {}
        for keyvalue in ordered_dict.items():
            self.word_dictionary[str(keyvalue[0])] = keyvalue[1]
        return list_of_words, self.word_dictionary

    # #!EXTRA# Produce a bar chart to show metrics
    def produce_barchart(self):
        """Generate a MatPlotLib bar chart of most frequently occuring messages."""
        if self.sort_words_been_called is False:
            self.sort_words()
            self.produce_barchart()
        else:
            plt.xlabel("Most frequently occuring words")
            plt.ylabel("Frequency appearing in message")
            plt.bar(range(len(self.word_dictionary)), self.word_dictionary.values(), tick_label=list(self.word_dictionary.keys()))
            plt.show()
            plt.savefig('bar_chart.pdf')


# Debug
# raw_message = "Here you see a long message for you to encrypt, it may take you a while"
# m = Metrics(raw_message)
# #m.print_metrics()
# list_of_words, word_dictionary = m.sort_words()
# # print(list_of_words)
# # print(word_dictionary)
# m.produce_barchart()
