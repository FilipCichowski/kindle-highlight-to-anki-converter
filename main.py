import re
import genanki
from PyDictionary import PyDictionary

highlight_separator = "=========="
non_letter_non_space_regex = "[^a-zA-Z ]+"

dictionary = PyDictionary()


def filterContentFromLine(raw_string):
    split_string = raw_string.split("\n")
    content = split_string[-2]
    return re.sub(non_letter_non_space_regex, "", content).lower()


def generateCardAnswer(translation_obj):
    answer = ""
    index = 1
    for key in translation_obj:
        for meaning in translation_obj.get(key):
            answer += f"<strong> </strong>{str(index)}. {meaning}\n"
            index = index + 1
    return answer


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

with open("My Clippings.txt", "r") as file:
    data = file.read()

highlights = data.split(highlight_separator)

for raw_string in highlights:
    word_list = filterContentFromLine(raw_string).split(" ")
    for word in word_list:
        translation_obj = dictionary.meaning(word)
        my_note = genanki.Note(
            model=my_model,
            fields=[word, generateCardAnswer(translation_obj)])
        my_deck.add_note(my_note)

genanki.Package(my_deck).write_to_file('output.apkg')