import sys
import parsivar
import json
import hazm
from hazm import Stemmer, Lemmatizer
from parsivar import Normalizer, Tokenizer
from hazm import stopwords_list

def readtext():
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    f.close()
    return lines

def normalize(object):
    normalizer = Normalizer(pinglish_conversion_needed=True)
    normal = normalizer.normalize(object)
    return normal

def tokenize(object):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize_words(object)
    return tokens

def stopword(object):
    for i in object:
        if i in readtext():
            object.remove(i)
    return object

def stemmerandlemmatizer(object):
    stemmer = Stemmer()
    lemmatizer = Lemmatizer()
    for i in range(len(object)):
        object[i] = stemmer.stem(object[i])
        object[i] = lemmatizer.lemmatize(object[i])
    return object

def test():
    text = "من  به تاریخ  ۱۱ شهریور به دانشگاه می روم. man  be tarikhe 11 shahrivar be danshgah  miravam"
    print("Normal shode : ", normalize(text))
    print("Token haye be dast amade : ", tokenize(normalize(text)))
    print("Hazf kalamate por tekrar : ", stopword(tokenize(normalize(text))))
    print("Hazf kalamate ba rishe yeksan : ", stemmerandlemmatizer(stopword(tokenize(normalize(text)))))

test()