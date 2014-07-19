import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import RegexpTokenizer


def resolve_anaphores(text):
    return text

def extract(text):
    '''
    :param text: a text to extract entity from
    :return:
    '''

    # Load wordnet
    wordnet = WordNetLemmatizer()

    # Cut out words from the context and part-of-speech tag them
    words = RegexpTokenizer(r'[a-z]+').tokenize(text)
    pos = pos_tag(words)

    # Extract noun-typed entities
    entities = []
    for (word, tag) in pos:
        if tag.startswith('NN') and word not in stopwords.words():
            entities.append(wordnet.lemmatize(word))

    return entities
