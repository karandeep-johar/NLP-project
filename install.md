pip install -U pytest
https://github.com/dasmith/stanford-corenlp-python - first block of installation lines

https://github.com/brendano/stanford_corenlp_pywrapper - first block of installation lines

keep both subfolders formed by these in the NLP-project folder

http://billchambers.me/tutorials/2015/01/14/python-nlp-cheatsheet-nltk-scikit-learn.html - Python NLP - NLTK and scikit-learn

https://github.com/piskvorky/gensim - genism

## Using NLTK

Installation: sudo pip install -U nltk

Simple Parser: https://github.com/emilmont/pyStatParser

Example code for syntax parsing: nltk_sample.py


## LinkGrammar

#install python-dev
sudo apt-get install python2.7-dev

wget http://www.abisource.com/downloads/link-grammar/5.3.4/link-grammar-5.3.4.tar.gz

tar -zxvf link-grammar-5.3.4.tar.gz

cd link-grammar-5.3.4/

./configure --enable-python-bindings

make

sudo make install

ldconfig

##supersense

sudo apt-get install python-dev
