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
                # time.sleep(0.5)

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
                        if p.find(text=True, recursive=False) and p.string]
        except:
            title, content = None, None

        return title, content


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=str)
    parser.add_argument("--end", type=str)
    args = parser.parse_args()

    # all tags in the ettoday menu
    tags = {"1": "??????", "2": "??????", "3": "??????", "4": "??????", "5": "??????", "6": "??????", "7": "??????", "8": "??????", "9": "??????", "10": "??????", "11": "??????", "12": "??????", "13": "??????", "15": "??????", "17": "??????", "18": "ET??????", "20": "3C??????", "21": "??????", "22": "??????", "23": "??????", "24": "??????", "26": "??????", "28": "??????", "30": "??????", "31": "?????????", "32": "??????", "33": "?????????", "34": "ET??????", "35": "??????", "36": "??????", "38": "??????", "39": "??????", "40": "??????", "41": "??????", "43": "?????????"}

    spider = EttodaySpider(tags)
    spider.run(args.start, args.end)
