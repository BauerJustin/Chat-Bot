# Required imports
import article_bot as artbot
import sys
import random
import string
import json
from time import sleep

# load text dictionary from json file
file = open("text.json")
text = json.loads(file.read())
file.close()
    
def bot_response(sentence):
    sentence = sentence.lower()
    scores = [0,0,0]

    # loop through all the words in the input and count the matches
    for word in sentence.split():
        if word in text['greeting'][0]:
            scores[0] += 1
        elif word in text['farewell'][0]:
            scores[1] += 1
    
    max_index = len(scores)-1
    for i in range(max_index):
        if scores[i] > scores[max_index]:
            max_index = i

    if max_index == 0:
        bot_print(random.choice(text['greeting'][1]))
    elif max_index == 1:
        bot_print(random.choice(text['farewell'][1]))
    else:
        bot_print(random.choice(text['unknown'][1]))
    
    return max_index

def process_article(user_input):
    # load article
    sentence_list = artbot.get_article(user_input.strip())
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
                bot_print(artbot.bot_article_response(user_input_article, sentence_list, text))

def bot_print(sentence):
    # print bot output with 'typing' animation 
    sentence += "\n"
    sys.stdout.write("Bot: ")
    sys.stdout.flush()
    for char in sentence:
        sleep(0.03)
        sys.stdout.write(char)
        sys.stdout.flush()

def main():

    bot_print("Hello There! I am your friendly chat bot.")
    
    while(True):

        # main user input
        user_input = input()

        # user must input non whitespace characters to get a response
        if len(user_input.strip()) > 0:
            # Case when user inputs an article
            if artbot.is_article(user_input):
                process_article(user_input)
            # Case when algorithm determines bot response
            else:
                index = bot_response(user_input)
                if index == 1:
                    break

main()