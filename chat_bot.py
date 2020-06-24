# Required imports
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from time import sleep
import sys
import random
import string
import nltk
import numpy as np
nltk.download('punkt', quiet=True)

# Bot and user text
bot_greetings = ['Hello There!', 'hi', 'hey', 'hola']
user_greetings = ['hi', 'hey', 'hello', 'hola', 'greetings', 'wassup']

bot_unknown = ['Sorry, I don\'t understand.', 'I\'m confused.', 'Try again.', 'Please ask again.']

user_bye = ['exit', 'bye', 'see you later', 'quit', 'cya']
bot_bye = ['Bye for now!', 'Cya later alligator!', 'Byeeeeee :(', 'Talk to you later!', 'Please come back!', 'Ok, I see how it is...', 'Fine, get out!']


def get_article(url):
    # Get website from user, download and parse it to apply Natural Language Processing
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    # Create a list of sentences from article text
    sentences = nltk.sent_tokenize(article.text)
    return sentences

def greeting_response(text, sentences):
    text = text.lower()

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

def index_sort(score_list):
    length = len(score_list)
    list_index = list(range(0,length))

    x = score_list
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    
    return list_index

def bot_response(user_input, sentences):
    user_input = user_input.lower()
    sentences.append(user_input)
    bot_response = ""
    cm = CountVectorizer().fit_transform(sentences)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response+' '+sentences[index[i]]
            response_flag = 1
            j += 1
        if j > 2:
            break

    if response_flag == 0:
        bot_response = bot_response+' '+random.choice(bot_unknown)

    sentences.remove(user_input)

    return bot_response

def bot_print(text):
    text += "\n"
    sys.stdout.write("Bot: ")
    sys.stdout.flush()
    for char in text:
        sleep(0.03)
        sys.stdout.write(char)
        sys.stdout.flush()

def begin_convo():
    bot_print("Hello There! I am your friendly chat bot.")
    bot_print("I can answer your questions about whatever article you want!")
    bot_print("Type bye to exit.")
    bot_print("Paste a website you would like me to search: ")
    url = input()
    return get_article(url)

def main():
    sentence_list = begin_convo()
    bot_print("Done! Ask me your questions.")
    while(True):
        user_input = input()
        if len(user_input) > 1:
            if user_input.lower() in user_bye:
                bot_print(random.choice(bot_bye))
                break
            else:
                if greeting_response(user_input, sentence_list) != None:
                    bot_print(greeting_response(user_input, sentence_list))
                else:
                    bot_print(bot_response(user_input, sentence_list))

main()