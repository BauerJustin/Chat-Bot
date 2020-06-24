# Required imports
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random, string, nltk, numpy as np
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

def greeting_response(text, sentences):
    text = text.lower()

    bot_greetings = ['Hello There!', 'hi', 'hey', 'hola']
    user_greetings = ['hi', 'hey', 'hello', 'hola', 'greetings', 'wassup']

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
    
    bot_unknown = ['Sorry, I don\'t understand.', 'I\'m confused.', 'Try again.', 'Please ask again.']

    if response_flag == 0:
        bot_response = bot_response+' '+random.choice(bot_unknown)

    sentences.remove(user_input)

    return bot_response

print("Bot: Hello There! I am your friendly chat bot.")
print("Bot: I can answer your questions about whatever article you want!")
print("Bot: Type bye to exit.")
url = input("Bot: Paste a website you would like me to search: ")
sentence_list = get_article(url)

user_bye = ['exit', 'bye', 'see you later', 'quit', 'cya']
bot_bye = ['Bye for now!', 'Cya later alligator!', 'Byeeeeee :(', 'Talk to you later!', 'Please come back!', 'Ok, I see how it is...', 'Fine, get out!']

while(True):
    user_input = input()
    if len(user_input) > 1:
        if user_input.lower() in user_bye:
            print(random.choice(bot_bye))
            break
        else:
            if greeting_response(user_input, sentence_list) != None:
                print("Bot: "+greeting_response(user_input, sentence_list))
            else:
                print("Bot: "+bot_response(user_input, sentence_list))