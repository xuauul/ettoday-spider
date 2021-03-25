import json
import time
import argparse
import datetime
import requests

from tqdm import tqdm
from bs4 import BeautifulSoup

class EttodaySpider:
    def __init__(self, tags):
        self.tags = tags
        self.base_url = "https://www.ettoday.net"

    def run(self, start_date, end_date):
        """
            generate "data/start_date-end_date.txt" :
            record news contents for a given date range.
        """

        filename = "data/%s-%s.txt" % (''.join(start_date.split('/')), ''.join(end_date.split('/')))
        links = self.get_news_list(start_date, end_date)

        with open(filename, 'w', encoding="utf-8") as fout:
            for url, tag, date in tqdm(links):
                title, content = self.get_one_page_content(url)
                if title == None or content == None: continue
                data = {"tag": tag, "date": date, "title": title, "content": content}
                fout.write(json.dumps(data, ensure_ascii=False) + '\n')

                # prevent getting blocked
                time.sleep(0.5)

    def get_news_list(self, start_date, end_date):
        """ get a list of news links for a given date range. """

        links = list()
        for date in self.get_date_range(start_date, end_date):
            for tag in self.tags.keys():
                page = self.base_url + "/news/news-list-%s-%s-%s-%s.htm" % (*date.split('/'), tag)
                soup = BeautifulSoup(requests.get(page).content, "html.parser")

                for news in soup.select("div.part_list_2 > h3"):
                    news_date = news.span.string.split()[0]
                    if news_date != date: break
                    links.append((news.a["href"], self.tags[tag], news_date))
        return links

    def get_date_range(self, start_date, end_date):
        """" generate a list of date for a given date range. """

        start = datetime.datetime.strptime(start_date, "%Y/%m/%d")
        end = datetime.datetime.strptime(end_date, "%Y/%m/%d")
        return [(start + datetime.timedelta(days=x)).strftime("%Y/%m/%d")
                for x in range(0, (end - start).days + 1)]

    def get_one_page_content(self, url):
        """ get a news content from a given url. """

        page = self.base_url + url
        soup = BeautifulSoup(requests.get(page).content, "html.parser")

        try:
            title = soup.select_one("h1.title").string
            content = [p.string for p in soup.select("div.story > p")
                        if p.find(text=True, recursive=False)]
        except:
            title, content = None, None

        return title, content


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=str)
    parser.add_argument("--end", type=str)
    args = parser.parse_args()

    # all tags in the ettoday menu
    tags = {"1": "政治", "2": "國際", "3": "大陸", "4": "新奇", "5": "生活", "6": "社會", "7": "地方", "8": "寵物", "9": "影劇", "10": "體育", "11": "旅遊", "12": "消費", "13": "論壇", "15": "名家", "17": "財經", "18": "ET來了", "20": "3C家電", "21": "健康", "22": "男女", "23": "公益", "24": "遊戲", "26": "網搜", "28": "電影", "30": "時尚", "31": "購物雲", "32": "親子", "33": "房產雲", "34": "ET車雲", "35": "軍武", "36": "保險", "38": "法律", "39": "直銷", "40": "探索", "41": "電競", "43": "行銷雲"}

    spider = EttodaySpider(tags)
    spider.run(args.start, args.end)
