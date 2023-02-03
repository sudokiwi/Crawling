import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt

def plt_options():
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    timer = fig.canvas.new_timer(interval=10000)
    timer.add_callback(plt.close)
    timer.start()


key_word = input("수집할 키워드를 입력하세요: ")
page_range = int(input("수집할 페이지를 입력하세요: "))
font_name = 'Malgun Gothic'

first_url = "https://www.joongang.co.kr/search/news?keyword="
second_url = "&page="

link = list()

for page in range(page_range):
    current_page = page + 1  # 1 -> 2 -> 3 ...
    crawling_url_list = first_url + key_word + second_url + str(current_page)

    response = requests.get(crawling_url_list)
    soup = BeautifulSoup(response.text, 'lxml')

    url_tag = soup.select('h2.headline > a')

    for url in url_tag:
        link.append(url['href'])
print("기사 URL 추출 완료.")

count_link = list()
for i in link:
    response2 = requests.get(i)
    soup2 = BeautifulSoup(response2.text, 'lxml')

    content = soup2.select("div.article_body.fs3")
    for b in content:
        pure_content = b.text.strip()

        engine = Okt()
        nouns_by_article = engine.nouns(pure_content)
        nouns = [n for n in nouns_by_article if len(n) > 1]
        nouns_count = Counter(nouns)
        by_num = OrderedDict(sorted(nouns_count.items(), key=lambda t: t[1], reverse=True))
        word = [i for i in by_num.keys()]
        number = [i for i in by_num.values()]

        for w, n in zip(word, number):
            nouns_with_count = '{}\t{}'.format(w, n)
            count_link.append(nouns_with_count)

print("기사 본문과 내용 추출 및 단어 개수 처리 완료.")
refine_list = list()

for i in count_link:
    refine_list.append(i.replace("\t", " "))
# '아이유\t18' -> '아이유 18'
# '무대\t12' -> '무대 12'

dic = dict()
for test in refine_list:
    temp = test.split(' ')
    key = temp[0]
    value = int(temp[1])
    if key in dic:
        dic[key] = dic[key] + value
    else:
        dic[key] = value

sorted_list = sorted(dic.items(), key=lambda item: item[1], reverse=True)
graph_dic = dict(sorted_list[:20])

fig = plt.gcf()
fig.set_size_inches(20, 10)
matplotlib.rc('font', family=font_name, size=10)
plt.title('기사에 나온 전체 단어 빈도 수', fontsize=30)
plt.xlabel('기사에 나온 단어', fontsize=20)
plt.ylabel('기사에 나온 단어의 개수', fontsize=20)
plt.bar(graph_dic.keys(), graph_dic.values(), color='#DD78F6')
plt.savefig('joongang_top20.jpg')
plt_options()
plt.show()
print('joongang_top20.jpg 가 저장되었습니다.\n')