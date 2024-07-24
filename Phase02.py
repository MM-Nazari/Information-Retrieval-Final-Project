import sys
import parsivar
import json
import hazm
from hazm import Stemmer, Lemmatizer
from parsivar import Normalizer, Tokenizer
from hazm import stopwords_list
import numpy
import math



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


# komak gerefte shode az geeksforgeeks
def positionalindex(object):
    positionalIndex = {}
    # iterate bar rooye hame tokenha dar file
    # i position har token ra taeen mikonad
    # content[i] meghdar ya khode token ra taeen mikonad
    for DocID in object.keys():
        # pardazesh faghat rooye content
        content = stemmerandlemmatizer(stopword(tokenize(normalize(object[DocID]['content']))))
        for i in range(len(content)):
            # agar token dar dictionary mojood bood
            if content[i] in positionalIndex:
                # tedad tekrar dar asnad 1 adad ezafe shavad
                positionalIndex[content[i]][0] += 1
                # agar docid ghbalan sabt shode bood
                if DocID in positionalIndex[content[i]][1]:
                    # be list position ha position jadid yani i ezafe shavad
                    positionalIndex[content[i]][1][DocID].append(i)
                # agar docid jadid ast
                else:
                    # position feli be onvan avalin position list sabt shavad
                    positionalIndex[content[i]][1][DocID] = [i]
            # agar token jadid ast
            else:
                # yek list be onvane value misazim
                positionalIndex[content[i]] = []
                # 1 ra be onvan tedad tekrar ya frequency sabt mikonim
                positionalIndex[content[i]].append(1)
                # dictionary be onavan ozve dovvome list baraye sabt position ha hamrahe docid misazim
                positionalIndex[content[i]].append({})
                # positon feli yani i ra be onvan avvalin position baraye docid feli sabt mikonim
                positionalIndex[content[i]][1][DocID] = [i]
    return positionalIndex


def readjson():
    # read file
    with open('data2.json', 'r', encoding='utf-8') as myfile:
        data = myfile.read()
    # parse file
    obj = json.loads(data)
    myfile.close()
    return obj


content = []
URL = []
title = []


def contenturltitle(object):
    tokenizer = Tokenizer()
    for DocID in object.keys():
        title.append(object[DocID]["title"])
        content.append(object[DocID]["content"])
        URL.append(object[DocID]["url"])
        # sentences.append(tokenizer.tokenize_sentences(content[int(DocID)]))


contenturltitle(readjson())
positionalindexx = positionalindex(readjson())
idfs = []


def tfidf(positionalindexx):
    for i in positionalindexx.keys():
        positionalindexx[i].append([])
        idf = math.log(201 / len(positionalindexx[i][1]), 10)
        idfs.append(idf)
        for j in positionalindexx[i][1].keys():
            tf = 1 + math.log(len(positionalindexx[i][1][j]), 10)
            positionalindexx[i][2].append(idf * tf)
    return positionalindexx


champions_list = {}


def Cloning(li1):
    li_copy = li1[:]
    return li_copy


def champion_list(positionalindexx):
    for i in positionalindexx.keys():
        champions_list.update({i: []})
        positionalindexx[i].append([])
        if len(positionalindexx[i][1].keys()) <= 5:
            positionalindexx[i][3] = Cloning(positionalindexx[i][2])
            for j in positionalindexx[i][1].keys():
                champions_list[i].append(j)

        else:
            list1, list2 = zip(*sorted(zip(positionalindexx[i][2], positionalindexx[i][1].keys())))
            #print(list1)
            #print(list2)
            for j in list2[-5:]:
                champions_list[i].append(j)
            for k in list1[-5:]:
                positionalindexx[i][3].append(k)

    return positionalindexx


positionalindex = champion_list(tfidf(positionalindexx))
print("Positional Index Of لیگ : ", positionalindex["لیگ"])
print("Champion List Of لیگ : ", champions_list["لیگ"])

print("Positional Index Of برتر : ", positionalindex["برتر"])
print("Champion List Of برتر : ", champions_list["برتر"])

print("Positional Index Of فوتبال : ", positionalindex["فوتبال"])
print("Champion List Of فوتبال : ", champions_list["فوتبال"])

print("Positional Index Of مایکل : ", positionalindex["مایکل"])
print("Champion List Of مایکل : ", champions_list["مایکل"])

print("Positional Index Of جردن : ", positionalindex["جردن"])
print("Champion List Of جردن : ", champions_list["جردن"])

print("Positional Index Of آمریکا : ", positionalindex["آمریکا"])
print("Champion List Of آمریکا : ", champions_list["آمریکا"])

ranks = [0] * 201


def cosine(query, scores):
    length = [0] * 201
    for i in range(len(query)):
        counter = 0
        for j in champions_list[query[i]]:
            try:
                ranks[int(j)] += scores[i] * positionalindex[query[i]][3][counter]
                length[int(j)] += positionalindex[query[i]][3][counter] * positionalindex[query[i]][3][counter]
                counter += 1
            except KeyError:
                continue

    for i in range(0, 201, 1):
        if length[i] != 0:
            ranks[i] /= length[i]
        else:
            continue

    return ranks


def jaccard(query):
    for i in range(0, 201, 1):
        doc = stemmerandlemmatizer(stopword(tokenize(normalize(content[i]))))
        union = set(doc).union(query)
        intersect = set(doc).intersection(query)
        ranks[i] = len(intersect) / len(union)

    return ranks


def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices


def query():
    query = stemmerandlemmatizer(stopword(tokenize(normalize(input("لطفا پرسمان را وارد کنید: ")))))
    scores = []
    doc_scores = []
    top_list = []

    for word in range(len(query)):
        if query[word] in positionalindex.keys():
            for i in range(len(positionalindex.keys())):
                tempp = list(positionalindex.keys())
                if tempp[i] == query[word]:
                    scores.append(idfs[i])
        else:
            continue


    tempp = jaccard(query)
    #("cosine ranks of query", tempp)
    print("jaccard ranks of query", tempp)

    doc_scores = sorted(tempp)
    #print(doc_scores)
    for i in doc_scores[-3:]:
        top_list.append(i)

    #print(top_list)
    '''
        for i in top_list:
        print("DocID :", temp.index(i, 1))
        print("URL : ", URL[temp.index(i, 1)])
        print("Title : ", title[temp.index(i, 1)])
        print("Content : ", content[temp.index(i, 1)])
    '''

    if len(set(top_list)) == len(top_list):
        for i in top_list:
            print("DocID :", tempp.index(i))
            print("URL : ", URL[tempp.index(i)])
            print("Title : ", title[tempp.index(i)])
            print("Content : ", content[tempp.index(i)])
    if len(top_list) - len(set(top_list)) == 1:
        if top_list[0] == top_list[1]:
            llist = find_indices(tempp, top_list[0])
            for i in range(0, 2, 1):
                print("DocID :", llist[i])
                print("URL : ", URL[llist[i]])
                print("Title : ", title[llist[i]])
                print("Content : ", content[llist[i]])
            print("DocID :", tempp.index(top_list[2]))
            print("URL : ", URL[tempp.index(top_list[2])])
            print("Title : ", title[tempp.index(top_list[2])])
            print("Content : ", content[tempp.index(top_list[2])])
        if top_list[1] == top_list[2]:
            llist = find_indices(tempp, top_list[1])
            print("DocID :", tempp.index(top_list[0]))
            print("URL : ", URL[tempp.index(top_list[0])])
            print("Title : ", title[tempp.index(top_list[0])])
            print("Content : ", content[tempp.index(top_list[0])])
            for i in range(0, 2, 1):
                print("DocID :", llist[i])
                print("URL : ", URL[llist[i]])
                print("Title : ", title[llist[i]])
                print("Content : ", content[llist[i]])

    if len(top_list) - len(set(top_list)) == 2:
        llist = find_indices(tempp, top_list[0])
        for i in range(0, 3, 1):
            print("DocID :", llist[i])
            print("URL : ", URL[llist[i]])
            print("Title : ", title[llist[i]])
            print("Content : ", content[llist[i]])


def run():
    while True:
        query()


run()
