import sys
from ontology_maker import call_maker
from MyParser import parse


def illegal_command():
	print("Illegal command, please try 'create' or 'question'.")
	exit(0)


if __name__ == '__main__':

	if len(sys.argv) < 3:
		illegal_command()

	command = sys.argv[1]
	if command == "create":
		if sys.argv[2] != "ontology.nt" or len(sys.argv) > 3:
			illegal_command()

		print("WikiDb Country Info Extractor Creating ontology...")
		call_maker()
		print("WikiDb Country Info Extractor command done.")
	elif command == "question":
		try:
			f = open("ontology.nt")
		except IOError:
			print("Illegal command, ontology.nt File not accessible")
		finally:
			exit(0)
		sentence = []
		for i in range(2, len(sys.argv)):
			sentence.append(sys.argv[i])
		answer = parse(sentence)

		# check for error message, if error exit
		if isinstance(answer, str):
			print(answer)
			exit(0)

		for ans in answer:
			print(ans)
		# print("WikiDb Country Info Extractor command done.")
	else:
		# command!="create" or command!="question"
		illegal_command()