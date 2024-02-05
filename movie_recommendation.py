import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec

def getRecommendation(cosine_sim):  #코사인 유사도 값을 받아서 처리하는 함수 #유사한 순으로 정렬함.
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)    #코사인값 큰거부터 정렬
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recmovieList = df_reviews.iloc[movieIdx,0] #0은 영화제목을 받아서 리턴하려고
    return recmovieList[1:11]  #자기자신인 첫번째꺼 제외하고 그다음 10개를 보기위해 11을 적음

df_reviews = pd.read_csv('./cleaned_one_review.csv')
# df_reviews = pd.read_csv('./cleaned_reviews.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)


# #영화 인덱스 기준으로 유사한 문장인거를 찾아 추천해주는거임 즉 job05을 이용한거임
# ref_idx = 10 #원하는 열 선택하는거임 즉 원하는 영화 선택하면 됨.
# print(df_reviews.iloc[ref_idx,0])
# cosin_sim = linear_kernel(Tfidf_matrix[ref_idx], Tfidf_matrix)
# print(cosin_sim[0])
# print(len(cosin_sim))
# recommendation = getRecommendation(cosin_sim)
# print(recommendation) #유사한 순서 10개 추천해준걸 보여줌

#영화 인덱스가 아닌 단어인 키워드를 기준으로 찾아 추천해주는거임 즉 job07을 이용함
embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
keyword = '드래곤'
sim_word = embedding_model.wv.most_similar(keyword, topn=10)
words = [keyword]
for word, _ in sim_word:
    words.append(word)
sentence = []
count = 10
for word in words:
    sentence = sentence + [word] * count
    count -= 1
sentence = ' '.join(sentence)
print(sentence)
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)

print(recommendation)