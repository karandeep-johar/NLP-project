import nltk
from nltk.corpus import wordnet as wn
from init import *


def penn_to_wn(tag):
    if tag.startswith('N'):
            return wn.NOUN
    # elif tag.startswith('J'):
    #     return wn.ADJ
    # elif tag.startswith('R'):
    #     return wn.ADV
    # elif tag.startswith('V'):
    #     return wn.VERB
    return None


sentence = "dog"
tagged = proc.parse_doc(sentence)['sentences'][0]
print tagged
synsets = []

for token in zip(tagged["tokens"], tagged["pos"]):
    wn_tag = penn_to_wn(token[1])
    if not wn_tag:
        continue
    print token, wn.synsets(token[0], pos=wn_tag)[0]
    synsets.append(wn.synsets(token[0], pos=wn_tag)[0])


def hypernyms(synset):
    return synset.hypernyms()
for x in synsets:
    print hypernyms(x)
    if len(hypernyms(x)) > 0:
        print "hyponym", hypernyms(x)[0].hypernyms()[0].hyponyms()[0]


'''Synonym generator using NLTK WordNet Interface: http://www.nltk.org/howto/wordnet.html
    'ss': synset
    'hyp': hyponym
    'sim': similar to
    'ant': antonym
    'also' also see

'''


def get_all_synsets(word, pos=None):
    for ss in wn.synsets(word):
        for lemma in ss.lemma_names():
            yield (lemma, ss.name())


def get_all_hyponyms(word, pos=None):
    for ss in wn.synsets(word, pos=pos):
            for hyp in ss.hyponyms():
                for lemma in hyp.lemma_names():
                    yield (lemma, hyp.name())


def get_all_similar_tos(word, pos=None):
    for ss in wn.synsets(word):
            for sim in ss.similar_tos():
                for lemma in sim.lemma_names():
                    yield (lemma, sim.name())


def get_all_antonyms(word, pos=None):
    for ss in wn.synsets(word, pos=None):
        for sslema in ss.lemmas():
            for antlemma in sslema.antonyms():
                    yield (antlemma.name(), antlemma.synset().name())


def get_all_also_sees(word, pos=None):
        for ss in wn.synsets(word):
            for also in ss.also_sees():
                for lemma in also.lemma_names():
                    yield (lemma, also.name())


def get_all_synonyms(word, pos=None):
    for x in get_all_synsets(word, pos):
        yield (x[0], x[1], 'ss')
    for x in get_all_hyponyms(word, pos):
        yield (x[0], x[1], 'hyp')
    for x in get_all_similar_tos(word, pos):
        yield (x[0], x[1], 'sim')
    for x in get_all_antonyms(word, pos):
        yield (x[0], x[1], 'ant')
    for x in get_all_also_sees(word, pos):
        yield (x[0], x[1], 'also')

for x in get_all_synonyms('love'):
    print x