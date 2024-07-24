### Part03

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
#sentences = []


def contenturltitle(object):
    tokenizer = Tokenizer()
    for DocID in object.keys():
        title.append(object[DocID]["title"])
        content.append(object[DocID]["content"])
        URL.append(object[DocID]["url"])
        #sentences.append(tokenizer.tokenize_sentences(content[int(DocID)]))


contenturltitle(readjson())
positionalindex = positionalindex(readjson())


def query():
    query = stemmerandlemmatizer(stopword(tokenize(normalize(input("لطفا پرسمان را وارد کنید: ")))))
    phrase = []
    docs = []
    docsor = []
    docsphrase = []
    sorteddocs = []
    sorteddocsor = []
    countsand = []
    countsor = []
    checkbit = 0
    thereis1 = 0
    thereis2 = 0
    for word in range(len(query)):
        if query[word] == "!":
            notword = query[word + 1]
            index1 = word
            thereis1 = 1

        if query[word] == '"' and checkbit == 1:
            index3 = word

        if query[word] == '"' and checkbit != 1:
            checkbit = 1
            check = word + 1
            while query[check] != '"':
                phrase.append(query[check])
                check += 1
            index2 = word
            thereis2 = 1

    if thereis1 == 1 and thereis2 == 1:
        if index1 > index3:
            query.pop(index1)
            query.pop(index2)
            query.pop(index3 - 1)
        else:
            query.pop(index1)
            query.pop(index2 - 1)
            query.pop(index3 - 2)

    if thereis1 == 1 and thereis2 == 0:
        query.pop(index1)

    if thereis1 == 0 and thereis2 == 1:
        query.pop(index2)
        query.pop(index3 - 1)

    if query[0] in positionalindex.keys():
        for i in positionalindex[query[0]][1].keys():
            if i not in docs:
                docs.append(i)
            if i not in docsor:
                docsor.append(i)
    else:
        k = 1
        while query[k] not in positionalindex.keys():
            k += 1
        for i in positionalindex[query[k]][1].keys():
            if i not in docs:
                docs.append(i)
            if i not in docsor:
                docsor.append(i)

    for word in range(len(query)):
        if query[word] in positionalindex.keys():
            docsb = []
            for i in positionalindex[query[word]][1].keys():
                if i not in docsb:
                    docsb.append(i)
            if thereis1 == 0 and thereis2 == 0:
                docs = sorted(set(docs).intersection(docsb))
            if thereis1 == 1:
                if query[word] == notword:
                    docs = sorted(set(docs) - set(docsb))
                else:
                    continue
            if thereis2 == 1:
                if query[word] != phrase[0] and query[word] != phrase[1]:
                    docs = sorted(set(docs).intersection(docsb))
                if query[word] == phrase[0] and query[word] != phrase[1]:
                    docs = sorted(set(docs).intersection(docsb))
                    docsphrase = docsb.copy()
                if query[word] != phrase[0] and query[word] == phrase[1]:
                    docsphrase = sorted(set(docsphrase).intersection(docsb))
                    for i in docsphrase:
                        flag = 0
                        for j in positionalindex[phrase[0]][1][i]:
                            for k in positionalindex[phrase[1]][1][i]:
                                if int(j) == int(k) - 1:
                                    flag = 1
                        if flag != 1:
                            docsphrase.remove(i)
                    docs = sorted(set(docs).intersection(docsphrase))
            docsor = sorted(set(docsor).union(docsb))

        else:
            continue

    flagdocs = 0
    if len(docs) > 0:
        for i in range(len(docs)):
            countsand.append(0)
            for j in query:
                if j in positionalindex.keys():
                    if thereis1 == 1 and j == notword:
                        continue
                    else:
                        try:
                            countsand[i] += len(positionalindex[j][1][docs[i]])
                        except KeyError:
                            continue
                else:
                    continue
        sorteddocs = [val for (_, val) in sorted(zip(countsand, docs), key=lambda x: x[0])]
        flagdocs = 1
    if len(docs) < 5:
        for i in range(len(docsor)):
            countsor.append(0)
            for j in range(len(query)):
                if query[j] in positionalindex.keys() and docsor[i] in positionalindex[query[j]][1].keys():
                    countsor[i] += len(positionalindex[query[j]][1][docsor[i]])
                else:
                    continue
        sorteddocsor = [val for (_, val) in sorted(zip(countsor, docsor), key=lambda x: x[0])]

    if flagdocs == 1 and len(sorteddocs) >= 5:
        for i in range(len(sorteddocs) - 1, len(sorteddocs) - 6, -1):
            print("DocID :", sorteddocs[i])
            print("URL : ", URL[int(sorteddocs[i])])
            print("Title : ", title[int(sorteddocs[i])])
            print("Content : ", content[int(sorteddocs[i])])


    if len(sorteddocs) < 5:
        difference = len(sorteddocsor) - len(sorteddocs)
        for i in range(len(sorteddocs) - 1, -1, -1):
            print("DocID :", sorteddocs[i])
            print("URL : ", URL[int(sorteddocs[i])])
            print("Title : ", title[int(sorteddocs[i])])
            print("Content : ", content[int(sorteddocs[i])])

        if difference > 0:
            for i in range(len(sorteddocsor) - 1, len(sorteddocsor) - (5 - len(sorteddocs)) - 1, -1):
                print("DocID :", sorteddocsor[i])
                print("URL : ", URL[int(sorteddocsor[i])])
                print("Title : ", title[int(sorteddocsor[i])])
                print("Content : ", content[int(sorteddocsor[i])])


    print("DocID haye AND : ", docs)
    print("DocID haye OR : ", docsor)
    print("Tedad tekrar kalamat dar DocID haye AND : ", countsand)
    print("DocID haye AND sort shode : ", sorteddocs)
    print("Tedad tekrar kalamat dar DocID haye OR : ", countsor)
    print("DocID haye OR sort shode : ", sorteddocsor)


def run():
    while True:
        query()


run()
