from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
import bz2
from pprint import pprint

# new type of tagger
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
    ]
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')
                
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]   

# with bz2.BZ2File("../data/aij-wikiner-en-wp2.bz2") as f:
#     line_list = f.readlines()
#     # pprint(line_list[1:4])
#     train_sents = []
#     label_set =set()
#     for line in line_list[1:]:
#         words = line.split()
#         row = map(lambda word: tuple(word.split("|")), words)
#         # print row
#         train_sents.append(row)
#         for elem in row:
#             label_set.add(elem[2])
#         # label_set.add(elem[2] for elem in row)



# pprint (train_sents[0])
# pprint(sent2features(train_sents[0])[0])

# pprint(label_set)

# X_train = [sent2features(s) for s in train_sents]
# y_train = [sent2labels(s) for s in train_sents]
# trainer = pycrfsuite.Trainer(verbose=False)

# for xseq, yseq in zip(X_train, y_train):
#     trainer.append(xseq, yseq)
# trainer.set_params({
#     'c1': 1.0,   # coefficient for L1 penalty
#     'c2': 1e-3,  # coefficient for L2 penalty
#     'max_iterations': 50,  # stop earlier

#     # include transitions that are possible, but not observed
#     'feature.possible_transitions': True
# })

# print trainer.params()
# trainer.train('wiki-en-wp2.crfsuite')

tagger = pycrfsuite.Tagger()
tagger.open('wiki-en-wp2.crfsuite')


line  = "Bahrani|NNP Arabic|NNP ,|, spoken|VBN by|IN Bahrani|NNP Shia|NNP in|IN Bahrain|NNP ,|, where|WRB it|PRP exhibits|VBZ some|DT differences|NNS from|IN Bahraini|NNP Arabic|NNP .|."
# line = "Subsequently|RB ,|, the|DT Altes|NNP Museum|NNP (|-LRB- Old|NNP Museum|NNP )|-RRB- in|IN the|DT Lustgarten|NNP displaying|VBG the|DT bust|NN of|IN Queen|NNP Nefertiti|NNP ,|, A|DT 3,000-year-old|JJ smile|NN ,|, Expatica.Com|VBZ .|."
words = line.split()
example_sent = map(lambda word: tuple((word+"|KJO").split("|")), words)

pprint(example_sent)


print(' '.join(sent2tokens(example_sent)))

print("Predicted:", ' '.join(tagger.tag(sent2features(example_sent))))
print("Correct:  ", ' '.join(sent2labels(example_sent)))

# X_test = [sent2features(s) for s in test_sents]
# y_test = [sent2labels(s) for s in test_sents]