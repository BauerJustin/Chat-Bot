# required imports
import json
import random
import datetime_bot as dtbot

# load answer dictionary from json file
file = open("questionAnswers.json")
answers = json.loads(file.read())
file.close()

def answerQuestion(sentence):
    scores = [0,0,0,0]
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
        if not foundWord:
            scores[3] += 1
    
    max_index = len(scores)-1
    for i in range(max_index):
        if scores[i] > scores[max_index]:
            max_index = i

    if max_index == 0:
        response = random.choice(answers['welcoming'][1])
    elif max_index == 1:
        response = random.choice(answers['background'][1])
    elif max_index == 2:
        response = dtbot.getTime()
    else:
        response = random.choice(answers['unknown'][1])

    return response