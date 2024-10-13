import csv
import pendulum
import os

from abc import ABC, abstractmethod
from collections import Counter
from string import whitespace, punctuation, digits


class Feed(ABC):
    feed_file_path = 'output/Feed.txt'

    def __init__(self, text):
        self.text = text
        self.type = None
        self.feed = None
        self.insert_date = pendulum.now()

    @classmethod
    def create_feed_file(cls):
        """If the file doesn't exist creates txt file to save new feeds."""
        if os.path.isfile(cls.feed_file_path) is False:
            with open(cls.feed_file_path, 'w', encoding='utf-8') as file:
                file.write('NEWS FEED\n')

    @abstractmethod
    def get_data_from_user(self):
        """Overwrite attributes with data from the user."""
        pass

    @abstractmethod
    def create_feed(self):
        """Creates feed in the form characteristic for specific feed type."""
        pass

    def save_feed(self):
        """Saves created feed in the txt file."""
        self.create_feed()
        with open(Feed.feed_file_path, 'a', encoding='utf-8') as file:
            file.write(self.feed + '\n')

    def normalize_text(self):
        """
        Normalizes text attribute to the form where each sentence starts with
        the capital letter.
        """
        lines = self.text.lower().split('.')

        for line_index, line in enumerate(lines):
            for char in line:
                if char not in whitespace:
                    line = line.replace(char, char.upper(), 1)
                    break

            lines[line_index] = line

        self.text = '.'.join(lines)


class News(Feed):
    def __init__(self, text, city):
        super().__init__(text)
        self.type = '--- NEWS ---'
        self.city = city
        if not text:
            self.get_data_from_user()
        self.normalize_text()

    def get_data_from_user(self):
        self.city = input('Provide city name: ').title()
        self.text = input('Provide news text: ')

    def create_feed(self):
        self.feed = f'\n{self.type}\n{self.text}\n{self.city}, {self.insert_date.format("YYYY-MM-DD HH:mm")}'
        print(self.feed)


class PrivateAd(Feed):
    def __init__(self, text: str, exp_date: str):
        super().__init__(text)
        self.type = '--- PRIVATE AD ---'
        self.exp_date = exp_date
        if not text:
            self.get_data_from_user()
        self.normalize_text()

        self.exp_date = pendulum.parse(self.exp_date, strict=False).date()
        self.days_left = (self.exp_date - self.insert_date.date()).days

    def get_data_from_user(self):
        self.text = input('Provide advertisement text: ')
        self.exp_date = input('Provide expiration date (YYYY-MM-DD): ')

    def create_feed(self):
        self.feed = f'\n{self.type}\n{self.text}\nActual until: {self.exp_date.format("YYYY-MM-DD")} ({self.days_left} days left)'
        print(self.feed)


class Journal(Feed):
    def __init__(self, text, name, mood):
        super().__init__(text)
        self.type = '--- JOURNAL ---'
        self.name = name
        self.mood = mood
        if not text:
            self.get_data_from_user()
        self.normalize_text()

    def get_data_from_user(self):
        self.text = input('Provide journal text: ')
        self.name = input('Provide your name: ').title()
        self.mood = input("What's your mood today: ").lower()

    def create_feed(self):
        self.feed = f'\n{self.type}\n{self.text}\nI feel {self.mood} today.\n{self.name}, {self.insert_date.format("YYYY-MM-DD HH:mm")}'
        print(self.feed)


class Input:
    default_path = 'input/'

    def __init__(self):
        self.current_path = None
        self.input_files_paths = []
        self.input_data = {}

    def get_paths_from_default_directory(self):
        """
        Save paths to the files in the default directory
        in the input_files.
        """
        self.input_files_paths = [f"{Input.default_path}{file}" for file in
                                  os.listdir(Input.default_path) if file.endswith('.txt')]

    def get_path_from_user(self):
        """
        Get path to the input file from the user. If not provided,
        read from the default directory.
        """
        user_path = input('Enter path to the txt file with the input: ').lower()
        if user_path:
            self.input_files_paths.append(user_path)
        else:
            self.get_paths_from_default_directory()

    def change_path(self, new_path):
        """
        Update path variable for the new file.
        :param new_path: path to the new file
        """
        print(f'Changed "{self.current_path}" path to "{new_path}".')
        self.current_path = new_path

    def delete_input_file(self):
        """Remove file from the current path."""
        os.remove(self.current_path)
        print(f'Removed input file: {self.current_path}')

    @staticmethod
    def create_input_collection(feed: str) -> dict:
        """
        From the given feed retrieve input parameters.
        :param feed: feed details
        :return: collection of feed input data
        """
        input_collection = {}

        for row in feed.split(';'):
            row = row.strip(whitespace)
            key = row[:row.find(':')].lower()
            value = row[(row.find("'")+1):-1]
            input_collection[key] = value

        return input_collection

    def read_feed_input_from_current_path(self):
        """
        Read all feeds data from the file currently specified in the
        current_path attribute. Remove file after reading data.
        """
        filename = self.current_path.split('/')[-1]
        self.input_data[filename] = []
        try:
            with open(self.current_path, 'r', encoding='utf-8') as file:
                feeds = file.read().split('<next_feed>')
                for feed in feeds:
                    feed_params = self.create_input_collection(feed)
                    self.input_data[filename].append(feed_params)

            self.delete_input_file()
        except FileNotFoundError as e:
            print(e)

    def get_input_from_files(self):
        """
        Scans all saved files paths from input_files attribute, retrieve
        input data and deletes the file.
        """
        for feed_file_path in self.input_files_paths:
            self.change_path(feed_file_path)
            self.read_feed_input_from_current_path()


class Output:
    target_dir = 'output/'

    def __init__(self):
        self.text = None
        self.words = []

    def read_text(self, path_to_file: str):
        """
        Reads the content of the text file from given path.
        :param path_to_file: path to the text file
        """
        with open(path_to_file, encoding='utf-8') as file:
            self.text = file.read()

    def extract_words_from_text(self):
        """Extracts from the text all words."""
        chars_to_remove = (punctuation + digits + whitespace).replace(' ', '')
        translator = str.maketrans('', '', chars_to_remove)

        # Remove from the text special chars and digits.
        cleaned_text = (self.text.translate(translator)).lower()
        self.words = [word for word in cleaned_text.split(' ')]
        self.words.sort()

    def generate_word_count_file(self):
        """Creates CSV file with list of words and number of occurrences."""
        words_collection = Counter(self.words)
        print(words_collection)

        with open(
                file=f'{Output.target_dir}word_count.csv',
                mode='w',
                encoding='utf-8',
                newline=''
        ) as file:
            file_writer = csv.writer(file)
            for word, num_of_occurrence in words_collection.items():
                file_writer.writerow(([word, num_of_occurrence]))
