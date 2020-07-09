# required imports
import json
import random
import datetime_bot as dtbot

# load answer dictionary from json file
file = open("data/questionAnswers.json")
answers = json.loads(file.read())
file.close()

def answerQuestion(sentence):
    scores = [0,0,0,0,0,0]
    response = ""

    # loop through all the words in the sentence and count the matches
    for word in sentence.split():
        foundWord = False
        if word in answers['welcoming'][0]:
            scores[0] += 1
            foundWord = True
        if word in answers['background'][0]:
            scores[1] += 1
            foundWord = True
        if word in answers['time'][0]:
            scores[2] += 1
            foundWord = True
        if word in answers['date'][0]:
            scores[3] += 1
            foundWord = True
        if word in answers['live'][0]:
            scores[4] += 1
            foundWord = True
        if not foundWord:
            scores[5] += 1
    
    max_index = len(scores)-1
    for i in range(max_index):
        if scores[i] > scores[max_index]:
            max_index = i

    if max_index == 0:
        response = random.choice(answers['welcoming'][1])
    elif max_index == 1:
        response = random.choice(answers['background'][1])
    elif max_index == 2:
        response = random.choice(answers['time'][1]) + dtbot.getTime()
    elif max_index == 3:
        response = random.choice(answers['date'][1]) + dtbot.getDate()
    elif max_index == 4:
        response = random.choice(answers['live'][1])
    else:
        response = random.choice(answers['unknown'][1])

    # update json dictionary with new words
    addWordsToDict(sentence, max_index)

    return response

def addWordsToDict(sentence, index):
    # determine key for dictionary
    key = ""
    if index == 0:
        key = 'welcoming'
    elif index == 1:
        key = 'background'
    elif index == 2:
        key = 'time'
    elif index == 3:
        key = 'date'
    elif index == 4:
        key = 'live'
    
    if key != "":
        # append new words not known to dictionary
        for word in sentence.split():
            if word not in answers[key][0]:
                answers[key][0].append(word)

        # write changes to json file
        with open("data/questionAnswers.json", 'w') as file:
            json.dump(answers, file)