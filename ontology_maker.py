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


def get_city_info(url, city):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)

    try:
        wiki_infobox = doc.xpath("//table[contains(@class, 'infobox')]")[0]
        country = wiki_infobox.xpath("//table//th[contains(.,'country')] | //table//th[contains(.,'Country')]")

        try:
            country_str = country[0].xpath("./../td//a//text()")[0].replace(" ", "_")
        except IndexError:
            country_str = country[0].xpath("./../td//text()")[0].replace(" ", "_")

    except IndexError:
        return None
    country = rdflib.URIRef(example_prefix + country_str)
    ontology.add((city, located_in_edge, country))
    return country


def get_team_info(url, team):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    playerTable = doc.xpath(
        "(//table[.//th/text()[contains(., 'Position')] and .//th/text()[contains(., 'Player')]])[not(position("
        ")>3)]/tbody/tr")

    for i in range(1, len(playerTable)):
        try:
            row = playerTable[i].xpath(".//text()")
            new_row = [x for x in row if x != '\n']

            player_str = clean_string(new_row[2])
            player = rdflib.URIRef(example_prefix + player_str)
            player_url = wiki_prefix + playerTable[i].xpath(".//@href")[2]

            if team is not None:
                ontology.add((player, playsFor_edge, team))
            get_player_info(player_url, player)
        except IndexError:
            continue


def get_league_info(url):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    teamTable = doc.xpath(
        "//table[.//th/text() [contains(., 'Team')] and .//th/text() [contains(., 'Location')]]/tbody/tr")

    league_name = doc.xpath("//h1[@id='firstHeading']/text()")[0].replace(" ", "_")
    league = rdflib.URIRef(example_prefix + league_name)

    for i in range(1, len(teamTable)):
        try:
            print("team#" + str(i))
            row = teamTable[i].xpath(".//text()")
            new_row = [x for x in row if x != '\n']

            team_str = clean_string(new_row[0])
            team = rdflib.URIRef(example_prefix + team_str)
            team_url = wiki_prefix + teamTable[i].xpath(".//td[1]//@href")[0]

            city_str = clean_string(new_row[1])
            city = rdflib.URIRef(example_prefix + city_str)
            city_url = wiki_prefix + teamTable[i].xpath(".//td[2]//@href")[0]

            ontology.add((team, league_edge, league))
            ontology.add((team, homeCity_edge, city))
            # country is a URIref or None
            country = get_city_info(city_url, city)
            get_team_info(team_url, team)
            # maybe add different countries to the same league, that is ok
            if country is not None:
                ontology.add((league, country_edge, country))
        except IndexError:
            continue


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

        get_person_info(prime_m, pm_link)
    except Exception as e:
        print("\t-- get_pm Error: --")
        print(e)
    times+=1
    print(times)
        # if times > 4:
            # exit()
        # else:
            # times+=1
        # pass


def get_government(infobox, country):
    global times
    try:
        gvlist = infobox.xpath(".//a[contains(text(), 'Government')]/../../td//text()")
        print(gvlist)
        exit()
        government = clean_string(gv)

        print(government + "\t")
        government = add_to_onto(government)
        ontology.add((country, government_edge, government))

    except Exception as e:
        print(e)
        print("\nError\n")
        if times > 4:
            exit()
        else:
            times+=1
        # pass


times = 0
def get_country_info(country, url):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)

    infoboxlist = doc.xpath("//table[contains(@class, 'infobox')]")
    # population
    # area
    # capital
    # it's possible to get more than one infobox, in that case, check all of them
    #for i in range(len(infoboxlist)):
    # president
    get_pres(infoboxlist[0], country)
    # prime minister
    get_pm(infoboxlist[0], country)
    # government
    get_government(infobox, country)
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
        print("\nCountry#" + str(i))
        print("\t"+country + "\t" + url)

        rdf_c = add_to_onto(country)
        res += get_country_info(rdf_c, url)
        i += 1
        # if i == 6:
        #     break
    print("final res=" + str(res))


if __name__ == '__main__':
    print("running...")

    make_ontology("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")
    ontology.serialize("ontology.nt", format="nt")

    print("done.")
