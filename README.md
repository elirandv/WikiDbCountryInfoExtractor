# WikiDbCountryInfoExtractor
WikiDb Country Information Extractor

School of Computer Science, Faculty of Exact Sciences, Tel-Aviv University
https://en-exact-sciences.tau.ac.il/computer

* 2019-2020 Web Data Management Workshop - Final Project

The challenge: 

This repository is a system for Information Extraction from Wikipedia and answering questions in natural language.
The program creates an ontology of the countries of the world, their capitals, presidents, prime ministers, type of regime, size of the country & the amount of population; 
After creating an ontology, The user can ask for answers from the program by using natural language questions.

Knowledge & Libraries in use: HTML, Xpath, IE, SPARQL, lxml, rdflib

## Requirements

* [Python 3.X](https://docs.python.org/3/)

## Getting Started

```bash
$ git clone https://github.com/elirandv/WikiDbCountryInfoExtractor
$ cd /WikiDbCountryInfoExtractor
```

## Running Tester (Ontology creation & queries attempts)

Next step is to enter the bash and run:

```bash
$ python answers.py
```

## Running Manually

Next step is to enter the bash and run:

```bash
$ python geo_qa.py create ontology.nt                    # creats ontology.nt
$ python geo_qa.py question "<question format>"          # requesting an info
```

## Passible Question Formats (case-insensitive)

who is the president of <country>?
who is the prime minister of <country>?
what is the population of <country>?
what is the area of <country>?
What is the government of <country>?
what is the capital of <country>?
when was the president of <country> born?
when was the prime minister of <country> born?
who is <person>?

## Running Example

```bash
$ python geo_qa.py question "who is the prime minister of United Kingdom?
$ Sergio Mattarella
$ python geo_qa.py question "who is the prime minister of United Kingdom?
$ Boris Johnson
$ python geo_qa.py question "what is the population of Democratic Republic of the Congo?
$ 101,780,263
$ python geo_qa.py question "what is the area of Fiji?
$ 18,274 Km2
$ python geo_qa.py question "What is the government of Eswatini?
$ Unitary Parliamentary Absolute Monarchy
$ python geo_qa.py question "what is the capital of Canada?
$ Ottawa
$ python geo_qa.py question "when was the president of South Korea born?
$ 1953-01-24
$ python geo_qa.py question "when was the prime minister of New Zealand born?
$ 1980-07-26
$ python geo_qa.py question "who is Donald Trump?
$ President of United States
$ python geo_qa.py question "who is Kyriakos Mitsotakis?
$ Prime minister of Greece
```

### Features

* World Countries Information Extraction from Wikipedia into XML Ontology (IE,Xpath).
* Natural language questions answering using SPARQL queries on the created ontology.

### Maintainers

* Oz Granit
* Eliran Eitan

