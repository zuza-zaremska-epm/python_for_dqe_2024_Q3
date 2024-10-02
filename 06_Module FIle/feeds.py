import pendulum
import os


class Feed:
    file_path = 'Feed.txt'

    def __init__(self):
        self.insert_date = pendulum.now()
        self.feed = ''

    @classmethod
    def create_feed_file(cls):
        """If the file doesn't exist creates txt file to save new feeds."""
        if os.path.isfile(cls.file_path) is False:
            with open(cls.file_path, 'w', encoding='utf-8') as file:
                file.write('NEWS FEED\n')

    def save_feed(self):
        """Saves created feed in the txt file."""
        with open(self.file_path, 'a', encoding='utf-8') as file:
            file.write(self.feed + '\n')


class News(Feed):
    def __init__(self):
        super().__init__()
        self.city = input('Provide city name: ').lower().title()
        self.text = input('Provide news text: ')
        self.feed = f'\n--- NEWS ---\n{self.text}\n{self.city}, {self.insert_date.format("YYYY-MM-DD HH:mm")}'
        print(self.feed)


class PrivateAd(Feed):
    def __init__(self):
        super().__init__()
        self.text = input('Provide advertisement text: ')
        self.exp_date = pendulum.parse(input('Provide expiration date (YYYY-MM-DD): '), strict=False).date()
        self.days_left = (self.exp_date - self.insert_date.date()).days
        self.feed = f'\n--- PRIVATE AD ---\n{self.text}\nActual until: {self.exp_date.format("YYYY-MM-DD")} ({self.days_left} days left)'
        print(self.feed)


class Journal(Feed):
    def __init__(self):
        super().__init__()
        self.text = input('Provide journal text: ')
        self.name = input('Provide your name ').lower().title()
        self.mood = input("What's your mood today: ").lower()
        self.feed = f'\n--- JOURNAL ---\n{self.text}\nI feel {self.mood} today.\n{self.name}, {self.insert_date.format("YYYY-MM-DD HH:mm")}'
        print(self.feed)


class Input:
    def __init__(self, path='input/', default=True):
        self.path = path
        self.input = []
        if default:
            self.paths_list = [file for file in os.listdir(self.path) if file.endswith('.txt')]
            self.path_id = 0
            self.paths_num = len(self.paths_list)

    def change_path(self, new_path):
        self.path = 'input/' + new_path

    def delete_input_file(self):
        """Removes current file with input data."""
        os.remove(self.path)

    def read_input_parameters(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            loops = len(lines) // 4

            for i in range(loops):
                input_param = {
                    'category': lines[0].split("'")[1],
                    'text': lines[1].split("'")[1],
                    'additional': lines[2].split("'")[1]
                }

                self.input.append(input_param)
                lines = lines[4:]

        self.delete_input_file()

    def get_input_from_all_files(self):
        """
        Scans all available files in the default directory, retrieve
        input data and deletes the file.
        """
        for path in self.paths_list:
            self.change_path(path)
            self.read_input_parameters()


def create_feed_by_category(category: str):
    """
    Creates feed by the given category.
    :param category: name of the feed category/type
    """
    category = category.lower()

    if category in ['news', 'new']:
        feed = News()
    elif category in ['private ad', 'private', 'ad', 'priv']:
        feed = PrivateAd()
    else:
        feed = Journal()

    feed.save_feed()


# Create new feed file if not exists.
Feed.create_feed_file()

while True:
    # Take an information from user.
    user_category = input('What category you want to add?\n"News" | "Private ad" | "Journal": ')
    create_feed_by_category(user_category)

    next_insert = input('Do you want to insert another (y/n)? ').lower()
    if next_insert not in ['y', 'yes']:
        print('\nFile has been saved.')
        break
