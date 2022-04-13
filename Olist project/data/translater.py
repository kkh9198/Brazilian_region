#%%
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import RSLPStemmer #Stemmer for portugese words.

from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest

import pandas as pd
import matplotlib.pyplot as plt
import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from googletrans import Translator

#%%
order_reviews_dataset = pd.read_csv('olist_order_reviews_dataset.csv')

#널값을 빈값으로 변경
order_reviews_dataset['review_comment_title'] = order_reviews_dataset['review_comment_title'].fillna('')
order_reviews_dataset['review_comment_message'] = order_reviews_dataset['review_comment_message'].fillna('')

#%%
stop = stopwords.words('portuguese')
stop.append('nao') #Stopword already have "Não", just adding this because it's appear on dataframe

text_review_1 = ' '.join(order_reviews_dataset[order_reviews_dataset["review_score"]==1]["review_comment_message"])
text_review_2 = ' '.join(order_reviews_dataset[order_reviews_dataset["review_score"]==2]["review_comment_message"])
text_review_3 = ' '.join(order_reviews_dataset[order_reviews_dataset["review_score"]==3]["review_comment_message"])
text_review_4 = ' '.join(order_reviews_dataset[order_reviews_dataset["review_score"]==4]["review_comment_message"])
text_review_5 = ' '.join(order_reviews_dataset[order_reviews_dataset["review_score"]==5]["review_comment_message"])

def resumo (texto,n):
    sentencas = sent_tokenize(texto)
    palavras = word_tokenize(texto.lower())
    
    stop = set(stopwords.words('portuguese') + list(punctuation))
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stop]
    
    frequencia = FreqDist(palavras_sem_stopwords)
    sentencas_importantes = defaultdict(int)
    
    for i, sentenca in enumerate(sentencas):
        for palavra in word_tokenize(sentenca.lower()):
            if palavra in frequencia:
                sentencas_importantes[i] += frequencia[palavra]
                
    idx_sentencas_importantes = nlargest(n, sentencas_importantes, sentencas_importantes.get)
    for i in sorted(idx_sentencas_importantes):
        print(sentencas[i])    

translator = Translator()

def visualize(label):
    words = ''
    i = 0
    mapColor = ''

    #매개변수에 따라서 색 변경
    if label == 5:
        mapColor = 'PuBu'
    elif label == 4:
        mapColor = 'YlGnBu'
    elif label == 3:
        mapColor = 'Wistia'
    elif label == 2:
        mapColor = 'YlOrRd'
    elif label == 1:
        mapColor = 'Reds'
        
    for msg in order_reviews_dataset[order_reviews_dataset['review_score'] == label]['review_comment_message']:
        if(msg != ''):
            try:
                msg = translator.translate(msg, src='pt', dest='en').text
                msg = msg.lower()
            except:
                pass
            
            
        print(f"{i} : {msg}")
        words += msg + ' '

        #횟수 제한
        if(i == 2000):
            break
        i += 1

    file_name = "review_score_" + str(label) + ".txt"
    f = open(file_name, 'w', encoding='UTF-8')
    f.write(words)
    f.close()
    wordcloud = WordCloud(width=600, height=400, colormap=mapColor).generate(words)
    plt.figure(figsize=(12,8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show() 