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
capitol_edge = wiki_prefix + "/capitol"

# person edges
birthDate_edge = wiki_prefix + "/birthDate"


def clean(line):
    line = str(line)
    line.replace("(rdflib.term.URIRef('http://en.wikipedia.org/wiki/", "")
    line.replace(",", "")
    line.replace("'", "")
    line.replace(")", "")
    line.replace("_", " ")
    return line


def who_is_pres(country):
    answer = []
    print(country)
    q = "select ?p where { <" + wiki_prefix + "/wiki/" + country + "> <" + president_edge + "> ?p}"
    for line in list(ontology.query(q)):
        print(clean(line))
        answer.append(clean(line))
    return answer



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
