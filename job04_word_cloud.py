#시각화 하려고 만듬
#wordcloud 패키지 사용함
import pandas as pd
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = './malgun.ttf'  #다양한 폰트가 들어있음
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic')    #malgun.ttf에 있는 다양한 font중 저걸 사용한다는거임.

df = pd.read_csv('./cleaned_one_review.csv')
# df = pd.read_csv('./cleaned_reviews.csv')
words = df.iloc[42, 1].split()
# iloc[11, 1]: DataFrame에서 11번째 행과 1번째 열에 해당하는 데이터를 가져옵니다.
# .split(): 가져온 문자열을 공백을 기준으로 분할하여 리스트로 만듭니다.
print(words)

worddict = collections.Counter(words) #단어가 몇번쓰였는지 세서 알려줘
worddict = dict(worddict) #그걸 딕셔너리 형태로 만들어 보기 편하게함.
print(worddict)

wordcloud_img = WordCloud(
    background_color='white', max_words=2000, font_path=font_path
    ).generate_from_frequencies(worddict)
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.show()