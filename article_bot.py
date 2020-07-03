# Required imports
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import nltk
import json
nltk.download('punkt', quiet=True)

def get_article(url):
    # Get website from user, download and parse it to apply Natural Language Processing
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    # Create a list of sentences from article text
    sentences = nltk.sent_tokenize(article.text)
    return sentences

def is_article(user_input):
    # returns true if article
    return len(user_input) > 25 and not (' ' in user_input.strip())

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

def bot_article_response(user_input, sentences, text):
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