import sys
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib
import matplotlib.pyplot as plt

# 반복되는 부분과 검색어로 추출되는 부분들을 분리하여 변수화 함
URL_BEFORE_KEYWORD = "https://www.joongang.co.kr/search/news?keyword="
URL_BEFORE_PAGE_NUM = "&page="

font_name = 'Malgun Gothic'

def get_link(key_word, page_range):
    link = list()

    for page in range(page_range):
        current_page = 1 + page
        crawling_url_list = URL_BEFORE_KEYWORD + key_word + URL_BEFORE_PAGE_NUM + str(current_page)

        response = requests.get(crawling_url_list)
        soup = BeautifulSoup(response.text, 'lxml')

        url_tag = soup.select('ul.story_list > li.card > div.card_body > h2.headline > a')

        for url in url_tag:
            link.append(url['href'])

    return link

def get_article(link):
    content = list()
    for page in range(len(link)):
        response1 = requests.get(link[page])
        soup = BeautifulSoup(response1.text, 'lxml')

        url_title = soup.select('h1.headline')
        url_tag1 = soup.select('div#article_body > p')

        content.append(url_title)
        content.append(url_tag1)

    return content

def wordcount(content):
    string = str(content)
    engine = Okt()
    all_nouns = engine.nouns(string)
    nouns = [n for n in all_nouns if len(n) > 1]

    global count, by_num

    count = Counter(nouns)
    by_num = OrderedDict(sorted(count.items(), key=lambda t: t[1], reverse=True))

    word = [i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    return word, number


def full_vis_bar(word, number):

    word20 = word[:20]
    number20 = number[:20]

    fig = plt.gcf()
    fig.set_size_inches(20,10)
    matplotlib.rc('font', family=font_name, size=10)
    plt.title("전체 단어 빈도 수", fontsize=20)
    plt.xlabel('단어', fontsize=20)
    plt.ylabel('개수', fontsize=20)
    plt.bar(word20, number20, color='#6799FF')
    plt.xticks(rotation=90)
    plt.savefig('all_words.jpg')
    plt.show()



def main(argv):
    # if len(argv) != 3:
    #     print("인자 값을 정확히 입력하세요")
    #     return

    # file1 = "crawling1.txt"
    # file2 = "wordcount1.txt"
    # file3 = "top20.txt"

    # 0은 파일명을 의미한다. 그래서 1부터 시작
    key_word = input(str("검색어를 입력하세요 : "))
    page_range = input(str("페이지를 입력하세요 : "))
    link = get_link(key_word, int(page_range))
    content = get_article(link)
    word, number = wordcount(content)
    full_vis_bar(word, number)
    print(word)
    print(number)

    # full_vis_bar(word20, number20)
    # get_article(file1, link, key_word, page_range)
    # wordcount(file1, file2)
    # # full_vis_bar(by_num)
    # top_n(file2, file3)
    # print(link)
    # print(content)
    # print(len(link))
    # print(len(content))

if __name__ == '__main__':
    main(sys.argv)