pp = pprint.PrettyPrinter(indent=2)
parsed = proc.parse_doc("Mr. Obama met Mrs. Clinton. He had spoken to her two days back.")
pp.pprint(parsed)
parsed = proc.parse_doc("Karandeep Johar, Varshaa Naganathan, Arvind Ramachandran and Dhruv Anand met to discuss the project. They had tested out Stanford CoreNLP thoroughly.")
pp.pprint(parsed)
parsed = proc.parse_doc("Is where A?")
pp.pprint(parsed)