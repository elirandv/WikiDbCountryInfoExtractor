import ontology_maker
import rdflib

ontology = rdflib.Graph()
ontology.parse("ontology.nt", format="nt")
wiki_prefix = "http://en.wikipedia.org"

# i use global ontology for faster run time
ontology = rdflib.Graph()

type = rdflib.URIRef("rdf:type")
country_ent = rdflib.URIRef(wiki_prefix + "/country")
person_ent = rdflib.URIRef(wiki_prefix + "/person")

# country edges
president_edge = rdflib.URIRef(wiki_prefix + "/president")
prime_minister_edge = rdflib.URIRef(wiki_prefix + "/prime_minister")
population_edge = rdflib.URIRef(wiki_prefix + "/population")
area_edge = rdflib.URIRef(wiki_prefix + "/area")
government_edge = rdflib.URIRef(wiki_prefix + "/government")
capital_edge = rdflib.URIRef(wiki_prefix + "/capital")

# person edges
birthDate_edge = rdflib.URIRef(wiki_prefix + "/birthDate")

def clean(line):
	line = str(line)
	line = line.replace("(rdflib.term.URIRef('http://en.wikipedia.org/wiki/", "")
	line = line.replace(",", "").replace("'", "").replace(")", "").replace("_", " ")
	return line
    
def q_1():
    answer = []
    q1 = "select count(distinct ?p) where { ?c <" + prime_minister_edge + "> ?p}"
    for line in list(ontology.query(q1)):
        answer.append(clean(line))
    return answer


def q_2():
	answer = []
    q2 = "select count(distinct ?c) where { ?c rdf:type <" + country_ent + "> }"
    for line in list(ontology.query(q2)):
        answer.append(clean(line))
    return answer


def q_3():
    answer = []
    q3 = "select count(distinct ?p) where { ?c <" + government_edge + "> ?g. filter contains(?g,"republic")  }"
    for line in list(ontology.query(q3)):
    answer.append(clean(line))
	return answer
    
def q_4():
	answer = []
    q4 = "select count(distinct ?p) where { ?c <" + government_edge + "> ?g. filter contains(?g,"monarchy")  }"
    for line in list(ontology.query(q4)):
    answer.append(clean(line))
	return answer
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        illegal_command()

	command = sys.argv[1]
	if command == "1":
        return q_1()
	elif command == "2":
        return q_3()
   	elif command == "3":
        return q_3()
	elif command == "4":
        return q_4()
	else:
		illegal_command()