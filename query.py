import query
# from sparQL import get_query


def who_is_pres(country):
    return "select ?p where { " \
        " ?p <"+president_edge+"> <"+wiki_prefix+country+">} "

def who_is_pm(country):
	return "select ?p where { " \
        " ?p <"+prime_minister_edge+"> <"+wiki_prefix+country+">} "

def what_is_pop(country):
	return "select ?p where { " \
        " ?p <"+population_edge+"> <"+wiki_prefix+country+">} "
       
def what_is_area(country):
    return "select ?a where { " \
        " ?a <"+area_edge+"> <"+wiki_prefix+country+">} "

def what_is_gov(country):
	return "select ?g where { " \
        " ?g <"+government_edge+"> <"+wiki_prefix+country+">} "

def what_is_cap(country):
	return "select ?c where { " \
        " ?c <"+capitol_edge+"> <"+wiki_prefix+country+">} "

def when_was_pres_born(country):
	return "select ?d where { " \
        " ?p <"+president_edge+"> <"+wiki_prefix+country+">} " \
        " ?p <"+birthDate_edge+"> ?d} "
       
def when_was_pm_born(country):
	return "select ?d where { " \
        " ?p <"+prime_minister_edge+"> <"+wiki_prefix+country+">} " \
        " ?p <"+birthDate_edge+"> ?d} "

def who_is(person):
	return "select ?e ?c where { " \
        " "+person+" ?e ?c} "
