import ontology_maker
import rdflib
import os

ontology = rdflib.Graph()
if os.path.isfile("ontology.nt"):
	ontology.parse("ontology.nt", format="nt")

wiki_prefix = "https://en.wikipedia.org"

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
	line = line.replace("https://en.wikipedia.org/wiki/", "")
	line = line.replace("_", " ")
	if line.endswith(","):
		line = line[:-1]
	return line.title()


def who_is_pres(country):
	answer = []
	q = "select ?p where { <" + wiki_prefix + "/wiki/" + country + "> <" + president_edge + "> ?p}"
	for line in ontology.query(q):
		answer.append(clean(line.p))
	return answer


def who_is_pm(country):
	answer = []
	q = "select ?p where { <" + wiki_prefix + "/wiki/" + country + "> <" + prime_minister_edge + "> ?p}"
	for line in ontology.query(q):
		answer.append(clean(line.p))
	return answer


def what_is_pop(country):
	answer = []
	q = "select ?p where { <" + wiki_prefix + "/wiki/" + country + "> <" + population_edge + "> ?p} "
	for line in ontology.query(q):
		answer.append(clean(line.p))
	return answer


def what_is_area(country):
	answer = []
	q = "select ?a where { <" + wiki_prefix + "/wiki/" + country + "> <" + area_edge + "> ?a} "
	for line in ontology.query(q):
		answer.append(clean(line.a))
	return answer


def what_is_gov(country):
	answer = []
	q = "select ?g where { <" + wiki_prefix + "/wiki/" + country + "> <" + government_edge + "> ?g} "
	for line in ontology.query(q):
		answer.append(clean(line.g))
	return answer


def what_is_cap(country):
	answer = []
	q = "select ?c where { <" + wiki_prefix + "/wiki/" + country + "> <" + capital_edge + "> ?c} "
	for line in ontology.query(q):
		answer.append(clean(line.c))
	return answer


def when_was_pres_born(country):
	answer = []
	q = "select ?d where {<" + wiki_prefix + "/wiki/" + country + "> <" + president_edge + "> ?p . ?p <" + birthDate_edge + "> ?d}"
	for line in ontology.query(q):
		answer.append(line.d)
	return answer


def when_was_pm_born(country):
	answer = []
	q = "select ?d where {<" + wiki_prefix + "/wiki/" + country + "> <" + prime_minister_edge + "> ?p . ?p <" + birthDate_edge + "> ?d}"
	for line in ontology.query(q):
		answer.append(line.d)
	return answer


def who_is(person):
	answer = []
	q = "select ?c where { ?c <" + prime_minister_edge + "> <" + wiki_prefix + "/wiki/" + person + ">} "
	for line in ontology.query(q):
		answer.append("Prime minister of " + clean(line.c))

	q = "select ?c where { ?c <" + president_edge + "> <" + wiki_prefix + "/wiki/" + person + ">} "
	for line in ontology.query(q):
		answer.append("President of " + clean(line.c))
	return answer