#추천시스템을 만들기 위한 전처리 과정

import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./reviews_kinolights.csv')
df.info()

df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords + ['영화', '감독', '연출', '배우','연기','작품','관객','장면']

okt = Okt()
cleaned_sentences = []

for review in df.reviews:
    review = re.sub('^가-힣', ' ',review) #리뷰에서 한글만 남기고 나머지 삭제하고 그자리를 띄어쓰기로 빈칸으로 만듬
    tokened_review = okt.pos(review, stem=True)  #형태소를 추출해주고 pos는 품사태깅까지 해줌
    #review: 형태소를 추출하고 품사 태깅할 대상인 한글 텍스트입니다.
    #stem=True: 형태소 분석 시 어간 추출을 수행합니다. 어간 추출은 단어의 기본 형태를 추출하는 과정입니다.
    #간 추출은 단어에서 접사 등을 제거하여 어간을 추출하는 과정입니다. 이를 통해 단어의 기본 형태를 파악할 수 있습니다.
    #품사태깅은 주어진 단어에 대해 그것이 어떤 품사에 속하는지를 태깅하는 작업입니다. 명사, 동사, 형용사 등 단어의 문법적 역할을 나타내는 정보를 부착합니다.
    #어미가 없어지지 않는건 명사와 동사같은거에만 어간추출이됨 아름답다같은 형용사는 아름답다 이렇게 나옴
    print(tokened_review)
    df_token = pd.DataFrame(tokened_review, columns=['word','class'])
    #tokened_review: 형태소 분석 및 품사 태깅 결과가 담긴 리스트입니다
    #columns=['word', 'class']: DataFrame의 열 이름을 'word'와 'class'로 설정합니다.
    df_token = df_token[(df_token['class']=='Noun')|
                        (df_token['class']=='Adjective')|
                        (df_token['class']=='Verb')] #Noun과 Adje와 Verb품사만 남긴다
    words = []
    for word in df_token.word:
        if 1<len(word):
            if word not in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    #' '.join(words): 리스트의 각 요소들을 공백을 이용하여 하나의 문자열로 결합합니다.
    #예를 들어, words가 ['I', 'love', 'Python']라면, cleaned_sentence에는 'I love Python'이 할당됩니다.
    cleaned_sentences.append(cleaned_sentence)
df['reviews'] = cleaned_sentences
df.dropna(inplace=True)
df.to_csv('./cleaned_reviews.csv',index=False)

print(df.head())
df.info()

df=pd.read_csv('./cleaned_reviews.csv')
df.dropna(inplace=True)
df.info()
df.to_csv('./cleaned_reviews.csv',index=False)



