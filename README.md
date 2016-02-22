# NLP-project

https://github.com/dasmith/stanford-corenlp-python - first block of installation lines

https://github.com/brendano/stanford_corenlp_pywrapper - first block of installation lines

keep both subfolders formed by these in the NLP-project folder

http://billchambers.me/tutorials/2015/01/14/python-nlp-cheatsheet-nltk-scikit-learn.html - Python NLP - NLTK and scikit-learn

https://github.com/piskvorky/gensim - genism

## Using NLTK

Installation: sudo pip install -U nltk

Simple Parser: https://github.com/emilmont/pyStatParser

Example code for syntax parsing: nltk_sample.py

COMPONENTS
----------
QG
-------
##Question generation - Varshaa
Input:
- Corpus
Output:
- for each sentence a plausible questioning word.


AG
--------
##Question Classification - Arvind

###Input:
- a single question string

###Output:
- type: Y/N, type of entity required as answer.
- fluency: yes or not
- hardness: estimate

##TFIDF sentence matching - Dhruv

###Input:

- Corpus
- Question String

###Output:
- scored list of sentences from the corpus which most probably can answer the question.

Common
--------
Sentence Splitting and Tokenization

## Wordnet integration - Karandeep

###Input:

- The sentence
- A word of the sentence
- Query type:
	Give homonym
	Give synonym

###Output:
appropriate query response








##Attributions
-Gensim tutorial (https://gist.github.com/clemsos/7692685, https://radimrehurek.com/gensim/tutorial.html)
-CoreNLP in python (https://github.com/dasmith/stanford-corenlp-python,https://github.com/brendano/stanford_corenlp_pywrapper)