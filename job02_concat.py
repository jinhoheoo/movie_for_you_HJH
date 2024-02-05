#데이터들 모두 모아서 하나로 만들어주는거임 어려울거 없음
import pandas as pd
import glob

data_paths = glob.glob('./crawling_data/*')
print(data_paths)

df = pd.DataFrame()

for path in data_paths:
    df_temp = pd.read_csv(path)     #csv파일 읽어오고
    df_temp.dropna(inplace=True)    #nan빼줌
    df_temp.columns=['titles','reviews']
    df = pd.concat([df, df_temp],ignore_index=True)   #합침, 인덱스는 무시

df.drop_duplicates(inplace=True)  # 중복있으면 제거
df.info()
df.to_csv('./reviews_kinolights.csv',index=False)


