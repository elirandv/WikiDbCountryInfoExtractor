import ontology_maker

wiki_prefix = "http://en.wikipedia.org"

def who_is_pres(country):
    q = "select ?p where { " \
        " ?p <"+president_edge+"> <"+wiki_prefix+country+">} "
    x1 = ontology.query(q)
    for line in list(x1):
        print(line)

def who_is_pm(country):
	x1 = "select ?p where { " \
        " ?p <"+prime_minister_edge+"> <"+wiki_prefix+country+">} "
    x1 = ontology.query(q)
    for line in list(x1):
        print(line)

def what_is_pop(country):
	x1 = "select ?p where { " \
        " ?p <"+population_edge+"> <"+wiki_prefix+country+">} "
    x1 = ontology.query(q)
    for line in list(x1):
        print(line)
        
def what_is_area(country):
    x1 = "select ?a where { " \
        " ?a <"+area_edge+"> <"+wiki_prefix+country+">} "
    x1 = ontology.query(q)
    for line in list(x1):
        print(line)
        
def what_is_gov(country):
	x1 = "select ?g where { " \
        " ?g <"+government_edge+"> <"+wiki_prefix+country+">} "
    x1 = ontology.query(q)
    for line in list(x1):
        print(line)
        
def what_is_cap(country):
	x1 = "select ?c where { " \
        " ?c <"+capitol_edge+"> <"+wiki_prefix+country+">} "
    x1 = ontology.query(q)
    for line in list(x1):
        print(line)
        
def when_was_pres_born(country):
	x1 = "select ?d where { " \
        " ?p <"+president_edge+"> <"+wiki_prefix+country+">} " \
        " ?p <"+birthDate_edge+"> ?d} "
    x1 = ontology.query(q)
    for line in list(x1):
        print(line)
               
def when_was_pm_born(country):
	x1 = "select ?d where { " \
        " ?p <"+prime_minister_edge+"> <"+wiki_prefix+country+">} " \
        " ?p <"+birthDate_edge+"> ?d} "
    x1 = ontology.query(q)
    for line in list(x1):
        print(line)
        
def who_is(person):
	x1 = "select ?e ?c where { " \
        " "+person+" ?e ?c} "
    x1 = ontology.query(q)
    for line in list(x1):
        print(line)
        

