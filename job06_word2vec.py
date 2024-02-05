# #단어를 벡터로 만들어 주는거임. 좌표로 만든다는거임. 여기서 벡터는 의미공간상의 좌표임
# #단어 의미를 학습시키려함.
# #비슷한 의미를 가진 단어는 비슷한 위치에 위치할거임. 사전적의미말고 연상단어 말하는듯
# #의미를 학습한 형태소들을 나타나게됨
#
# import pandas as pd
# from gensim.models import Word2Vec
#
# df_review = pd.read_csv('./cleaned_reviews.csv')
# df_review.info()
#
# reviews = list(df_review['reviews'])
# print(reviews[0])
#
# tokens = []
# for sentence in reviews:
#     token = sentence.split()
#     tokens.append(token)
# print(tokens[0])
#
# #임베딩은 단어나 문장의 의미를 보존하면서 모델이 이해할 수 있는 형태로 변환합니다.
# # 이렇게 수치적으로 나타낸 단어 벡터는 의미적 유사성을 보존하므로, 비슷한 의미를 가진 단어들은 벡터 공간 상에서 가까이 위치하게 됩니다.
# # "king - man + woman" 연산을 수행하면 "queen"에 가까운 결과가 나오는 등 단어 간의 의미적 관계를 임베딩 벡터 공간에서 산술적으로 표현할 수 있습니다.
# #임베딩은 주로 자연어 처리 작업에서 모델의 입력으로 활용되며, 텍스트 데이터의 특성을 수치화하여 모델이 학습하고 이해하는 데 도움을 줍니다.
# embedding_model = Word2Vec(tokens, vector_size=100, window=4, min_count=20, workers=4,epochs=100, sg=1)
# #vector_size=100은 embedding에서 차원이 커지면 차원의 저주로 제대로된 학습이 안되서 100으로 차원을 줄인거임.
# #min_count=20 최소 20이상 출연하지 않는 단어는 학습하지 않겠다는거임
# #worker=4 학습할 때 cpu4개 쓰겠다는 거임.
#
# #tokens: 이는 토큰화된 문장이나 문서의 목록이어야 합니다. 목록의 각 요소는 문장이나 문서를 나타내며 그 안의 단어는 토큰화되어 있어야 합니다.
# #vector_size: 이 매개변수는 단어 벡터의 차원을 지정합니다. 여기에서는 각 단어가 100차원의 벡터로 표현될 것입니다.
# #window: 현재 단어와 예측 단어 사이의 최대 거리를 정의합니다. window 매개변수는 모델이 임베딩을 학습할 때 고려할 문맥 창의 크기를 제어합니다. 여기서는 4로 설정되어 있으므로 모델은 문장에서 현재 단어 앞 뒤로 4개의 단어를 고려합니다.
# #min_count: 이 매개변수는 학습 중에 고려되는 최소한의 단어 빈도를 지정합니다. 이 값보다 적게 나타나는 단어는 무시됩니다. 여기서는 20으로 설정되어 있어 빈도가 20보다 적은 단어는 어휘에서 제외됩니다.
# #workers: 학습 중에 사용할 CPU 코어 수를 설정합니다. 여기서는 4로 설정되어 있으므로 학습은 네 개의 CPU 코어를 사용합니다.
# #epochs: 이는 전체 데이터 집합에 대한 반복(패스) 횟수입니다. 여기서는 100으로 설정되어 있어 모델은 데이터 집합 전체를 100번 반복합니다.
# #sg: 이 매개변수는 학습 알고리즘을 지정합니다. sg가 1이면 Skip-gram 모델을 사용하고 0이면 CBOW (Continuous Bag of Words)를 사용합니다. 여기서는 1로 설정되어 있으므로 Skip-gram 모델이 사용됩니다.
#
# embedding_model.save('./models/word2vec_movie_review.model')
# print(list(embedding_model.wv.index_to_key))
# print(len(embedding_model.wv.index_to_key))
import pandas as pd
from gensim.models import Word2Vec

df_review = pd.read_csv('./cleaned_one_review.csv')
df_review.info()

reviews = list(df_review['reviews'])
print(reviews[0])

tokens = []
for sentence in reviews:
    token = sentence.split()
    tokens.append(token)
print(tokens[0])

embedding_model = Word2Vec(tokens, vector_size=100, window=4,
            min_count=20, workers=4, epochs=100, sg=1)
embedding_model.save('./models/word2vec_movie_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))