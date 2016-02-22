import nltk
from nltk.corpus import wordnet as wn
import pprint
from stanford_corenlp_pywrapper import CoreNLP
proc = CoreNLP(configfile='config.ini', corenlp_jars=[
               "./stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*"])


def penn_to_wn(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


sentence = "I am going to buy some gifts"
tagged = proc.parse_doc(sentence)['sentences'][0]

synsets = []

for token in zip(tagged["tokens"], tagged["pos"]):
    wn_tag = penn_to_wn(token[1])
    if not wn_tag:
        continue
    print token, wn.synsets(token[0], pos=wn_tag)[0]

# def hypernyms(synset):
#     return synset.hypernyms()


# for x in synsets("dog"):
#     print "XXXXXXXXXXXXXXXXXXXXXXXXx"
#     print x
#     for lemma in x[0].lemmas():
#         print lemma
