from nltk.tokenize import sent_tokenize

def extract(text):
    '''
    Split a text in a context

    :param text: the text to contextualize
    :return: array of string representing the context
    '''
    return sent_tokenize(text)
