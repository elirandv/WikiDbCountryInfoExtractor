from query import *


# aux func
def fix_str_lst(str_lst):
    res = ""
    for str in str_lst:
        res += str
        res += '_'
    return res[:-1]


def who_ques(question):
    if len(question) < 3:
        return 'Error: who question too short'
    if question[1] != "is":
        return 'Error: wrong "who" question format'
    if question[2] == "the":
        # who is president of..
        if len(question) < 6:
            return 'Error: who question too short'
        if question[3] == "president" and question[4] == "of":
            return who_is_pres(fix_str_lst(question[5:]))

        # who is prime minister of..
        if len(question) < 7:
            return 'Error: who question too short'
        if question[3] == "prime" and question[4] == "minister" and question[5] == "of":
            return who_is_pm(fix_str_lst(question[6:]))

    # who is <person>
    return who_is(fix_str_lst(question[2:]))


def what_ques(question):
    if len(question) < 6:
        return 'Error: what question too short'
    if question[1] != "is" or question[2] != "the" or question[4] != "of":
        return 'Error: wrong "what" question format'
    if question[3] == "population":
        return what_is_pop(fix_str_lst(question[5:]))
    if question[3] == "area":
        return what_is_area(fix_str_lst(question[5:]))
    if question[3] == "government":
        return what_is_gov(fix_str_lst(question[5:]))
    if question[3] == "capital":
        return what_is_cap(fix_str_lst(question[5:]))
    return 'Error: unknown "what" question'


def when_ques(question):
    if len(question) < 7:
        return 'Error: when question too short'
    if question[1] != "was" or question[2] != "the" or question[-1] != "born":
        return 'Error: wrong "when" question format'
    if question[3] == "president" and question[4] == "of":
        return when_was_pres_born(fix_str_lst(question[5:-1]))
    if question[3] == "prime" and question[4] == "minister" and question[5] == "of":
        return when_was_pm_born(fix_str_lst(question[6:-1]))
    return 'Error: unknown "what" question'


def parse(question):
    # question is an array of words
    if len(question) < 1:
        return 'Error: empty question'

    if not question[len(question)-1].endswith('?'):
        return 'Error: please end with "?"'
    # slice '?' from end
    question[len(question) - 1] = question[len(question)-1][:-1]

    if question[0] == 'Who' or question[0] == 'who':
        answer = who_ques(question)
    elif question[0] == 'What' or question[0] == 'what':
        answer = what_ques(question)
    elif question[0] == 'When' or question[0] == 'when':
        answer = when_ques(question)
    else:
        answer = 'Error: not a question'

    return answer

