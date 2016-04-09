
from stanford_corenlp_pywrapper import CoreNLP
import os,sys
from collections import Counter
# dir = "."
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*')
proc2 = CoreNLP(configfile='../src/simple.ini', corenlp_jars=[filename])

def removeHeadings(article):
    data = article.read()
    data = str(unicode(data, errors='ignore'))
    splitData = data.split('\n')
    splitData = [para for para in splitData if para]
    splitData[0] = splitData[0].split('(')[0]
    # print splitData[1]
    # print splitData[2]
    title = ' '.join(splitData[0].split('_')).strip()
    i=0
    for i in range(1,len(splitData)):
        para = splitData[i]
        if len(para.split())<=4:
            break
    pronounCount=Counter()
    for para in splitData[1:i]:
        pronounCount['It'] += para.count('. It')+para.count('. They')+para.count('. Their')
        pronounCount['He'] += para.count('. He')+para.count('. His')
        pronounCount['She'] += para.count('. She')+para.count('. Her')
        pronounCount['It'] += para.count('. It')
    if i>0 and sum(pronounCount.values())>0:
        most_common,_ = pronounCount.most_common(1)[0]
        for j in range(1,i):
            if most_common=='It':
                splitData[j] = splitData[j].replace('. It','. '+title)
                splitData[j] = splitData[j].replace('. They','. '+title)
                splitData[j] = splitData[j].replace('. Their','. '+title+'\'s')
            if most_common=='He':
                splitData[j] = splitData[j].replace('. He','. '+title)
                splitData[j] = splitData[j].replace('. His','. '+title+'\'s')
            if most_common=='She':
                splitData[j] = splitData[j].replace('. She','. '+title)
                splitData[j] = splitData[j].replace('. Her','. '+title+'\'s')
    finalParas = []
    for i in range(1,len(splitData)):
        para = splitData[i]
        if len(para.split())>4:
            finalParas.append(para)
    data = '.\n '.join(finalParas)
    titleLemmas = [w.lower() for w in proc2.parse_doc(title)['sentences'][0]['lemmas']]
    titleLemmasSet = set(titleLemmas)
    for tL in titleLemmas:
        parts = tL.split('_')
        if len(parts)>1:
            titleLemmasSet|=set(parts)
    return data,titleLemmasSet

print removeHeadings(open(sys.argv[1]))[0]