# Expand previous Homework 5/6/7/8/9 with additional class, which allow to save records into database:
# 1.Different types of records require different data tables
# 2.New record creates new row in data table
# 3.Implement “no duplicate” check.
from feeds import Input, InputText, InputJson, InputXml, Output, DatabaseManager
from feeds import Feed, News, PrivateAd, Journal


def create_feed_by_category(input_details: dict):
    """
    Creates feed by the given input details.
    :param input_details: data provided for the feed
    """
    category = input_details.get('category').lower()

    if not category:
        print('Category not provided - impossible to create.')
    else:
        if category in ['news', 'new']:
            text = input_details.get('text')
            city = input_details.get('city')
            feed = News(text, city)
            input_details.update({'category': 'news', 'text': feed.text, 'city': feed.city})
        elif category in ['private ad', 'private', 'ad', 'priv']:
            text = input_details.get('text')
            exp_date = input_details.get('exp_date')
            feed = PrivateAd(text, exp_date)
            input_details.update({'category': 'private ad', 'text': feed.text, 'exp_date': feed.exp_date})
        else:
            text = input_details.get('text')
            name = input_details.get('name')
            mood = input_details.get('mood')
            feed = Journal(text, name, mood)
            input_details.update({'category': 'journal', 'text': feed.text, 'name': feed.name, 'mood': feed.mood})

        feed.save_feed()
        print(input_details)
        return input_details


def adjust_input_to_user_path() -> Input:
    """
    Get path to the custom file from the user and adjust input type to the
    given path.
    :return: adjusted input type
    """
    user_path = input('Provide path to the file: ').lower()
    file_extension = user_path.split('.')[-1]
    if file_extension == 'txt':
        input_type = InputText()
    elif file_extension == 'json':
        input_type = InputJson()
    elif file_extension == 'xml':
        input_type = InputXml()
    else:
        # Invalid file path will be ignored.
        input_type = InputText()

    input_type.get_user_path(user_path)
    return input_type


DB_TABLES_CONFIG = {
    'news': {
        'news_id': 'INT PRIMARY KEY',
        'news_text': 'TEXT',
        'news_city': 'TEXT'
    },
    'private_ads': {
        'private_ad_id': 'INT PRIMARY KEY',
        'private_ad_text': 'TEXT',
        'private_ad_exp_date': 'TEXT'
    },
    'journals': {
        'journal_id': 'INT PRIMARY KEY',
        'journal_text': 'TEXT',
        'journal_author_name': 'TEXT',
        'journal_author_mood': 'TEXT'
    }
}

# Connect to database.
db = DatabaseManager(db_name='feeds', db_configuration=DB_TABLES_CONFIG)
db.connect_to_database()
db.create_database_structure()

# Create new feed file if not exists.
Feed.create_feed_file()
get_feeds = True

while get_feeds:
    # Get information about data ingestion type.
    ingestion = input('\nDo you want to enter data manually/by file? (m/f) ').lower()
    if ingestion in ['f', 'by file', 'file', 'files']:
        inputs = []
        custom_path = input('\nDo you want to provide path to the file? (y/n) ')
        if custom_path.lower() in ['y', 'yes']:
            input_instance = adjust_input_to_user_path()
            inputs.append(input_instance)
        else:
            # Get data from the input dict for all input types.
            for input_instance in [InputText(), InputJson(), InputXml()]:
                input_instance.get_paths_from_default_directory()
                inputs.append(input_instance)

        for input_instance in inputs:
            input_instance.get_input_from_files()
            for filename, feeds_details in input_instance.input_data.items():
                for feed_params in feeds_details:
                    feed_params = create_feed_by_category(feed_params)
                    db.insert_data(feed_params)
    else:
        user_category = input('What category you want to add?\n"News" | "Private ad" | "Journal": ')
        feed_params = {'category': user_category}
        feed_params = create_feed_by_category(feed_params)
        db.insert_data(feed_params)

    next_insert = input('\nDo you want to insert another (y/n)? ')
    if next_insert.lower() not in ['y', 'yes']:
        get_feeds = False

db.disconnect_from_database()
print('\nFeed file has been saved.')

output = Output()
output.read_text(Feed.feed_file_path)

output.extract_words_from_text()
output.generate_word_count_file()

output.generate_letter_count_file()
