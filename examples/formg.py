import sys
puncTags = ['.',',','IN','#','$','CC','SYM','-LRB-','-RRB-',"''",'``',"'","`",'"',':',';','[',']','{','}','-','_','!','?','~','&','*']
def formGrammaticalSentence(sentence):
    charType=[]
    if type(sentence) is str:
        sentence=sentence.split()
    print sentence[-1]
    if sentence[-1]=='?':
        if sentence[1]==',':
            del sentence[1]
        if sentence[-2]=='and' or sentence[-2]==',':
            del sentence[-2]
    for word in sentence:
        if word.isalpha():
            charType.append('ALPH')
        elif "'s" in word:
            charType.append('APOS')
        elif "'" in word:
            charType.append('APO')
        elif word in set(puncTags):
            charType.append('PUNC')
        else:
            charType.append('OTHER')
    formedSent = ''
    sentence[0]=sentence[0][0].upper()+sentence[0][1:]
    for i in range(len(sentence)):
        word = sentence[i]
        word=word.replace("-LRB-","(")
        word=word.replace("-RRB-",")")
        word=word.replace("``",'"')
        word=word.replace("''",'"')
        if charType[i]=='PUNC' or charType[i]=='APO' or charType[i]=='APOS':
            formedSent+=word
        elif charType[i]=='ALPH':
            formedSent+=' '+word
        elif charType[i]=='OTHER':
            formedSent+=' '+word

    formedSent = formedSent.strip()
    if formedSent[-1]!='.' and formedSent[-1]!='?' and formedSent[-1]!='!':
        formedSent+='.'
    return formedSent
print formGrammaticalSentence(sys.argv[1])