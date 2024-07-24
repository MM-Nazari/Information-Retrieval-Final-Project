### Part02

# komak gerefte shode az geeksforgeeks
def positionalindex(object):
    positionalIndex = {}
    DocID = 0
    # iterate bar rooye hame tokenha dar file
    # i position har token ra taeen mikonad
    # object[i] meghdar ya khode token ra taeen mikonad
    for i in range(len(object)):
        # agar token dar dictionary mojood bood
        if object[i] in positionalIndex:
            # tedad tekrar dar asnad 1 adad ezafe shavad
            positionalIndex[object[i]][0] += 1
            # agar docid ghbalan sabt shode bood
            if DocID in positionalIndex[object[i]][1]:
                # be list position ha position jadid yani i ezafe shavad
                positionalIndex[object[i]][1][DocID].append(i)
            # agar docid jadid ast
            else:
                # position feli be onvan avalin position list sabt shavad
                positionalIndex[object[i]][1][DocID] = [i]
        # agar token jadid ast
        else:
            # yek list be onvane value misazim
            positionalIndex[object[i]] = []
            # 1 ra be onvan tedad tekrar ya frequency sabt mikonim
            positionalIndex[object[i]].append(1)
            # dictionary be onavan ozve dovvome list baraye sabt position ha hamrahe docid misazim
            positionalIndex[object[i]].append({})
            # positon feli yani i ra be onvan avvalin position baraye docid feli sabt mikonim
            positionalIndex[object[i]][1][DocID] = [i]
    return positionalIndex


def test2():
    text = "بارها و بارها از نخبگان و دلسوزان نظام این جمله بیان شده که قبل از وقوع انقلاب بلکه از هزاران سال پیش مردم ایران به پوشش و حجاب ارج می‌نهادند و در حال حاضر این مسئله همچون رفتار رضا شاه میشه. خوبه که داریم می رویم به سمت حجاب اختیاری و نظام مورد علاقه ما مثل رضا شاه نمی شه."
    print(positionalindex(stemmerandlemmatizer(stopword(tokenize(normalize(text))))))


test2()
