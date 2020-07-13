# Required imports
import article_bot as abot
import question_bot as qbot
import sys
import random
import string
import json
import re
from copy import deepcopy
from time import sleep

# load text dictionary from json file
file = open("data/baseText.json")
text = json.loads(file.read())
backup_text = deepcopy(text)
file.close()

# initialize regex
regex = re.compile('[%s]' % re.escape(string.punctuation))
    
def bot_response(sentence):
    sentence = regex.sub('', sentence).lower()
    scores = [0,0,0,0,0,0]

    # loop through all the words in the input and count the matches
    for word in sentence.split():
        if word in text['greeting'][0]:
            scores[0] += 1
        if word in text['farewell'][0]:
            scores[1] += 1
        if word in text['question'][0]:
            scores[2] += 2
        if word in text['article'][0]:
            scores[3] += 1
        if word in text['thanks'][0]:
            scores[4] += 1
    
    max_index = len(scores)-1
    for i in range(max_index):
        if scores[i] > scores[max_index]:
            max_index = i

    if max_index == 0:
        bot_print(random.choice(text['greeting'][1]))
    elif max_index == 1:
        bot_print(random.choice(text['farewell'][1]))
    elif max_index == 2:
        bot_print(qbot.answerQuestion(sentence))
    elif max_index == 3:
        bot_print(random.choice(text['article'][1]))
    elif max_index == 4:
        bot_print(random.choice(text['thanks'][1]))
    else:
        bot_print(random.choice(text['unknown'][1]))
    
    # update json file 
    addWordsToDict(sentence, max_index)

    return max_index

def process_article(user_input):
    # load article
    sentence_list = abot.get_article(user_input.strip())
    article_given = True
    bot_print("Article loaded! Ask me your questions. \nType done when you don't have any more questions.")
    while(article_given):
        # let user ask questions about article
        user_input_article = input()
        if len(user_input_article.strip()) > 0:
            if user_input_article == "done":
                sentence_list = []
                bot_print("Article is no longer loaded.")
                article_given = False
            elif user_input_article.lower() in text['farewell'][0]:
                bot_print("Type done first if you want to say goodbye.")
            else:
                bot_print(abot.bot_article_response(user_input_article, sentence_list, text))

def addWordsToDict(sentence, index):
    # determine key for dictionary
    key = ""
    if index == 0:
        key = 'greeting'
    elif index == 1:
        key = 'farewell'
    elif index == 3:
        key = 'article'
    elif index == 4:
        key = 'thanks'
    
    if key != "":
        # append new words not known to dictionary
        for word in sentence.split():
            if word not in text[key][0]:
                text[key][0].append(word)

    # write changes to json file
    with open("data/baseText.json", 'w') as file:
        json.dump(text, file)

def bot_print(sentence):
    # print bot output with 'typing' animation 
    sentence += "\n"
    sys.stdout.write("ASI: ")
    sys.stdout.flush()
    for char in sentence:
        sleep(0.03)
        sys.stdout.write(char)
        sys.stdout.flush()

def main():

    bot_print("Hello There! I am ASI, your friendly chat bot.")
    
    while(True):

        # main user input
        user_input = input()

        # user must input non whitespace characters to get a response
        if len(user_input.strip()) > 0:
            # Case when user inputs an article
            if abot.is_article(user_input):
                process_article(user_input)
            # Case to clear changes to text files
            elif user_input.strip().lower() == "clear":
                with open("data/baseText.json", 'w') as file:
                    json.dump(backup_text, file)
                text = deepcopy(backup_text)
                qbot.clearQuestionsDict()
                bot_print("Changes have been cleared!")
            # Case when algorithm determines bot response
            else:
                index = bot_response(user_input)
                # end convo
                if index == 1:
                    break

if __name__ == "__main__":
    main()