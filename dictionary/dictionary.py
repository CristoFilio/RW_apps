import json
from difflib import get_close_matches

data_frame = json.load(open('data.json'))
formatted_df = {key.lower(): data_frame[key] for key in data_frame}

def dictionary():
    while True:
        word = input('\nPlease type a word to define: ').lower()
        number = 1

        if word in formatted_df.keys():
            print('{}:\n'.format(word.capitalize()))
            for definition in formatted_df[word]:
                print('{}.- {}'.format(number, definition))
                number += 1
        else:
            suggested_words = get_close_matches(word, formatted_df.keys())
            if len(suggested_words) > 0:
                print('\nDid you mean to type one of these words?')
                print(", ".join([word.capitalize() for word in suggested_words]))
            else:
                print('\nThat word does not exist in the dictionary')

if __name__ == "__main__":
    dictionary()