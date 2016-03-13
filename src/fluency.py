#! /usr/bin/env python
# -*- coding: utf8 -*-
#
# Link Grammar example usage
#

# sudo apt-get install python-dev
# ./configure --enable-python-bindings --disable-java-bindings
# make
# sudo make install
# sudo ldconfig

# from init import *
import locale

from linkgrammar import Sentence, ParseOptions, Dictionary
# from linkgrammar import _clinkgrammar as clg

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

po = ParseOptions()


# English is the default language
# sent = Sentence("Mary seeing Bob good.", Dictionary(), po)
def checkSentence(sentence):
    sent = Sentence(sentence,Dictionary(),po)
    linkages = sent.parse()
    if min(sent.num_linkages_found(), sent.num_valid_linkages()) >0:
        return True
    return False

# print checkSentence("Mary seeing Bob good.")