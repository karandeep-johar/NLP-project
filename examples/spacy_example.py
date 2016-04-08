from spacy.en import English
from spacy.attrs import *
from spacy.parts_of_speech import *
from joblib import Parallel, delayed
from pprint import pprint
import os
nlp = English()
from collections import defaultdict

#Np1 also called Np2
#Beta Leonis, also known as Denebola, is the bright tip of the tail with a magnitude of two.
def _span_to_tuple(span):
    start = span[0].idx
    end = span[-1].idx + len(span[-1])
    tag = span.root.tag_
    text = span.text
    label = span.label_
    return (start, end, tag, text, label)

def merge_spans(spans, doc):
    # This is a bit awkward atm. What we're doing here is merging the entities,
    # so that each only takes up a single token. But an entity is a Span, and
    # each Span is a view into the doc. When we merge a span, we invalidate
    # the other spans. This will get fixed --- but for now the solution
    # is to gather the information first, before merging.
    tuples = [_span_to_tuple(span) for span in spans]
    for span_tuple in tuples:
        doc.merge(*span_tuple)

def get_span_doc(doc, grand_children):
    # start = grand_children[0].idx
    # end = grand_children[-1].idx+len(grand_children[-1])
    # return str(doc)[start:end]
    i=0
    end = len(doc)
    for w in doc:
        if w==grand_children[0]:
            start = i
        elif w==grand_children[-1]:
            end = i
            break
        i+=1
    return doc[start:end+1]

def extract_is_relations(doc):
    # merge_spans(doc.ents, doc)
    # print doc
    merge_spans(doc.noun_chunks, doc)
    # print doc
    # print doc.ents
    # for w in doc:
    #     print w.ent_type_, w
    relations = []
    for entity in filter(lambda w: w.ent_type_ and w.dep_ =="nsubj" and w.head.orth_=="is" , doc):

        # isWord = entity.head
        for child in entity.head.children:
            if child.dep_=="attr":
                grand_children = [grand_child for grand_child in child.subtree]
                # print grand_children[0].idx, grand_children[0].orth_
                
                isa = get_span_doc(doc, grand_children)
                # print entity.head,(entity.head,entity,isa)
                relation = (entity.head,entity,isa)
                relations.append(relation)
            # if person.dep_ in ("pobj"):

            # print entity, entity.ent_type_, entity.head
            # for child in entity.head.children:
            #     print child
            #     for x in child.subtree:
            #         print "x",x
    return relations

def extract_also_known_as_relations(doc):
    merge_spans(doc.noun_chunks, doc)
    relations = []
    for sent in doc.sents:
        for token in sent:
            if token.orth_=="known":
                known = token
                if known.nbor(-1).orth_=="also" and known.nbor(1).orth_=="as":
                    ent1 = known.head
                    ent2 = known.nbor(1).children.next()
                    relations.append( (known,ent1, ent2))
                    break
                elif known.nbor(-1).orth_=="Also" and known.nbor(1).orth_ =="as":
                    ent2 = known.nbor(1).children.next()
                    comma = ent2.nbor(1)
                    if comma.is_punct:
                        ent1 = comma.nbor(1)
                        relations.append((known,ent1, ent2))
                    # print ent1,known, ent2
                    break  
    return relations
def extract_as_relations(doc):
    merge_spans(doc.ents, doc)
    # merge_spans(doc.noun_chunks, doc)
    relations = []
    for person in filter(lambda w: w.ent_type_ == 'PERSON', doc):
        if person.dep_ in ("pobj") and person.head.dep_ in ("prep") and person.head.orth_ == "as" and person.head.head.ent_type_=="PERSON":
            relations.append((person.head,  person.head.head,person))
    #     if money.dep_ in ('attr', 'dobj'):
    #         subject = [w for w in money.head.lefts if w.dep_ == 'nsubj']
    #         if subject:
    #             subject = subject[0]
    #             print doc
    #             relations.append((subject, money))
    #     elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
    #         print doc
    #         relations.append((money.head.head, money))
    
    return relations

def count_parent_verb_by_person(docs):
    # counts = defaultdict(defaultdict(int))
    ents = []
    for doc in docs:
        for ent in doc.ents:
            if ent.label_ in ['PERSON']  :
                ents.append(str(ent))
                # counts[ent.orth_][ent.root.head.lemma_] += 1
    return set(ents)
def dependency_labels_to_root(token):
    '''Walk up the syntactic tree, collecting the arc labels.'''
    dep_labels = []
    while token.head is not token:
        dep_labels.append((token.dep_, token))
        token = token.head
    return dep_labels

def change_called_to_known(paragraphs):
    paragraphs =  str(paragraphs).replace("also called", "also known as")
    paragraphs =  paragraphs.replace("Also called", "Also known as")
    return unicode( paragraphs)
def check_pronoun(ent):
    return not reduce(lambda a,b: a or b , map(lambda a: a.pos_=="PRON", ent))
def no_pronoun(relationship):
    relation, ent1, ent2 = relationship

    x = not reduce(lambda a,b: a or b , map(lambda a: a.pos_=="PRON", ent2))
    return x
with open("../data/set4/a3.txt","r") as f:
    paragraphs = unicode(f.read(), errors="ignore")
    # pprint(paragraphs.split(3*os.linesep))

    paragraphs = change_called_to_known(paragraphs).split("\n")

    relations=[]
    for paragraph in paragraphs:
        # for sent in doc.sents:
        relation = extract_as_relations(nlp(paragraph))
        if relation:
            relations.extend(relation)
        relation =  extract_is_relations(nlp(paragraph))
        if relation:
            relations.extend(relation)
        relation =  extract_also_known_as_relations(nlp(paragraph))
        if relation:
            relations.extend(relation)


        # for sent in doc.sents:
        #     for token in sent:
        #         print dependency_labels_to_root(token)
    # relations = filter(no_pronoun, relations)
    pprint(relations)

    # doc =nlp(u"Min Nan, part of the Min group, is widely spoken in Southeast Asia ( also known as Hokkien in the Philippines, Singapore, and Malaysia).")
    # doc = nlp(u"At magnitude 3.9 is Delta Cancri, also known as Asellus Australis. ")
    # doc = nlp(u"Rigel, which is also known as Beta Orionis, is a B-type blue supergiant that is the sixth brightest star in the night sky.")
    # doc = nlp(u"The spread of RP (also known as BBC English) through the media has caused many traditional dialects of rural England to recede, as youths adopt the traits of the prestige variety instead of traits from local dialects.")
    # doc = nlp(u"In 1991 there were 2,000 foreign learners taking China's official Chinese Proficiency Test (also known as HSK, comparable to the English Cambridge Certificate), while in 2005, the number of candidates had risen sharply to 117,660.")
    # doc =nlp(u"The Andromeda Galaxy's two main companions, M32 and M110 ( also known as NGC 221 and NGC 205, respectively) are faint elliptical galaxies that lie near it.")
    # doc = nlp(u"Also known as Acrux, Alpha Crucis is a triple star 321 light-years from Earth.")
    # doc =nlp(u"Also known as Altarf, Beta Cancri is the brightest star in Cancer at apparent magnitude 3.5 and located 290 light-years from Earth.")
    # # merge_spans(doc.ents, doc)
    # merge_spans(doc.noun_chunks, doc)

    # for token in doc:
    #     if token.orth_=="known":
    #         known = token
    #         print known
    #         if known.nbor(-1).orth_=="also" and known.nbor(1).orth_=="as":
    #             ent1 = known.head
    #             ent2 = known.nbor(1).children.next()
    #             print ent1,known, ent2
    #             break
    #         elif known.nbor(-1).orth_=="Also" and known.nbor(1).orth_ =="as":
    #             print "here"
    #             ent2 = known.nbor(1).children.next()
    #             comma = ent2.nbor(1)
    #             if comma.is_punct:
    #                 ent1 = comma.nbor(1)
    #                 print ent1,known, ent2
    #             # print ent1,known, ent2
    #             break  
    # for np in doc.noun_chunks:
    #     print np
    # print doc
        # print doc
        # break

    # doc = nlp(u"Since the ninth century, English has been written in a Latin alphabet (also called Roman alphabet).")
    # merge_spans(doc.noun_chunks, doc)
    # for token in doc:
    #     if token.orth_=="called" and token.nbor(-1).orth_=="also":
    #         print token.head
    #         # if 
    #         ent1 =[]
    #         ent2 = []
    #         for child in token.children:
    #             print child, child.ent_type_
    #             if not ent1 and child.dep_=="nsubj":
    #                 print child
    #                 ent1 = get_span_doc(doc,[grand_child for grand_child in child.subtree])

    #             elif child.dep_=="oprd":
    #                 print child
    #                 ent2 = get_span_doc(doc, [grand_child for grand_child in child.subtree])
    #             if ent1 and ent2:
    #                 print (token.orth_, ent1, ent2)
    # print count_parent_verb_by_person(docs)