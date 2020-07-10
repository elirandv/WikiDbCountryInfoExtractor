import sys
from ontology_maker import make_ontology
#from parser import parse
#from sparQL import get_query

if __name__ == '__main__':
    command=sys.argv[1]
    if (command=="create"):  
        print("Createing ontology...")
        make_ontology("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")
        print("Ontology.nt was added")
    elif command=="question":

        # query = parser(sys.argv[2])
        
        query = "select ?c where { " \
            " ?c <"+prefix+"catpital> <"+prefix+"Central_African_Republic>} "
            
        # get_query(query, "ontology.nt")
        print("w")
    else:
        # (command!="create" or command!="question"):
        print("Illegal command, please try 'create' or 'question'.")
    print("WikiDb Country Info Extractor command done.")



















#can u see this change??????