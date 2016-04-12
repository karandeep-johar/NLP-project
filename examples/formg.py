import sys
puncTags = ['.',',','IN','#','$','CC','SYM','-LRB-','-RRB-',"''",'``',"'","`",'"',':',';','[',']','{','}','-','_','!','?','~','&','*']
def formGrammaticalSentence(sentence):
    charType=[]
    if type(sentence) is str:
        sentence=sentence.split()
    for word in sentence:
        if word.isalpha():
            charType.append('ALPH')
        elif '\'s' in word:
            charType.append('APOS')
        elif '\'' in word:
            charType.append('APO')
        elif len(set(puncTags) and set(word))>0:
            charType.append('PUNC')
    formedSent = ''
    sentence[0]=sentence[0][0].upper()+sentence[0][1:]
    for i in range(len(sentence)):
        word = sentence[i]
        if charType[i]=='PUNC' or charType[i]=='APO' or charType[i]=='APOS':
            formedSent+=word
        elif charType[i]=='ALPH':
            formedSent+=' '+word
    formedSent = formedSent.strip()
    if formedSent[-1]!='.' and formedSent[-1]!='?' and formedSent[-1]!='!':
        formedSent+='.'
    return formedSent
print formGrammaticalSentence(sys.argv[1])