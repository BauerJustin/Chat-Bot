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
    
def greeting_response(greeting, sentences):
    greeting = greeting.lower()

    # loop through all the words in the input and if any match to greeting bot will reply with a greeting
    for word in greeting.split():
        if word in text['greeting'][0]:
            return random.choice(text['greeting'][1])

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
    #variables
    sentence_list = []
    article_given = False

    bot_print("Hello There! I am your friendly chat bot.")
    
    while(True):

        # main user input
        user_input = input()

        # user must input non whitespace characters to get a response
        if len(user_input.strip()) > 0:
            # Case when user says bye
            if user_input.lower() in text['farewell'][0]:
                bot_print(random.choice(text['farewell'][1]))
                break
            # Case when user says hello
            elif greeting_response(user_input, sentence_list) != None:
                bot_print(greeting_response(user_input, sentence_list))
            # Case when user is done with the article
            elif user_input == "done" and article_given:
                sentence_list = []
                article_given = False
                bot_print("Article is no longer loaded.")
            # Case when user is asking questions about the article
            elif article_given:
                bot_print(artbot.bot_article_response(user_input, sentence_list, text))
            # Case when user is inputting an article
            elif len(user_input) > 50 and not (' ' in user_input.strip()):
                sentence_list = artbot.get_article(user_input.strip())
                article_given = True
                bot_print("Article loaded! Ask me your questions. \nType done when you don't have any more questions.")
            # Case when program does not recongize users input
            else:
                bot_print(random.choice(text['unknown'][1]))

main()