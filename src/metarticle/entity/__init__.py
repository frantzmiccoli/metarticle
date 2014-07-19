import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def resolveAnaphores(text):
    return text

def extract(text):
    '''
    :param text: a text to extract entity from
    :return:
    '''

    # Cut out words from the context and part-of-speech tag them
    words = word_tokenize(text)
    pos = pos_tag(words)

    # Extract noun-typed entities
    entities = []
    for (word, tag) in pos:
        if tag.startswith('NN'):
            entities.append(word)

    entities
