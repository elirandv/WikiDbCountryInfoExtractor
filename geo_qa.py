import sys
from ontology_maker import call_maker
from parser import parse

if __name__ == '__main__':
    wiki_prefix = "http://en.wikipedia.org"
    if len(sys.argv)==1:
        print("Illegal command, please try 'create' or 'question'.")
        exit(0)
    command=sys.argv[1]
    if (command=="create"):  
        print("WikiDb Country Info Extractor Createing ontology...")
        make_ontology("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")
        print("Ontology.nt was added")
        print("WikiDb Country Info Extractor command done.")
    elif command=="question":
            
        get_query(query, "ontology.nt")
        print("???")
        print("WikiDb Country Info Extractor command done.")
    else:
        # (command!="create" or command!="question"):
        print("Illegal command, please try 'create' or 'question'.")


def illegal_command():
	print("Illegal command, please try 'create' or 'question'.")
	exit(0)


if __name__ == '__main__':

	if len(sys.argv) == 1:
		illegal_command()

	command = sys.argv[1]
	if command == "create":
		print("WikiDb Country Info Extractor Creating ontology...")
		call_maker()
		print("WikiDb Country Info Extractor command done.")
	elif command == "question":
		sentence = []
		for i in range(2, len(sys.argv)):
			sentence.append(word)

		answer = parse(sentence)
		print(answer)
		print("WikiDb Country Info Extractor command done.")
	else:
		# command!="create" or command!="question"
		illegal_command()