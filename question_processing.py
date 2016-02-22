pp = pprint.PrettyPrinter(indent=2) 
parsed = proc.parse_doc("What city in China was he born?")
pp.pprint(parsed)
#print parsed)
#print parsed.keys()
if parsed[u'sentences'][0][u'tokens'][-1]=='?':
	print "Yes, it is question"
	# Is it a yes/no question:
	first_word=parsed[u'sentences'][0][u'lemmas'][0]
	if first_word=='be' or first_word=='do':
		print "Yes-No"
		# Invoke TFIDF and if score is high- Easy
		# else hard
	else:
		print "Factoid"
		#Find type of factoid # CHeck wh word
		wh_word=parsed[u'sentences'][0][u'tokens'][0]
		if wh_word.lower()=='who':
			print 'Person'
		elif wh_word.lower()=='when':
			print 'Time'
		elif wh_word.lower()=='where':
			print 'Place'
		elif wh_word.lower()=='what':
			print 'Need to find out'
			# Find headword

		else:
			print 'Default case'



	#
else:
	print "No, not a question"
#pp.pprint(parsed)
