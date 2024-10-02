# Expand previous Homework 5 with additional class, which allow to provide records by text file:
# 1.Define your input format (one or many records)
# 2.Default folder or user provided file path
# 3.Remove file if it was successfully processed
# 4.Apply case normalization functionality form Homework 3/4
from feeds import Input, Feed, News, PrivateAd, Journal


# Get information about input type.
data_type = input('Do you want to enter data manually/by file? (m/f) ').lower()

if data_type == 'f':
    feed_counter = 0
    custom_path = input('Do you want to provide path to the file? (y/n) ').lower()

    if custom_path == 'y' or custom_path == 'yes':
        custom_path = input('Enter path to the txt file with the input: ').lower()
        file_input = Input(custom_path, False)
        file_input.read_input_parameters()
    else:
        file_input = Input()
        file_input.get_input_from_all_files()

# Create new feed file if nox exists.
Feed.create_feed_file()
next_feed = True

while next_feed:
    if data_type == 'm':
        # Take an information from user.
        user_category = input('What category you want to add?\n"News" | "Private ad" | "Note": ').lower()
    else:
        user_category = file_input.input[feed_counter]['category'].lower()

    if user_category == 'news':
        if data_type == 'm':
            news_text = input('Provide news text: ')
            user_city = input('Provide city name: ').lower().title()
        else:
            news_text = file_input.input[feed_counter]['text']
            user_city = file_input.input[feed_counter]['additional']

        news = News(news_text, user_city)
        news.save_feed()

    elif user_category == 'private ad':
        if data_type == 'm':
            ad_text = input('Provide advertisement text: ')
            expiration_date = input('Provide expiration date (dd-mm-yyyy): ')
        else:
            ad_text = file_input.input[feed_counter]['text']
            expiration_date = file_input.input[feed_counter]['additional']

        ad = PrivateAd(ad_text, expiration_date)
        ad.save_feed()

    else:
        if data_type == 'm':
            note_text = input('Provide note text: ')
            user_name = input('Provide your name ').lower().title()
        else:
            note_text = file_input.input[feed_counter]['text']
            user_name = file_input.input[feed_counter]['additional']

        note = Note(note_text, user_name)
        note.save_feed()

    if data_type == 'm':
        next_insert = input('Do you want to insert another (y/n)? ').lower()
        if next_insert in ['y', 'yes']:
            next_feed = True
        else:
            next_feed = False
    else:
        feed_counter += 1
        if feed_counter == len(file_input.input):
            next_feed = False


print('\nFile has been saved.')
