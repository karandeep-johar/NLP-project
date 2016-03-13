# SUBJECT: Person - Who, Place - Where, Time - When, Else: - What
import os
import sys
from init import *
'''
path = os.getcwd()
corpus = sys.argv[1]
with open(path+'/'+corpus,'r') as file:
    lines = file.readlines()
    for l in lines:
        parsed = proc.parse_doc(l)
        pp.pprint(parsed)
        # Rule 1: WHAT do/does/did the SUBJECT VERB?
'''
pp = pprint.PrettyPrinter(indent=2)
parsed = proc.parse_doc("Arvind is going to Japan tomorrow. He will present his project there.")
# Idea: Get the NN_ from the sentence and get NER tag (PERSON/LOCATION/DATE)
for s in parsed['sentences']:
    pos = s['pos']
    ner = s['ner']
    tokens = s['tokens']
    nounIndices = []
    for i in range(0, len(pos)):
        tag = pos[i]
        if tag[0:2] == 'NN':
            nounIndices.append(i)
    for i in nounIndices:
        if ner[i] == 'PERSON':
            print tokens[i] + "/" + pos[i] + "/WHO?"
        elif ner[i] == 'LOCATION':
            print tokens[i] + "/" + pos[i] + "/WHERE?"
        elif ner[i] == 'DATE':
            print tokens[i] + "/" + pos[i] + "/WHEN?"
        else:
            print tokens[i] + "/" + pos[i] + "/WHAT?"

# Rule 1: WHAT do/does/did the SUBJECT VERB?
