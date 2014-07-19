from nltk.tokenize import blankline_tokenize

def extract(text):
    '''
    Split a text in a context

    :param text: the text to contextualize
    :return: array of string representing the context
    '''
    return blankline_tokenize(text)
