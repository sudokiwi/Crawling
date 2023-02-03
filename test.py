def wordcount(file1, file2):
    f = open(file1, 'r', encoding='utf-8')
    g = open(file2, 'w', encoding='utf-8')

    engine = Okt()
    data = f.read()
    all_nouns = engine.nouns((data))
    nouns = [n for n in all_nouns if len(n) > 1]

    global count, by_num

    count = Counter(nouns)
    by_num = OrderedDict(sorted(count.items(), key=lambda t: t[1], reverse=True))

    word = [i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    for w, n in zip(word, number):
        final1 = f"{w}  {n}"
        g.write(final1 + '\n')

    f.close(), g.close()


