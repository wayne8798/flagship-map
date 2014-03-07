import math
from os import listdir
from text.blob import TextBlob as tb

def tf(word, blob):
    return float(blob.words.count(word)) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1.0 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def load_docs():
    bloblist = []
    pairlist = []
    for school_name in listdir('data'):
        f = open('data/'+school_name, 'r')
        blob = tb(' '.join(f.readlines()))
        bloblist.append(blob)
        pairlist.append([school_name, blob])
        f.close()
    return [bloblist, pairlist]

bloblist, pairlist = load_docs()
for pair in pairlist:
    print 'Top words in document ' + pair[0]
    scores = {word: tfidf(word, pair[1], bloblist) for word in pair[1].words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:10]:
        print('\tWord: {}, TF-IDF: {}'.format(word, round(score, 5)))
