import requests
import lxml.html
import rdflib

wiki_prefix = "http://en.wikipedia.org"

# i use global ontology for faster run time
ontology = rdflib.Graph()

# country edges
president_edge = rdflib.URIRef(wiki_prefix + "/president")
prime_minister_edge = rdflib.URIRef(wiki_prefix + "/prime_minister")
population_edge = rdflib.URIRef(wiki_prefix + "/population")
area_edge = rdflib.URIRef(wiki_prefix + "/area")
government_edge = rdflib.URIRef(wiki_prefix + "/government")
capital_edge = rdflib.URIRef(wiki_prefix + "/capital")

# person edges
birthDate_edge = rdflib.URIRef(wiki_prefix + "/birthDate")


# aux func
def clean_string(some_str):
    # some_str = "".join(some_str.splitlines())
    if some_str.startswith('/wiki/'):
        some_str = some_str[6:]
    return some_str.strip().replace("\n", "").replace(" ", "_")


def handle_gvlist(strlist):
    res = ""
    for str in strlist:
        if '[' in str or ']' in str:
            continue
        res += str
    return clean_string(res)


def add_to_onto(str):
    return rdflib.URIRef(wiki_prefix + "/wiki/" + str)


def get_person_info(person, url):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)

    try:
        # date of birth
        try:
            date = doc.xpath("//*[@class='bday']/text()")[0]
        except IndexError:
            date = doc.xpath("//*[./th/text()='Born']/td/text()")[0]
            if not any(char.isdigit() for char in date):
                return
        date = clean_string(date)

        # print(str(person) + "\t" + date)
        dob = rdflib.Literal(date, datatype=rdflib.XSD.date)
        ontology.add((person, birthDate_edge, dob))
    except Exception as e:
        # print(e)
        # print("\n** Person collection Error: " + str(person) + " **\n")
        pass


def get_pres(infobox, country):
    try:
        pres = infobox.xpath(".//a[text() = 'President']/../../following-sibling::td//a/@href")[0]
        president = clean_string(pres)
        pres_link = wiki_prefix + pres

        # print(president + "\t" + pres_link)
        president = add_to_onto(president)
        ontology.add((country, president_edge, president))

        get_person_info(president, pres_link)
    except Exception as e:
        # print("\n** President collection Error: "+str(country)+" **\n")
        # print(e)
        pass


def get_pm(infobox, country):
    try:
        pm = infobox.xpath(".//a[text() = 'Prime Minister']/../../following-sibling::td//a/@href")[0]
        prime_m = clean_string(pm)
        pm_link = wiki_prefix + pm

        # print("\t" + prime_m + "\t" + pm_link)
        prime_m = add_to_onto(prime_m)
        ontology.add((country, prime_minister_edge, prime_m))
        get_person_info(prime_m, pm_link)

    except Exception as e:
        # print("\n** Prime Minister collection Error: "+str(country)+" **\n")
        # print(e)
        pass


def get_government(infobox, country):
    try:
        gvlist = infobox.xpath(".//a[contains(text(), 'Government')]/../../td//text()|.//th[contains(text(), "
                               "'Government')]/../td//text()")
        government = handle_gvlist(gvlist)
        if government == "":
            raise ValueError('Government Not Found')

        # print(government + "\t")
        government = add_to_onto(government)
        ontology.add((country, government_edge, government))

    except Exception:
        # print("\n** Government collection Error: " + str(country) + " **\n")
        # exit()
        pass


def clean_area(a):
    area = clean_string(a)
    words = area.split('\xa0')
    # print("\n\t** " + str(words))
    if len(words) == 1 or words[1] == "km":
        area = words[0] + "_km2"
    else:
        area = words[2].split('(')[1] + "_km2"
    return area


def get_area(infobox, country):
    try:
        a = infobox.xpath("(.//a[contains(text(), 'Area')]/../../following-sibling::tr//td//text())[1]|(.//th["
                          "contains(text(), 'Area')]/../following-sibling::tr//td//text())[1] ")[0]
        area = clean_area(a)
        if str(country) == "https://en.wikipedia.org/wiki/Channel_Islands":
            area = "198 km\u00B2"
        # print("\n\t** Area of " + str(country) + ": " + area )
        area = add_to_onto(area)
        ontology.add((country, area_edge, area))

    except Exception as e:
        # print(e)
        # print("\n** Area collection Error: " + str(country) + " **\n")
        # exit()
        pass


def get_pop(infobox, country):
    try:
        p = infobox.xpath("(.//a[contains(text(), 'Population')]/../../following-sibling::tr//td//text())[1]|(.//th["
                          "contains(text(), 'Population')]/../following-sibling::tr//td//text())[1]")[0]
        population = p.split('\xa0')[0]

        # print("\n\tPopulation="+population)
        population = add_to_onto(population)
        ontology.add((country, population_edge, population))

    except Exception as e:
        # print(e)
        # print("\n** Population collection Error: " + str(country) + " **\n")
        # exit()
        pass


def get_capital(infobox, country):
    try:
        cap = infobox.xpath("(//tr/th/text()[contains(., 'Capital')]/../../td//a[not(@class='image')]/@href)[1]")[0]
        capital = clean_string(cap)
        cap_link = wiki_prefix + cap

        # print("\t" + str(country) + ",\t" + capital + ":\t" + cap_link)

        capital = add_to_onto(capital)
        ontology.add((country, capital_edge, capital))

    except Exception as e:
        # print("\n** Capitol collection Error: "+str(country)+" **\n")
        # print(e)
        pass


def get_country_info(country, url):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)

    infoboxlist = doc.xpath("//table[contains(@class, 'infobox')]")
    # president
    get_pres(infoboxlist[0], country)
    # prime minister
    get_pm(infoboxlist[0], country)
    # government
    get_government(infoboxlist[0], country)
    # area
    get_area(infoboxlist[0], country)
    # population
    get_pop(infoboxlist[0], country)
    # capital
    get_capital(infoboxlist[0], country)
    return 1


def get_countries(url):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    # get countries form table
    countrylist = doc.xpath(
        '//table[@id="main"]/tbody/tr/td[1]//span/a[@title]')
    # edge case, add 'Channel Islands' to list
    # i put it in place for reasons unknown even to myself
    countrylist.insert(189, doc.xpath(
        '//table[@id="main"]/tbody/tr/td[1]//a[@title="Channel Islands"]')[0])
    res = {}
    for i in range(len(countrylist)):
        try:
            country = clean_string(countrylist[i].xpath("./@href")[0])
            url = wiki_prefix + countrylist[i].xpath("./@href")[0]
            res[country] = url
        except Exception as e:
            print("\t-- get_countries Error: --")
            print(e)
            # exit()
            continue
    return res


def make_ontology(url):
    # get dict of countries and links to wikipages
    country_dict = get_countries(url)
    i = 1
    res = 0
    for country in country_dict:
        url = country_dict[country]
        # print("\nCountry#" + str(i))
        # print("\t"+country + "\t" + url)

        rdf_c = add_to_onto(country)
        res += get_country_info(rdf_c, url)
        i += 1
    # print("Countries count in Ontology=" + str(res))


def call_maker():

    make_ontology("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")
    ontology.serialize("ontology.nt", format="nt")

    print("ontology.nt was added")


if __name__ == '__main__':

    make_ontology("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")
    ontology.serialize("ontology.nt", format="nt")

    print("ontology.nt was added")
