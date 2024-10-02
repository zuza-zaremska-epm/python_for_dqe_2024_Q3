# Expand previous Homework 5 with additional class, which allow to provide records by text file:
# 1.Define your input format (one or many records)
# 2.Default folder or user provided file path
# 3.Remove file if it was successfully processed
# 4.Apply case normalization functionality form Homework 3/4
from feeds import Input, Feed, News, PrivateAd, Journal


def create_feed_by_category(category: str, input_collection: dict):
    """
    Creates feed by the given category.
    :param category: name of the feed category
    :param input_collection: data provided for the feed
    """
    category = category.lower()

    if category in ['news', 'new']:
        text = input_collection.get('text')
        city = input_collection.get('city')
        feed = News(text, city)
    elif category in ['private ad', 'private', 'ad', 'priv']:
        text = input_collection.get('text')
        exp_date = input_collection.get('exp_date')
        feed = PrivateAd(text, exp_date)
    else:
        text = input_collection.get('text')
        name = input_collection.get('name')
        mood = input_collection.get('mood')
        feed = Journal(text, name, mood)

    feed.save_feed()


# Get information about data ingestion type.
ingestion = input('Do you want to enter data manually/by file? (m/f) ').lower()
if ingestion in ['f', 'by file', 'file']:
    custom_path = input('Do you want to provide path to the file? (y/n) ')
    if custom_path.lower() in ['y', 'yes']:
        custom_path = input('Enter path to the txt file with the input: ').lower()
        file_input = Input(path=custom_path)
        file_input.read_input_parameters()
    else:
        file_input = Input()
        file_input.get_input_from_all_files()


# Create new feed file if not exists.
Feed.create_feed_file()
feed_counter = 0
# Populate feed file with data.
while True:
    if ingestion in ['f', 'by file', 'file']:
        feed_counter += 1
        input_data = file_input.input[feed_counter]
        feed_category = input_data.get('category')
        create_feed_by_category(feed_category, input_data)

        if feed_counter == len(file_input.input):
            break

    else:
        user_category = input('What category you want to add?\n"News" | "Private ad" | "Journal": ')
        create_feed_by_category(user_category, {})

        next_insert = input('Do you want to insert another (y/n)? ')
        if next_insert.lower() not in ['y', 'yes']:
            break

print('\nFile has been saved.')
