import ontology_maker
import rdflib

ontology = rdflib.Graph()
ontology.parse("ontology.nt", format="nt")
wiki_prefix = "http://en.wikipedia.org"

# country edges
president_edge = wiki_prefix + "/president"
prime_minister_edge = wiki_prefix + "/prime_minister"
population_edge = wiki_prefix + "/population"
area_edge = wiki_prefix + "/area"
government_edge = wiki_prefix + "/government"
capital_edge = wiki_prefix + "/capital"

# person edges
birthDate_edge = wiki_prefix + "/birthDate"


def clean(line):
	line = str(line)
	line = line.replace("(rdflib.term.URIRef('http://en.wikipedia.org/wiki/", "")
	line = line.replace("'", "").replace(")", "").replace("_", " ")
	if line.endswith(","):
		line = line[:-1]
	return line


def clean_date(line):
	line = str(line)
	line = line.replace("(rdflib.term.Literal('", "")
	line = line.replace("', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#date')),)", "")
	line = line.replace(",", "").replace("'", "").replace(")", "").replace("_", " ")
	return line


def who_is_pres(country):
	answer = []
	q = "select ?p where { <" + wiki_prefix + "/wiki/" + country + "> <" + president_edge + "> ?p}"
	for line in list(ontology.query(q)):
		answer.append(clean(line))
	return answer


def who_is_pm(country):
	answer = []
	q = "select ?p where { <" + wiki_prefix + "/wiki/" + country + "> <" + prime_minister_edge + "> ?p}"
	for line in list(ontology.query(q)):
		answer.append(clean(line))
	return answer


def what_is_pop(country):
	answer = []
	q = "select ?p where { <" + wiki_prefix + "/wiki/" + country + "> <" + population_edge + "> ?p} "
	for line in list(ontology.query(q)):
		answer.append(clean(line))
	return answer


def what_is_area(country):
	answer = []
	q = "select ?a where { <" + wiki_prefix + "/wiki/" + country + "> <" + area_edge + "> ?a} "
	for line in list(ontology.query(q)):
		answer.append(clean(line))
	return answer


def what_is_gov(country):
	answer = []
	q = "select ?g where { <" + wiki_prefix + "/wiki/" + country + "> <" + government_edge + "> ?g} "
	for line in list(ontology.query(q)):
		answer.append(clean(line))
	return answer


def what_is_cap(country):
	answer = []
	q = "select ?c where { <" + wiki_prefix + "/wiki/" + country + "> <" + capital_edge + "> ?c} "
	for line in list(ontology.query(q)):
		answer.append(clean(line))
	return answer


def when_was_pres_born(country):
	answer = []
	q = "select ?d where {<" + wiki_prefix + "/wiki/" + country + "> <" + president_edge + "> ?p . ?p <" + birthDate_edge + "> ?d}"
	for line in list(ontology.query(q)):
		answer.append(clean_date(line))
	return answer


def when_was_pm_born(country):
	answer = []
	q = "select ?d where {<" + wiki_prefix + "/wiki/" + country + "> <" + prime_minister_edge + "> ?p . ?p <" + birthDate_edge + "> ?d}"
	for line in list(ontology.query(q)):
		answer.append(clean_date(line))
	return answer


def who_is(person):
	answer = []
	q = "select ?c where { ?c <" + prime_minister_edge + "> <" + wiki_prefix + "/wiki/" + person + ">} "
	for line in list(ontology.query(q)):
		answer.append("Prime minister of " + clean(line))

	q = "select ?c where { ?c <" + president_edge + "> <" + wiki_prefix + "/wiki/" + person + ">} "
	for line in list(ontology.query(q)):
		answer.append("President of " + clean(line))
	return answer
