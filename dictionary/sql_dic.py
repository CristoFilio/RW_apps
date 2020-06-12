import mysql.connector
from difflib import get_close_matches

con = mysql.connector.connect(
        user='*',
        password='*',
        host='*',
        database='*'
)

cursor = con.cursor()

def query_pull(word, mode):
    if mode == 'exact_match':
        query = cursor.execute("SELECT * FROM words WHERE word = '{}'".format(word))
    elif mode == 'similar':
        #use regular expresions to find the first and last 3 letters of the word in the query
        query = (cursor.execute("SELECT word FROM words WHERE "
                                "word REGEXP '[[:<:]]{}' "
                                "OR word REGEXP '{}[[:>:]]' "
                                .format(word[:3], word[-4:])))
    query_return = cursor.fetchall()
    return query_return


def dictionary():
    while True:
        word = input('\nPlease type a word to define.\nType close program to exit: ').lower()
        while not word.isalpha():
            word = input('\nPlease type a word to define, no numeric values are accepted: ').lower()
        number = 1
        query_return = query_pull(word, 'exact_match')
        if word == 'close program':
            print('Thank you for using this software')
            break

        if len(query_return) > 0:

            if word in query_return[0][1].lower():
                print('\n{}:'.format(word.capitalize()))

                for definition in query_return:
                    print('{}.- {}'.format(number, definition[0]))
                    number += 1
        else:

            query_return = query_pull(word, 'similar')
            if len(query_return) > 0:
                suggested_words = set(get_close_matches(word, [result[0].lower() for result in query_return]))
                print('\nDid you mean to type one of these words?')
                print(", ".join([word.capitalize() for word in suggested_words]))
            else:
                print('\nThat word does not exist in the dictionary')

if __name__ == "__main__":
    dictionary()
