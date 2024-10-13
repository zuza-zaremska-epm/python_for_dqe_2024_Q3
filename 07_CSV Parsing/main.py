# Calculate number of words and letters from previous Homeworks 5/6 output test file.
# Create two csv:
# 1.word-count (all words are preprocessed in lowercase)
# 2.letter, count_all, count_uppercase, percentage (add header, spacecharacters are not included)
# CSVs should be recreated each time new record added.
from feeds import Input, Output, Feed, News, PrivateAd, Journal


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
        elif category in ['private ad', 'private', 'ad', 'priv']:
            text = input_details.get('text')
            exp_date = input_details.get('exp_date')
            feed = PrivateAd(text, exp_date)
        else:
            text = input_details.get('text')
            name = input_details.get('name')
            mood = input_details.get('mood')
            feed = Journal(text, name, mood)

        feed.save_feed()


# Create new feed file if not exists.
Feed.create_feed_file()
get_feeds = True

while get_feeds:
    # Get information about data ingestion type.
    ingestion = input('\nDo you want to enter data manually/by file? (m/f) ').lower()
    if ingestion in ['f', 'by file', 'file', 'files']:
        file_input = Input()
        custom_path = input('\nDo you want to provide path to the file? (y/n) ')
        if custom_path.lower() in ['y', 'yes']:
            file_input.get_path_from_user()
        else:
            file_input.get_paths_from_default_directory()

        file_input.get_input_from_files()
        for filename, feeds_details in file_input.input_data.items():
            for feed_params in feeds_details:
                create_feed_by_category(feed_params)
    else:
        user_category = input('What category you want to add?\n"News" | "Private ad" | "Journal": ')
        feed_params = {'category': user_category}
        create_feed_by_category(feed_params)

    next_insert = input('\nDo you want to insert another (y/n)? ')
    if next_insert.lower() not in ['y', 'yes']:
        get_feeds = False

print('\nFile has been saved.')
output = Output()
output.read_text(Feed.feed_file_path)
output.extract_words_from_text()
output.generate_word_count_file()
