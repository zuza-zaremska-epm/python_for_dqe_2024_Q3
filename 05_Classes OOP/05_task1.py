# Create a tool, which will do user generated news feed:
# 1.User select what data type he wants to add
# 2.Provide record type required data
# 3.Record is published on text file in special format
#
# You need to implement:
# 1.News – text and city as input. Date is calculated during publishing.
# 2.Private ad – text and expiration date as input. Day left is calculated during publishing.
# 3.Your unique one with unique publish rules.
#
# Each new record should be added to the end of file. Commit file in git for review.
import pendulum
import os


class Feed:
    file_path = 'Feed.txt'

    def __init__(self, text):
        self.text = text
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
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city
        self.feed = f'\n--- NEWS ---\n{self.text}\n{self.city}, {self.insert_date.format("YYYY-MM-DD HH:mm")}'
        print(self.feed)


class PrivateAd(Feed):
    def __init__(self, text: str, exp_date: str):
        super().__init__(text)
        self.exp_date = pendulum.parse(exp_date).date()
        self.days_left = (self.exp_date - self.insert_date.date()).days
        self.feed = f'\n--- PRIVATE AD ---\n{self.text}\nActual until: {self.exp_date.format("YYYY-MM-DD")} ({self.days_left} days left)'
        print(self.feed)


class Journal(Feed):
    def __init__(self, text, name, mood_name):
        super().__init__(text)
        self.name = name.title()
        self.mood = mood_name.lower()
        self.feed = f'\n--- JOURNAL ---\n{self.text}\nI feel {mood_name} today.\n{self.name}, {self.insert_date.format("YYYY-MM-DD HH:mm")}'
        print(self.feed)


def create_feed_by_category(category: str):
    """
    Creates feed by the given category.
    :param category: name of the feed category/type
    """
    if category in ['news', 'new']:
        user_city = input('Provide city name: ').lower().title()
        news_text = input('Provide news text: ')

        news = News(news_text, user_city)
        news.save_feed()

    elif category in ['private ad', 'private', 'ad', 'priv']:
        ad_text = input('Provide advertisement text: ')
        expiration_date = input('Provide expiration date (YYYY-MM-DD): ')

        ad = PrivateAd(ad_text, expiration_date)
        ad.save_feed()

    else:
        mood = input("What's your mood today: ").lower()
        journal_text = input('Provide journal text: ')
        user_name = input('Provide your name ').lower().title()

        journal = Journal(journal_text, user_name, mood)
        journal.save_feed()


# Create new feed file if not exists.
Feed.create_feed_file()

while True:
    # Take an information from user.
    user_category = input('What category you want to add?\n"News" | "Private ad" | "Journal": ').lower()
    create_feed_by_category(user_category)

    next_insert = input('Do you want to insert another (y/n)? ').lower()
    if next_insert not in ['y', 'yes']:
        print('\nFile has been saved.')
        break
