import requests
import lxml.html
import rdflib


wiki_prefix = "http://en.wikipedia.org"
example_prefix = "http://example.org/"

# i use global ontology for faster run time
ontology = rdflib.Graph()

# country edges
president_edge = rdflib.URIRef(wiki_prefix + "/president")
prime_minister_edge = rdflib.URIRef(wiki_prefix + "/prime_minister")
population_edge = rdflib.URIRef(wiki_prefix + "/population")
area_edge = rdflib.URIRef(wiki_prefix + "/area")
government_edge = rdflib.URIRef(wiki_prefix + "/government")
capitol_edge = rdflib.URIRef(wiki_prefix + "/capitol")

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


def get_player_info(url, player):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)

    wiki_infobox = doc.xpath("//table[contains(@class, 'infobox')]")
    try:
        # date of birth
        b = wiki_infobox[0].xpath("//table//th[contains(text(), 'Date of birth')]")
        date = b[0].xpath("./../td//span[@class='bday']//text()")[0]
        date = clean_string(date)
        dob = rdflib.Literal(date, datatype=rdflib.XSD.date)
        ontology.add((player, birthDate_edge, dob))
    except:
        pass
    try:
        # place of birth
        c = wiki_infobox[0].xpath("//table//th[contains(text(), 'Place of birth')]")
        pob_str = c[0].xpath("./../td//a/text()")[0]
        pob_str = clean_string(pob_str)
        pob = rdflib.URIRef(example_prefix + pob_str)
        ontology.add((player, birthPlace_edge, pob))
        try:
            pob_link = wiki_prefix + c[0].xpath("./../td//a/@href")[0]
            get_city_info(pob_link, pob)
        except:
            pass
    except:
        pass
    try:
        # player position
        d = wiki_infobox[0].xpath("//table//th[contains(text(), 'Playing position')]")
        str_pos = d[0].xpath("./../td//a/text()")[0].replace(" ", "_")
        str_pos = clean_string(str_pos)
        player_pos = rdflib.URIRef(example_prefix + str_pos)
        ontology.add((player, position_edge, player_pos))
    except:
        pass


def add_to_onto(str):
    return rdflib.URIRef(wiki_prefix + "/" + str)


def get_person_info(person, url):
    #dob = rdflib.Literal(date, datatype=rdflib.XSD.date)
    return


def get_pres(infobox, country):
    try:
        pres = infobox.xpath(".//a[text() = 'President']/../../following-sibling::td//a/@href")[0]
        president = clean_string(pres)
        pres_link = wiki_prefix + pres

        # print(president + "\t" + pres_link)
        president = add_to_onto(president)
        ontology.add((country, president_edge, president))

        get_person_info(president, pres_link)
    except Exception:
        print("\n** President collection Error: "+country+" **\n")
        print(e)
        pass


def get_pm(infobox, country):
    global times
    try:
        pm = infobox.xpath(".//a[text() = 'Prime Minister']/../../following-sibling::td//a/@href")[0]
        prime_m = clean_string(pm)
        pm_link = wiki_prefix + pm

        print("\t" + prime_m + "\t" + pm_link)
        prime_m = add_to_onto(prime_m)
        ontology.add((country, prime_minister_edge, prime_m))
        times+=1
        get_person_info(prime_m, pm_link)
    except Exception as e:
        print("\n** Prime Minister collection Error: "+country+" **\n")
        print(e)
        # pass
    print(times)


def get_government(infobox, country):
    global times_gvm_m
    global times_gvm_r
    try:
        gvlist = infobox.xpath(".//a[contains(text(), 'Government')]/../../td//text()|.//th[contains(text(), "
                               "'Government')]/../td//text()")
        government = handle_gvlist(gvlist)
        if government == "":
            raise ValueError('Government Not Found')

        print(government + "\t")
        government = add_to_onto(government)
        ontology.add((country, government_edge, government))

    except Exception as e:
        print(e)
        print("\n** Government collection Error: "+country+" **\n")
        exit()


def get_area(infobox, country):
    try:
        a = infobox.xpath("(.//a[contains(text(), 'Area')]/../../following-sibling::tr//td//text())[1]|(.//th[contains(text(), 'Area')]/../following-sibling::tr//td//text())[1] ")[0]
        area = clean_string(a)

        #print("\n\tArea="+area)
        area = add_to_onto(area)
        ontology.add((country, area_edge, area))

    except Exception as e:
        print(e)
        print("\n** Area collection Error: "+country+" **\n")
        exit()
        # pass


def get_pop(infobox, country):
    try:
        p = infobox.xpath("(.//a[contains(text(), 'Population')]/../../following-sibling::tr//td//text())[1]|(.//th[contains(text(), 'Population')]/../following-sibling::tr//td//text())[1]")[0]
        population = clean_string(p)

        #print("\n\tPopulation="+population)
        population = add_to_onto(population)
        ontology.add((country, population_edge, population))

    except Exception as e:
        print(e)
        print("\n** Population collection Error: "+country+" **\n")
        exit()
        # pass


times = 0
times_gvm_m = 0
times_gvm_r = 0
def get_country_info(country, url):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)

    infoboxlist = doc.xpath("//table[contains(@class, 'infobox')]")
    # capital
    # it's possible to get more than one infobox, in that case, check all of them
    #for i in range(len(infoboxlist)):
    # president
    #get_pres(infoboxlist[0], country)
    # prime minister
    #get_pm(infoboxlist[0], country)
    # government
    #get_government(infoboxlist[0], country)
    # area
    get_area(infoboxlist[0], country)
    # population
    get_pop(infoboxlist[0], country)
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
            exit()
            continue
    return res


def make_ontology(url):
    # get dict of countries and links to wikipages
    country_dict = get_countries(url)
    i = 1
    res = 0
    for country in country_dict:
        url = country_dict[country]
        #print("\nCountry#" + str(i))
        #print("\t"+country + "\t" + url)

        rdf_c = add_to_onto(country)
        res += get_country_info(rdf_c, url)
        i += 1
        # if i == 6:
        #     break
    print("Countries count in ontology.nt :" + str(res))


if __name__ == '__main__':
    print("running...")

    make_ontology("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")
    ontology.serialize("ontology.nt", format="nt")

    print("done.")
