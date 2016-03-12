import nltk
grammar1 = nltk.parse_cfg("""
S -> NP VP
VP -> V NP
V -> "saw"
NP -> "Mary" | "Bob"
""")
sent = "Mary saw Bob saw".split()
rd_parser = nltk.RecursiveDescentParser(grammar1)
if len(rd_parser.nbest_parse(sent)) > 0:
    for tree in rd_parser.nbest_parse(sent):
         print(tree)
else:
    print("Error: %s is not a match for the grammar rule %s") % (sent, grammar1)
