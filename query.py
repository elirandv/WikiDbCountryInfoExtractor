import ontology_maker
import rdflib

ontology = rdflib.Graph()
ontology.parse("ontology.nt", format="nt")
wiki_prefix = "http://en.wikipedia.org"


# country edges
president_edge = rdflib.URIRef(wiki_prefix + "/president")
prime_minister_edge = rdflib.URIRef(wiki_prefix + "/prime_minister")
population_edge = rdflib.URIRef(wiki_prefix + "/population")
area_edge = rdflib.URIRef(wiki_prefix + "/area")
government_edge = rdflib.URIRef(wiki_prefix + "/government")
capitol_edge = rdflib.URIRef(wiki_prefix + "/capitol")

# person edges
birthDate_edge = rdflib.URIRef(wiki_prefix + "/birthDate")


def who_is_pres(country):
	q = "select ?p where { ?p <" + president_edge + "> <" + wiki_prefix +"/wiki/"+ country + ">} "
	return ontology.query(q)


def who_is_pm(country):
	q = "select ?p where { " \
	    " ?p <" + prime_minister_edge + "> <" + wiki_prefix + country + ">} "
	return ontology.query(q)


def what_is_pop(country):
	q = "select ?p where { " \
	    " ?p <" + population_edge + "> <" + wiki_prefix + country + ">} "
	return ontology.query(q)


def what_is_area(country):
	q = "select ?a where { " \
	    " ?a <" + area_edge + "> <" + wiki_prefix + country + ">} "
	return ontology.query(q)


def what_is_gov(country):
	q = "select ?g where { " \
	    " ?g <" + government_edge + "> <" + wiki_prefix + country + ">} "
	return ontology.query(q)


def what_is_cap(country):
	q = "select ?c where { " \
	    " ?c <" + capitol_edge + "> <" + wiki_prefix + country + ">} "
	return ontology.query(q)


def when_was_pres_born(country):
	q = "select ?d where { " \
	    " ?p <" + president_edge + "> <" + wiki_prefix + country + ">} " \
	                                                               " ?p <" + birthDate_edge + "> ?d} "
	return ontology.query(q)


def when_was_pm_born(country):
	q = "select ?d where { " \
	    " ?p <" + prime_minister_edge + "> <" + wiki_prefix + country + ">} " \
	                                                                    " ?p <" + birthDate_edge + "> ?d} "
	return ontology.query(q)


def who_is(person):
	q = "select ?e ?c where {" + person + " ?e ?c} "
	return ontology.query(q)
