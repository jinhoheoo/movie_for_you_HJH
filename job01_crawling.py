#영화 리뷰 조사해서 추천하는 시스템 만들어줄꺼임.

from selenium import webdriver  #pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager  #pip install webdriver_manager
from selenium.common.exceptions import NoSuchElementException   #페이지 잘 안켜지면 오류로 취급할 수 있음
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#이거 어디서 가져오냐면 저 사이트 들어가서 검사 누른후 네트워크들어간후 새로고침 하면 많이 뜨는데 거기서 header 들어가서
#젤 아래로 들어가면 user-agent있음 그거 긁어온거임
options.add_argument('user_agent='+ user_agent)
options.add_argument('lang=ko_KR')
# options.add_argument('headless')#이거 하면 페이지 들어가서 어디 긁어오는지 안보임
# 유튜브같은건 브라우저의 크기를 줄이면 한번에 나타나는게 달라지고 그런데 이런걸 반응형이라고함.
# 검사들어가서 기기변환 눌러보면 모바일용, pc용 이렇게 볼수 있음 oc에서는 4개 모바일에서는 2개 이런게 반응형임
options.add_argument('window-size=1920X1080')#이렇게 하면 반응형일 때 사이즈 고정해서 문제해결함.

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

#Xpath는 버튼같이 누르고 싶은거 검사로해서 누르고 xpath copy로 가져오면 됨.
start_url="https://m.kinolights.com/discover/explore"
button_movie_tv_xpath = '//*[@id="contents"]/section/div[3]/div/div/div[3]/button'  #이렇게하면 영화 버튼의 xpath 가져와짐
button_movie_xpath = '//*[@id="contents"]/section/div[4]/div[2]/div[1]/div[3]/div[2]/div[2]/div/button[1]'
button_ok_xpath = '//*[@id="applyFilterButton"]'
driver.get(start_url)
time.sleep(2)

button_movie_tv = driver.find_element(By.XPATH, button_movie_tv_xpath) #위에서 적은 Xpath로 영화 버튼 찾음
driver.execute_script('arguments[0].click();',button_movie_tv)
# 자바스크립트로 버튼이 코딩되어 있어서 그냥 .click이나 enter 말고 이렇게 해야함
time.sleep(0.5)

button_movie = driver.find_element(By.XPATH, button_movie_xpath) #위에서 적은 Xpath로 영화 버튼 찾음
driver.execute_script('arguments[0].click();',button_movie)
# 자바스크립트로 버튼이 코딩되어 있어서 그냥 .click이나 enter 말고 이렇게 해야함
time.sleep(1)
#이렇게 되면 사이트 들어가서 영화/tv누르고 거기서 영화까지누르게됨. 이제 필터적용까지 누르면됨.

button_ok = driver.find_element(By.XPATH, button_ok_xpath) #위에서 적은 Xpath로 영화 버튼 찾음
driver.execute_script('arguments[0].click();',button_ok)
# 자바스크립트로 버튼이 코딩되어 있어서 그냥 .click이나 enter 말고 이렇게 해야함


for i in range(25):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1)

list_review_url = []
movie_titles = []
for i in range(1, 700):
    base = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/a').get_attribute("href")
    #XPATH를 사용하여 웹 페이지에서 해당 링크를 찾고, 찾은 링크의 href 속성 값을 base에 저장합니다.
    #영화 검사로 클릭해보면 <a data-v 뭐 이런식으로 a적혀있는 a태그가 있는데 그거를 클릭하고 xpath가져오고 뒤에 href저거 적어주면 영화 클릭해서 들어가진곳의 주소가 가져와짐
    #href는 HTML에서 하이퍼링크의 속성(attribute) 중 하나입니다. HTML 문서에서 <a> 태그를 사용하여 링크를 생성할 때, 해당 링크의 대상 URL을 지정하는 데 사용됩니다.
    #<a> 태그는 HTML에서 "앵커(Anchor)" 태그로 불리며, 하이퍼링크를 생성하는 데 사용됩니다. 이 태그는 웹 페이지에서 다른 웹 페이지로 이동하거나, 같은 페이지 내의 특정 위치로 스크롤할 수 있는 링크를 만들 때 주로 사용됩니다.
    #//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/a 이게 a태그의 xpath임
    list_review_url.append(f"{base}/reviews")
    #이거는 저 영화 들어가서 거기에 리뷰 거기로 들어가는 주소 리스트에 추가해주는거임.
    #이걸 바탕으로 리뷰 긁어오면 됨.
    title = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/div/div[1]').text
    #영화 이름 이나 리뷰같은 텍스트 가져올 때도 이런식으로 xpath로 텍스트 클릭해서 가져오면 됨. 뒤에 text붙이면 text 저장됨.
    movie_titles.append(title)

print(list_review_url[:5])
print(len(list_review_url))
print(movie_titles[:5])
print(len(movie_titles))


reviews = []
for idx, url in enumerate(list_review_url[551:600]):
    driver.get(url)
    time.sleep(1)
    review = ''
    for i in range(1, 31):
        # 리뷰 내용에 더보기 있으면 더보기들어가서 리뷰내용 가져올려고하고 더보기 없으면 리뷰 타이틀만 가져옴
        # 각각의 리뷰 하나하나 xpath로 접근해서 가져오니 더보기로 back으로 뒤로가기해서 다시 순서진행함
        review_title_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/a[1]/div'.format(i)
        review_more_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/div/button'.format(i)
        try:
            review_more = driver.find_element(By.XPATH, review_more_xpath)
            driver.execute_script('arguments[0].click();', review_more)
            time.sleep(1)
            review_xpath = '//*[@id="contents"]/div[2]/div[1]/div/section[2]/div/div'
            review = review + ' ' + driver.find_element(By.XPATH, review_xpath).text
            driver.back()    #이걸로 더보기 들어간후 뒤로가기해서 다시 기본리뷰로감
            time.sleep(1)   #뒤로가기하고 페이지 뜰때까지 조금 기다려줌.

        except NoSuchElementException as e: #더보기가 없을때 일어나는 에러
            print('더보기',e)
            try:

                review = review + ' ' + driver.find_element(By.XPATH, review_title_xpath).text
            # 더보기 누르려했는데 없어서 뒤로가서 긁으려했는데 리뷰개수가 부족해서 안긁히면 에러발생함
            #여기서 에러가 나면 젤 마지막 except으로 가서 에러 처리함
        # 더보기 없을때 오류발생으로해서 그냥 리뷰타이틀 텍스트 가져오게함.
            except:
                print('review title error')
        except StaleElementReferenceException as e: #아예 검색할 대상이 없을때 발생하는 에러
            print('stale',e)
            time.sleep(1)

        except: #그외 모든 에러
            print('error')

    print(review)
    reviews.append(review)
print(reviews[:5])
print(len(reviews))

df = pd.DataFrame({'titles':movie_titles[551:600], 'reviews':reviews})
today = datetime.datetime.now().strftime('%Y%m%d')
df.to_csv('./crawling_data/reviews_600.csv', index=False)


