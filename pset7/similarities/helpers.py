from nltk.tokenize import sent_tokenize,word_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    la = a.split("\n")
    lb = b.split("\n")

    lc = []

    # if a.rstrip("\n") not in la:
    #     la.append(a.rstrip("\n"))

    # for line in b:
    #     lb.append(line.rstrip("\n"))
    for i in range(len(la)):
        if la[i] in lb and la[i] not in lc:
            lc.append(la[i])
    # TODO
    return lc


def sentences(a, b):
    """Return sentences in both a and b"""
    la = sent_tokenize(a)
    lb = sent_tokenize(b)
    # lb = nltk.tokenize.sent_tokenize(b,language = 'engilsh')
    lc = []

    for i in range(len(la)):
        if la[i] in lb and la[i] not in lc:
            lc.append(la[i])
    # TODO
    return lc




def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    la = []
    lb = []
    for i in range(len(a)-n+1) :
        la.append(a[i:(i+n)])
    for i in range(len(b)-n+1) :
        lb.append(b[i:(i+n)])
    print(f"{la}")


    lc = []
    for i in range(len(la)):
        if la[i] in lb and la[i] not in lc:
            lc.append(la[i])
    # TODO
    return lc
