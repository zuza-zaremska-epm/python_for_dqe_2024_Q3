import pendulum
import os

from abc import ABC, abstractmethod
from string import whitespace


class Feed(ABC):
    file_path = 'Feed.txt'

    def __init__(self, text):
        self.text = text
        self.feed = ''
        self.insert_date = pendulum.now()

    @classmethod
    def create_feed_file(cls):
        """If the file doesn't exist creates txt file to save new feeds."""
        if os.path.isfile(cls.file_path) is False:
            with open(cls.file_path, 'w', encoding='utf-8') as file:
                file.write('NEWS FEED\n')

    def save_feed(self):
        """Saves created feed in the txt file."""
        with open(Feed.file_path, 'a', encoding='utf-8') as file:
            file.write(self.feed + '\n')

    @abstractmethod
    def get_data_from_user(self):
        """Overwrite attributes with data from the user."""
        pass


class News(Feed):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city
        if not text:
            self.get_data_from_user()

        self.feed = f'\n--- NEWS ---\n{self.text}\n{self.city}, {self.insert_date.format("YYYY-MM-DD HH:mm")}'
        print(self.feed)

    def get_data_from_user(self):
        self.city = input('Provide city name: ').title()
        self.text = input('Provide news text: ')


class PrivateAd(Feed):
    def __init__(self, text, exp_date):
        super().__init__(text)
        self.exp_date = exp_date
        if not text:
            self.get_data_from_user()

        self.days_left = (self.exp_date - self.insert_date.date()).days
        self.feed = f'\n--- PRIVATE AD ---\n{self.text}\nActual until: {self.exp_date.format("YYYY-MM-DD")} ({self.days_left} days left)'
        print(self.feed)

    def get_data_from_user(self):
        self.text = input('Provide advertisement text: ')
        expiration_date = input('Provide expiration date (YYYY-MM-DD): ')
        self.exp_date = pendulum.parse(expiration_date, strict=False).date()


class Journal(Feed):
    def __init__(self, text, name, mood):
        super().__init__(text)
        self.name = name
        self.mood = mood
        if not text:
            self.get_data_from_user()

        self.feed = f'\n--- JOURNAL ---\n{self.text}\nI feel {self.mood} today.\n{self.name}, {self.insert_date.format("YYYY-MM-DD HH:mm")}'
        print(self.feed)

    def get_data_from_user(self):
        self.text = input('Provide journal text: ')
        self.name = input('Provide your name: ').title()
        self.mood = input("What's your mood today: ").lower()


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
            # TODO: Handle invalid path
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
            key = row[:row.find(':')]
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
        with open(self.current_path, 'r', encoding='utf-8') as file:
            feeds = file.read().split('<next_feed>')
            for feed in feeds:
                input_param = self.create_input_collection(feed)
                self.input_data[filename].append(input_param)

        self.delete_input_file()

    def get_input_from_files(self):
        """
        Scans all saved files paths from input_files attribute, retrieve
        input data and deletes the file.
        """
        for file_path in self.input_files_paths:
            self.change_path(file_path)
            self.read_feed_input_from_current_path()
