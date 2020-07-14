import sys
from ontology_maker import call_maker
from parser import parse
# from sparQL import get_query


def invalid_command():
    print("Illegal command, please try 'create ontology.nt' or 'question <string>'.")
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        invalid_command()

    command = sys.argv[1]
    if command == "create":

        if sys.argv[1] != "ontology.nt":
            invalid_command()

        print("WikiDb Country Info Extractor Creating ontology...")
        call_maker()

        print("WikiDb Country Info Extractor command done.")
    elif command == "question":

        sentence = []
        for i in range(2, len(sys.argv)):
            sentence.append(sys.argv[i])

        query = parse(sentence)

        query = "select ?c where { " \
                " ?c <" + prefix + "capital> <" + prefix + "Central_African_Republic>} "

        # get_query(query, "ontology.nt")
        print("???")
        print("WikiDb Country Info Extractor command done.")
    else:
        invalid_command()
