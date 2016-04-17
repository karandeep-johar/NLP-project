import os
import itertools
import unicodedata
import chardet
from init import *
from collections import defaultdict
from question_processing import *
with open("pronouns.txt","r") as pro:
    pronouns = set(map(lambda x:x.strip(), pro.read().split("\n")))
# print pronouns
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

def get_span_doc(doc, grand_children, because = []):
    # start = grand_children[0].idx
    # end = grand_children[-1].idx+len(grand_children[-1])
    # return str(doc)[start:end]
    i=0
    end = len(doc)
    for w in doc:
        if w==grand_children[0]:
            start = i
        else:
            if len(because) > 0:
                if w==because:
                    end = i-1
                    break
            elif w==grand_children[-1]:
                end = i
                break
        i+=1
    return doc[start:end+1]

def extract_because_relations(doc):
    merge_spans(doc.ents, doc)
    # print doc
    relations = []
    for entity in filter(lambda w: w.dep_ == "mark" and w.orth_ == "because", doc):
        for child in entity.head.children:
            grand_children = [grand_child for grand_child in child.subtree]
            ans = get_span_doc(doc, grand_children)
            ans = ans[1:]
            #print "ANS----",ans
            break
        if entity.head.head.head.tag_ == 'VERB':
            #       try:
            for child in entity.head.head.head.children:
                grand_children = [grand_child for grand_child in child.subtree]
                ques = get_span_doc(doc, grand_children,entity)
                #print "QUES----",ques
                break
        elif entity.head.head.tag_ == 'VERB':
            for child in entity.head.head.children:
                grand_children = [grand_child for grand_child in child.subtree]
                ques = get_span_doc(doc, grand_children,entity)
                #print "QUES----",ques
                break
        else:
            try:
                for child in entity.head.head.head.children:
                    grand_children = [grand_child for grand_child in child.subtree]
                    ques = get_span_doc(doc, grand_children,entity)
                    #print "QUES----",ques
                    break
            except:
                for child in entity.head.head.children:
                    grand_children = [grand_child for grand_child in child.subtree]
                    ques = get_span_doc(doc, grand_children,entity)
                    #print "QUES----",ques
                    break
        relation = (entity,ques,ans)
        relations.append(relation)
    return relations


def extract_is_relations(doc):
    relations = []
    try:
        merge_spans(doc.ents, doc)
        # print doc
        merge_spans(doc.noun_chunks, doc)
        for entity in filter(lambda w: w.ent_type_ and w.dep_ =="nsubj" and w.head.orth_ in ("is","was","been","has","have","had") , doc):
        # isWord = entity.head
        # print "entity", entity
            for child in entity.head.children:
                # print child, child.dep_
                if child.dep_ in ("attr","dobj"):
                    grand_children = [grand_child for grand_child in child.subtree]
                    # print grand_children[0].idx, grand_children[0].orth_
                    # print "69", child, grand_children
                    isa = get_span_doc(doc, grand_children)
                    # print entity.head,(entity.head,entity,isa)
                    relation = (entity.head,entity,isa)
                    # print "XXXXXXXXXXXXXXXX"
                    # print entity.head.orth_,entity.head.lemma_
                    relations.append(relation)

    except Exception, e:
        return relations
    
    return relations

def extract_also_known_as_relations(doc):
    merge_spans(doc.noun_chunks, doc)
    relations = []
    try:
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
    except Exception, e:
        return relations
    return relations

def extract_as_relations(doc):
    merge_spans(doc.ents, doc)
    # merge_spans(doc.noun_chunks, doc)
    relations = []
    try:
        for person in filter(lambda w: w.ent_type_ == 'PERSON', doc):
               if person.dep_ in ("pobj") and person.head.dep_ in ("prep") and person.head.orth_ == "as" and person.head.head.ent_type_=="PERSON":
                   relations.append((person.head,  person.head.head,person))
    except Exception, e:
        return relations
   
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

def count_parent_verb_by_person(doc, ents):
    # counts = defaultdict(defaultdict(int))
    
    # ents = []
    merge_spans(doc.ents, doc)
    # merge_spans(doc.noun_chunks, doc)
    for ent in doc.ents:
        if ent.label_:
            s = ent.orth_.replace("'s","")
            s = s.replace("s'","")
            ents[s].append(ent.label_)
        # if ent.label_ in ['PERSON']:
        #     ents.append(ent)
            # counts[ent.orth_][ent.root.head.lemma_] += 1
    return ents
def dependency_labels_to_root(token):
    '''Walk up the syntactic tree, collecting the arc labels.'''
    dep_labels = []
    while token.head is not token:
        dep_labels.append((token.dep_, token))
        token = token.head
    return dep_labels

def change_called_to_known(paragraphs):
    paragraphs =  paragraphs.replace("also called", "also known as")
    paragraphs =  paragraphs.replace("Also called", "Also known as")
    return unicode( paragraphs)

def check_pronoun(ent):
    # print "check_pronoun184", ent, not reduce(lambda a,b: a or b , map(lambda a: str(a.lower()) in pronouns, ent))
    return not reduce(lambda a,b: a or b , map(lambda a: str(a.lower()) in pronouns, ent))

def extract_entities_relations(paragraph):
    
    # curlinkname = f.read()
    # code = chardet.detect(curlinkname)
    # paragraphs = curlinkname.decode(code['encoding'], errors="ignore")
    # paragraphs = unicodedata.normalize('NFKD', paragraphs).encode('ascii','ignore')

    # # print type(paragraphs)
    # # pprint(paragraphs.split(3*os.linesep))

    # paragraphs_unicode = change_called_to_known(paragraphs)
    # paragraph,_ = removeHeadings(f)
    paragraphs_unicode = change_called_to_known(paragraph)
    paragraphs =  paragraphs_unicode.split("\n")

    relations=[]
    because_relations = []
    ents = defaultdict(list)
    for paragraph in paragraphs:
        # for sent in doc.sents:
        for sent in nlp(paragraph).sents:
            sent = sent.orth_
            because_relations.extend(extract_because_relations(nlp(sent)))
            relations.extend(extract_as_relations(nlp(sent)))
            relations.extend(extract_is_relations(nlp(sent)))
            relations.extend(extract_also_known_as_relations(nlp(sent)))
        ents = count_parent_verb_by_person(nlp(paragraph), ents)
        p = nlp(paragraph)
        merge_spans(p.noun_chunks, p)
        # for sent in doc.sents:
        #     for token in sent:
        #         print dependency_labels_to_root(token)
    # for relation in relations:
    #     print relation[1].lemma_, relation[1].lemma_.lower() in pronouns
    
    relations = filter(lambda relation:check_pronoun( relation[1].lemma_.lower().split()) and check_pronoun([relation[2].lemma_.lower().split()[0]]), relations)
    because_relations = filter(lambda relation:check_pronoun( relation[1].lemma_.lower().split()), because_relations)
    relations.extend(because_relations)
    # for relation in relations:
    #     print relation, relation[1].ent_type_
    # pprint(relations)
    # entities_product = []
    # for i in itertools.product(ents,ents):
    #     entities_product.append((i[0].similarity(i[1]), i[0], i[1]))
    # pprint(entities_product)

    # pprint(dict(ents))
    # for x in ents:
    #     if u"PERSON" in ents[x]:
    #         print x

    return dict(ents), relations

def format_type(date):
    date_str = str(date)
    for x in puncTags:
        date_str = date_str.replace(x, " ")
    date_list = date_str.split()
    hash_kjo = map(lambda x: str(x.isalpha())+" "+str(x.isdigit()) +" "+ str(x.isalnum()), date_list)
    
    return str(hash_kjo)

def make_hard_questions(question,  entities, relations):
    questions =[]
    for relation in relations:
        relation = [str(relation[0].orth_),str( relation[1].orth_), str(relation[2].orth_)]
        if relation[0].lower() == "known":
            if relation[1].lower() in question.lower() and relation[2].lower() in question.lower():
                continue
            else:
                if relation[1] in question:
                    questions.append(question.replace(relation[1], relation[2]))
                if relation[2] in question:
                    questions.append(question.replace(relation[2], relation[1]))
        if relation[0].lower() == "as":
            q  = nlp(unicode(question))
            if "play" in q[:].lemma_:
                continue
            if relation[1].lower() in question.lower() and relation[2].lower() in question.lower():
                continue
            else:
                if relation[2] in question:
                    questions.append(question.replace(relation[2], relation[1]+"'s character"))
    return questions
def makeHardBooleanQuestions(question,entities,relations):
    questions =[]
    qp =  Question_parser(question)
    if qp.qtype == "BOOLEAN":
        questions.extend(change_dates(question, entities, relations))
        questions.extend(change_names(question, entities))
    return questions
    
def change_names(question, entities):
    q = nlp(unicode(question))
    people = {k:"PEOPLE"  for k in entities if set(entities[k]) == set(["PERSON"])}
    # print "PEOPLE"
    # print people
    merge_spans(q.ents, q)
    ents = []
    for ent in q.ents:
        if ent.label_:
            ents.append(str(ent.orth_))
    questions = []
    found = ""
    for ent in ents:
        if not found:
            for new_person in sorted(people, key=len, reverse=True):
                # print "241", str(new_person), question
                if str(new_person) == ent:
                    found = str(new_person)
                    break
    if found:
        for new_person in sorted(people, key=len, reverse=True):
            if new_person not in question and len(new_person.split()) == len(found.split()) and new_person.isalpha() and found.isalpha():
                questions.append(question.replace(found, new_person))
    # for person in q.ents:
    #     print "240 person",  person.orth_
    #     for new_person in people:
    #         if new_person == person.orth_ or person.orth_ not in people:
    #             continue
    #         print "new_person", new_person
    #         questions.append(question[:person.idx] + str(new_person) +" "+ question[person.idx+len(str(person)):] )
    return questions
def change_dates(question, entities, relations):
    questions = []
    dates = defaultdict(list)
    for entity in entities:
        if "DATE" in entities[entity]:
            if format_type(entities[entity]):
                dates[format_type(entity)].append( entity   )
    q = nlp(unicode(question))
    merge_spans(q.ents, q)
    for date in filter(lambda x: x.ent_type_=="DATE", q):
        fd = format_type(date)
        if fd:
            for possible_date in dates[fd]:
                if str(possible_date) not in question : #and  nlp(unicode(str(possible_date))).similarity(nlp(unicode(str(date))))>0.85:
                    questions.append(question[:date.idx]+str(possible_date) + " "+ question[date.idx+len(str(date)):])
    return questions

def check_who_what(rel, entities):
    try:
        ner_list = entities[rel.encode('utf-8')]
        ner = max(set(ner_list), key=ner_list.count)
        if ner == 'PERSON' or ner == 'ORG':
            return "Who"
        else:
            return "What"
    except:
        return None

def make_because_question(rel):
    proc = init.proc2
    parsed = proc.parse_doc(rel[1])
    pos = parsed[u'sentences'][0][u'pos']
    q = str(rel[1])
    q = q.split()
    if pos[1][0:2] == 'VB':
        verb_root = parsed[u'sentences'][0][u'lemmas'][1]
        if verb_root == 'be':
            q_word = "Why " + parsed[u'sentences'][0][u'tokens'][1] + " "
            prefix = str(q_word)+str(q[0])+str(" ")
        elif verb_root == 'have' and pos[2][0:2] == 'VB':
            q_word = "Why " + parsed[u'sentences'][0][u'tokens'][1] + " "
            prefix = str(q_word)+str(q[0])+str(" ")
        elif pos[1] == 'VBD' or pos[1] == 'VBN':
            q_word = "Why did "
            prefix = str(q_word)+str(q[0])+str(" ")+str(verb_root)+str(" ")
        elif pos[1] == 'VBP' or pos[1] == 'VBG' or pos[1] == 'VBZ':
            q_word = "Why does "
            prefix = str(q_word)+str(q[0])+str(" ")+str(verb_root)+str(" ")
        if not str(q[-1]).isalnum():
            q.remove(q[-1])
        q = ' '.join(q[2:])
        q = prefix+q+"?"
        return q
    else:
        return None

def make_questions_relations(relations,entities):
    questions = []
    for relation in relations:
        relation = [str(relation[0].orth_),str( relation[1].orth_), str(relation[2].orth_)]
        relation[0] = relation[0][0].upper() +relation[0][1:]
        start = relation[1].split(" ",1)
        # print "290", start, relation[1]
        if str(start[0]).lower() in stopwords:
            start[0] = start[0].lower()
        relation[1] = " ".join(start)
        if relation[0].lower() in ("is", "was"):
            questions.append(" ".join(relation)+"?")
        elif relation[0].lower() in  ["had","has"]:
            questions.append("Did "+ relation[1] + " have " + relation[2] +"?")
        elif relation[0].lower() == "been":
            questions.append("Has " + relation[1] + " been " + relation[2] +"?")
        elif relation[0].lower() == "as":
            #make harder question this
            questions.append("Which character was played by "+ relation[1] + " in the film ?")
            questions.append("Did "+ relation[1] + " play the character of "+ relation[2] +" in the film ?")
            questions.append("Who plays "+ relation[2] +" in the film ?")
        elif relation[0].lower() == "known":
            #make harder questions using this
            questions.append("Is "+ relation[1] +" also known as "+ relation[2]+" ?")
            questions.append("Is "+ relation[1] +" also called "+ relation[2]+" ?")
            questions.append("What is another name for "+ relation[1]+" ?")
            questions.append("What is another name for "+ relation[2]+" ?")
        elif relation[0].lower() == "because":
            q = make_because_question(relation)
            if not q is None:
                questions.append(q)
        if relation[0].lower() == "is":
            q_word = check_who_what(relation[1], entities)
            if not q_word is None:
                questions.append(q_word+" is "+ relation[1]+" ?")
    return questions
#TODO remove punctuation errors, look at why 2014-15 becomes 201415 and make tougher questions?
# choose one of who/what/where etc.
# make questions by replacing people, dates
if __name__ == '__main__':
    with open("wiki.txt","r") as f:
        paragraph,_,_ = removeHeadings(f)
        x = extract_entities_relations(paragraph)
        pprint.pprint(x[1])
        pprint.pprint(make_questions_relations(x[1],x[0]))
        # pprint.pprint(x[1])
        # pprint.pprint(make_questions_relations(x[1]))

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