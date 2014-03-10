import math
import json
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
frontend_data = {}
for pair in pairlist:
    school_name = pair[0]
    blob = pair[1]
    frontend_data[school_name] = {}
    print 'Top words in document ' + school_name
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:30]:
        rounded_score = round(score, 8)
        frontend_data[school_name][word] = rounded_score
        print('\tWord: {}, TF-IDF: {}'.format(word, rounded_score))

fout = open('frontend_data.json', 'w')
fout.write(json.dumps(frontend_data))
fout.close()
