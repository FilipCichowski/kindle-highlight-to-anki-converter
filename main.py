import re
import genanki
from PyDictionary import PyDictionary
from pathvalidate import sanitize_filepath
import sys

highlight_separator = "=========="
non_letter_non_space_regex = "[^a-zA-Z ]+"

dictionary = PyDictionary()


def filter_content_from_line(raw_string):
    split_string = raw_string.split("\n")
    content = split_string[-2]
    return re.sub(non_letter_non_space_regex, "", content).lower()


def generate_card_answer(word):
    answer = ""
    index = 1
    translation_obj = dictionary.meaning(word, disable_errors=True)
    try:
        for key in translation_obj:
            for meaning in translation_obj.get(key):
                answer += f"<strong> </strong>{str(index)}. {meaning}<br>"
                index = index + 1
        return answer
    # if None was returned which means word wasn't find in dictionary
    except TypeError:
        print(f"Can't find word '{word}' in dictionary, no card is generated.")
        return None


def read_data_fom_file(path):
    try:
        with open(path, "r") as file:
            data = file.read()
            return data
    except OSError:
        print(f"Cant open file {path}. Try again!")
        return None


def get_path_from_user():
    path = sanitize_filepath(input("Enter path to 'My Clippings.txt' from your Kindle or click Enter if file is "
                                   "located in main folder: "))
    if path == "":
        return "My Clippings.txt"
    else:
        return path


def get_data():
    data = read_data_fom_file(get_path_from_user())
    if data is None:
        get_data()
    else:
        return data


my_model = genanki.Model(
    1607392319,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '<h1>{{Question}}<h1>',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])

my_deck = genanki.Deck(
    2059400110,
    'My clippings')

print("""
  /$$$$$$  /$$ /$$                     /$$                                     /$$$$$$$$               /$$$$$$            /$$       /$$
 /$$__  $$| $$|__/                    |__/                                    |__  $$__/              /$$__  $$          | $$      |__/
| $$  \__/| $$ /$$  /$$$$$$   /$$$$$$  /$$ /$$$$$$$   /$$$$$$   /$$$$$$$         | $$  /$$$$$$       | $$  \ $$ /$$$$$$$ | $$   /$$ /$$
| $$      | $$| $$ /$$__  $$ /$$__  $$| $$| $$__  $$ /$$__  $$ /$$_____/         | $$ /$$__  $$      | $$$$$$$$| $$__  $$| $$  /$$/| $$
| $$      | $$| $$| $$  \ $$| $$  \ $$| $$| $$  \ $$| $$  \ $$|  $$$$$$          | $$| $$  \ $$      | $$__  $$| $$  \ $$| $$$$$$/ | $$
| $$    $$| $$| $$| $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$ \____  $$         | $$| $$  | $$      | $$  | $$| $$  | $$| $$_  $$ | $$
|  $$$$$$/| $$| $$| $$$$$$$/| $$$$$$$/| $$| $$  | $$|  $$$$$$$ /$$$$$$$/         | $$|  $$$$$$/      | $$  | $$| $$  | $$| $$ \  $$| $$
 \______/ |__/|__/| $$____/ | $$____/ |__/|__/  |__/ \____  $$|_______/          |__/ \______/       |__/  |__/|__/  |__/|__/  \__/|__/
                  | $$      | $$                     /$$  \ $$                                                                         
                  | $$      | $$                    |  $$$$$$/                                                                         
                  |__/      |__/                     \______/                                                                          
""")

data = get_data()

# highlights = data.split(highlight_separator)
#
# for raw_string in highlights:
#     word_list = filterContentFromLine(raw_string).split(" ")
#     for word in word_list:
#         card_answer = generateCardAnswer(word)
#         if card_answer is not None:
#             my_note = genanki.Note(
#                 model=my_model,
#                 fields=[word, card_answer])
#             my_deck.add_note(my_note)
#
# genanki.Package(my_deck).write_to_file('output.apkg')
