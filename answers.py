import sys
import os
import ontology_maker
import rdflib
from query import *

ontology = rdflib.Graph()
if os.path.isfile("ontology.nt"):
	ontology.parse("ontology.nt", format="nt")

wiki_prefix = "https://en.wikipedia.org"

type = "rdf:type"
country_ent = wiki_prefix + "/country"
person_ent = wiki_prefix + "/person"

# country edges
president_edge = wiki_prefix + "/president"
prime_minister_edge = wiki_prefix + "/prime_minister"
population_edge = wiki_prefix + "/population"
area_edge = wiki_prefix + "/area"
government_edge = wiki_prefix + "/government"
capital_edge = wiki_prefix + "/capital"

# person edges
birthDate_edge = wiki_prefix + "/birthDate"


def illegal_command():
    print("problen/n")
    exit(0)


def clean(line):
    line = str(line)
    line = line.rsplit('/', 1)[-1]
    line = line.replace("(rdflib.term.URIRef('http://en.wikipedia.org/wiki/", "")
    line = line.replace(",", "").replace("'", "").replace(")", "").replace("_", " ")
    return line


def q(i):
    answer = []
    if i == 1:
        print("\n### PM count?\n")
        q = "select (count(distinct ?p) as ?n) where { ?c <" + prime_minister_edge + "> ?p }"
    elif i == 2:
        print("\n### Countries count?\n")
        q = "select (count(distinct ?c) as ?n) where { ?c <rdf:type> <" + country_ent + "> }"
    elif i == 3:
        print("\n### Republics count?\n")
        q = "select (count(distinct ?c) as ?n) where { ?c <" + government_edge + "> ?g. filter (contains(str(?g),'republic'))  }"
    elif i == 4:
        print("\n### Monarchy count?\n")
        q = "select (count(distinct ?c) as ?n) where { ?c <" + government_edge + "> ?g. filter (contains(str(?g),'monarchy'))  }"
    elif i == 5:
        print("\n### PM list?\n")
        q = "select distinct ?p where { ?c <" + prime_minister_edge + "> ?p }"
    elif i == 6:
        print("\n### Republics list?\n")
        q = "select distinct ?c where { ?c <" + government_edge + "> ?g. filter (contains(str(?g),'republic'))  }"

    if i<5:
        for line in ontology.query(q):
            answer.append(line.n)
        return answer
    else:
        for line in list(ontology.query(q)):
            answer.append(clean(line))
        return answer
        
if __name__ == '__main__':

    print("activate: python geo_qa.py create ontology.nt\n")
    os.system("python geo_qa.py create ontology.nt")

    print("question 1: who is the president of Italy?\n")
    os.system("python geo_qa.py question who is the president of Italy?")
    print("\nquestion 2: who is the prime minister of United Kingdom?\n")
    os.system("python geo_qa.py question who is the prime minister of United Kingdom?")
    print("\nquestion 3: what is the population of Democratic Republic of the Congo?\n")
    os.system("python geo_qa.py question what is the population of Democratic Republic of the Congo?")
    print("\nquestion 4 what is the area of Fiji?:\n")
    os.system("python geo_qa.py question what is the area of Fiji?")
    print("\nquestion 5 What is the government of Eswatini?:\n")
    os.system("python geo_qa.py question What is the government of Eswatini?")
    print("\nquestion 6 what is the capital of Canada?:\n")
    os.system("python geo_qa.py question what is the capital of Canada?")
    print("\nquestion 7 when was the president of South Korea born?:\n")
    os.system("python geo_qa.py question when was the president of South Korea born?")
    print("\nquestion 8 when was the prime minister of New Zealand born?:\n")
    os.system("python geo_qa.py question when was the prime minister of New Zealand born?")
    print("\nquestion 9: who is Donald Trump?\n")
    os.system("python geo_qa.py question who is Donald Trump?")
    print("\nquestion 10: who is kyriakos mitsotakis?\n")
    os.system("python geo_qa.py question who is Kyriakos Mitsotakis?")

    print("\nquestion 1: Who is the pResident of itAly?\n")
    os.system("python geo_qa.py question Who is the pResident of itAly?")

    print("\nquestion 3: what is the PopulaTion of Democratic republic Of the CoNgo?\n")
    os.system("python geo_qa.py question what is the population of Democratic Republic of the Congo?")


    print("\nNull return question 11: who is the president of United States Virgin Islands?\n")
    os.system("python geo_qa.py question who is the president of United States Virgin Islands?")  
    
    print("\nNull return question 12: what is the capital of Monaco?\n")
    os.system("python geo_qa.py question what is the capital of Monaco?")
    print("\n")

    for i in range(1, 7):
        answer = q(i)
        # check for error message, if error exit
        if isinstance(answer, str):
            illegal_command()
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
    print("All answers WikiDb Country Info Extractor command done.")
