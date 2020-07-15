import sys
from ontology_maker import call_maker
from parser import parse
from sparQL import get_query


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