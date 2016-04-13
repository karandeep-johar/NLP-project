from init import *
import nltk
from nltk import *
def easy_generation(sentence):
    parsed=proc3.parse_doc(sentence)
    syn_tree=parsed[u'sentences'][0][u'parse']
    parse_tree=nltk.Tree.fromstring(syn_tree)
    try:
        if parse_tree[0,0].label()=="NP" and parse_tree[0,1].label()=="VP" and (parse_tree[0,1,0,0] in set(['is', 'was','does',"has","can","could", "will", "would"])):
            word = parse_tree[0,1,0,0]
            parse_tree[0,1].remove(parse_tree[0,1,0])
            ques = word+" "+" ".join(parse_tree.leaves())
            tokens = proc3.parse_doc(ques)['sentences'][0]['tokens']
            #TODO improve capitalization
            tokens[-1] = "?"
            logger.critical("easy_generation")
            logger.critical(tokens)
            if tokens[1] in ["A", "An", "The"]:
                tokens[1] = tokens[1].lower()
            return " ".join(tokens)
            

    except Exception, e:
        return None
if __name__ == '__main__':
    logger.critical(easy_generation("A second sequel, Star Trek Beyond, is scheduled to be released on July 22, 2016."))
    with open("wiki.txt","r") as file:
        data,_ = removeHeadings(file)
        for sentence in sent_tokenize(data):
            ques = easy_generation(sentence)
            if ques:
                logger.critical(sentence)
                logger.critical(ques)
        # print sentences