import query


# aux func
def unclean_str_lst(str_lst):
    res = ""
    for str in str_lst:
        res += str
        res += '_'
    return res[:-1]


def who_ques(question):
    if len(question) < 3:
        return 'Error: who question too short'
    if question[1] != "is":
        return 'Error'
    if question[2] == "the":
        # who is president of..
        if len(question) < 6:
            return 'Error: who question too short'
        if question[3] == "president" and question[4] == "of":
            return query.who_is_pres(unclean_str_lst(question[5:]))

        # who is prime minister of..
        if len(question) < 7:
            return 'Error: who question too short'
        if question[3] == "prime" and question[4] == "minister" and question[5] == "of":
            return query.who_is_pm(question[6])

    # who is <person>
    if len(question) > 3:
        return 'Error: who question too long'
    return query.who_is(question[2])


def what_ques(question):
    if len(question) < 6:
        return 'Error: what question too short'
    return 'Error'


def when_ques(question):
    return 'Error'


def parse(question):
    # question is an array of words
    if len(question) < 1:
        return 'Error: empty question'
    if question[len(question)-1].endswith("?"):
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
        answer = 'Error'

    return answer

