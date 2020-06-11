def formater():
    text = ''
    interrogatives = ('why', 'how', 'when', 'who', 'what')
    while True:
        to_format = input('Say something: ').capitalize()
        if '/end' in to_format:
            return print(text)
        elif question_check(to_format, interrogatives):
            text += '{}? '.format(to_format)
        else:
            text += '{}. '.format(to_format)

def question_check(sentence, list_of_words):
    for word in list_of_words:
        if word in sentence.lower():
            return True

formater()