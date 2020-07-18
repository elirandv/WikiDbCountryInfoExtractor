import sys
import os
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

		if not os.path.isfile("ontology.nt"):
			# there's a Mean Girls reference hidden here
			print("The file does not exist!")
			exit(0)

		sentence = []
		country_name = False
		# notice "ques ques ques" becomes 1 word in argv
		for i in range(2, len(sys.argv)):
			# if country_name==False or str(sys.argv[i]).title()=="born".title():
				# sentence.append(str(sys.argv[i]).title())
			# else:
				# sentence.append(str(sys.argv[i]))
			# if sentence[-1]=="Of":
				# country_name=True
			sentence = sys.argv[i].lower().split(" ")
		answer = parse(sentence)

		# check for error message, if error exit
		if isinstance(answer, str):
			print(answer)
			exit(0)
		if len(answer)==0:
			pass
		elif len(answer)==1:
			print(answer[0])
		else:
			print(answer[0], end='')
			for i in range(1,len(answer)):
				print(", "+answer[i], end='')
			print("\n")
		# print("WikiDb Country Info Extractor command done.")
	else:
		# command!="create" or command!="question"
		illegal_command()