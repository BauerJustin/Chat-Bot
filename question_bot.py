# required imports
import json
import random

# load answer dictionary from json file
file = open("questionAnswers.json")
answers = json.loads(file.read())
file.close()

def answerQuestion(sentence):
    scores = [0]
    response = ""

    for word in sentence.split():
        if word in answers['welcoming'][0]:
            scores[0] += 1
    
    max_index = len(scores)-1
    for i in range(max_index):
        if scores[i] > scores[max_index]:
            max_index = i

    if max_index == 0:
        response = random.choice(answers['welcoming'][1])
    else:
        response = random.choice(answers['unknown'][1])

    return response