# TF는 특정 문서 내에서의 상대적인 빈도를 나타내며, DF는 여러 문서에서의 등장 여부를 나타냅니다.
# 이 두 지표를 사용하여 TF-IDF (Term Frequency-Inverse Document Frequency)를 계산할 수 있습니다.
# TF (Term Frequency): Term Frequency는 단어가 문서 내에서 얼마나 자주 등장하는지를 나타내는 지표입니다.
# 특정 단어의 등장 횟수를 해당 문서의 전체 단어 수로 나눈 값으로 계산됩니다.
# DF (Document Frequency): Document Frequency는 특정 단어가 몇 개의 문서에서 등장했는지를 나타내는 지표입니다.
# 특정 단어가 여러 문서에서 자주 등장하면 그 단어의 DF는 높아집니다.

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle
#
# TF-IDF (Term Frequency-Inverse Document Frequency)를 사용하여 텍스트 데이터를 벡터화하고,
# 그 결과를 저장하는 과정입니다. 각 단어의 TF-IDF 값을 계산하고 이를 희소 행렬로 저장합니다
# TF (Term Frequency - 단어 빈도): 각 문서에서 각 단어가 얼마나 자주 나타나는지 계산합니다. 이는 특정 단어의 등장 횟수를 해당 문서의 전체 단어 수로 나눈 값입니다.
# IDF (Inverse Document Frequency - 역문서 빈도): 전체 문서에서 특정 단어가 얼마나 자주 나타나는지 계산합니다. 이는 특정 단어가 나타난 문서의 수를 전체 문서 수로 나눈 후 로그를 취한 값입니다.
# TF-IDF 값 계산: TF와 IDF 값을 곱하여 TF-IDF 값을 얻습니다. 이는 특정 단어가 특정 문서에서 얼마나 중요한지를 나타내는 값입니다.
# 희소 행렬로 저장: 계산된 TF-IDF 값을 희소 행렬(Sparse Matrix) 형태로 저장합니다. 희소 행렬은 대부분의 값이 0인 행렬이지만, 중요한 값을 포함한 위치만 저장하여 메모리를 효율적으로 사용합니다.
# 희소 행렬(Sparse Matrix)은 대부분의 원소가 0인 행렬을 말합니다. 희소 행렬은 매우 큰 행렬에서 0이 아닌 값이 들어있는 원소의 위치만을 저장하여 메모리를 효율적으로 사용할 수 있게 해줍니다.
#(0, 0) 1 희소행렬은 이런식으로 저장하는데 0,0에 1이라는 값이 들어있다는거를 의미함.
#(0, 2) 2
#(1, 1) 3

df_reviews = pd.read_csv('./cleaned_one_review.csv')
# df_reviews = pd.read_csv('./cleaned_reviews.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
#TF-IDF 변환을 수행할 TfidfVectorizer 객체를 생성합니다. sublinear_tf=True는 TF를 로그 스케일로 변환합니다.
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])
#reviews' 열의 텍스트 데이터를 이용하여 TF-IDF 행렬을 계산합니다.
print(Tfidf_matrix.shape)

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)
#TfidfVectorizer 객체를 pickle 파일로 저장합니다.
mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)
#계산된 TF-IDF 행렬을 Matrix Market 형식으로 저장합니다.