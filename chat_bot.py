# Required imports
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from time import sleep
import sys
import random
import string
import nltk
import json
import numpy as np
nltk.download('punkt', quiet=True)

# load text dictionary from json file
file = open("text.json")
text = json.loads(file.read())
file.close()

def get_article(url):
    # Get website from user, download and parse it to apply Natural Language Processing
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    # Create a list of sentences from article text
    sentences = nltk.sent_tokenize(article.text)
    return sentences

def greeting_response(greeting, sentences):
    greeting = greeting.lower()

    # loop through all the words in the input and if any match to greeting bot will reply with a greeting
    for word in greeting.split():
        if word in text['greeting'][0]:
            return random.choice(text['greeting'][1])

def index_sort(similarity_scores_list):
    # create a list of indexes for each line in article
    list_index = list(range(0,len(similarity_scores_list)))

    # sort list of article indexes from highest to lowest to user input
    for i in range(len(similarity_scores_list)):
        for j in range(len(similarity_scores_list)):
            if similarity_scores_list[list_index[i]] > similarity_scores_list[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    
    return list_index

def bot_article_response(user_input, sentences):
    # score lines from article with relation to user input
    user_input = user_input.lower()
    sentences.append(user_input)
    bot_response = ""
    cm = CountVectorizer().fit_transform(sentences)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0

    # add sentences to bot response which have the highest match to the user input
    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response+' '+sentences[index[i]]
            response_flag = 1
            j += 1
        # limit number of matches in output
        if j > 2:
            break

    # if there is not match output random message stating the bot does not know
    if response_flag == 0:
        bot_response = bot_response+' '+random.choice(text['unknown'][1])

    sentences.remove(user_input)

    return bot_response

def bot_print(text):
    # print bot output with 'typing' animation 
    text += "\n"
    sys.stdout.write("Bot: ")
    sys.stdout.flush()
    for char in text:
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
                bot_print(bot_article_response(user_input, sentence_list))
            # Case when user is inputting an article
            elif len(user_input) > 50 and not (' ' in user_input.strip()):
                sentence_list = get_article(user_input.strip())
                article_given = True
                bot_print("Article loaded! Ask me your questions. \nType done when you don't have any more questions.")
            # Case when program does not recongize users input
            else:
                bot_print(random.choice(text['unknown'][1]))

main()