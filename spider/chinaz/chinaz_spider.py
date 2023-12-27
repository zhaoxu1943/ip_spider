# encoding:utf-8
import re

import requests
from bs4 import BeautifulSoup

pattern = r"(/Html/site_|/site_)(.*)(\.html)"


def execute_spider(para_url, para_headers, para_session):
    # 发起request
    req = para_session.get(para_url, headers=para_headers)
    # 解析返回内容
    bs_obj = BeautifulSoup(req.text, 'html.parser')

    origin_rank_list = bs_obj.findAll("div", {"class": "w90 col-red03 fz16"})
    origin_link_list = bs_obj.findAll("div", {"class": "w320 PCop"})

    # 格式化后的排名和链接
    format_rank_list = []
    format_site_list = []
    format_link_list = []

    for rank in origin_rank_list:
        format_rank_list.append(rank.string.encode('utf-8').decode())

    for link in origin_link_list:
        temp = link.find('a')
        text = temp.text.encode('utf-8').decode()
        format_text = text.replace('▪', '')
        href = temp['href'].encode('utf-8').decode()
        format_href = re.sub(pattern, r"\2", href)
        format_site_list.append(format_text)
        format_link_list.append(format_href)
    return format_rank_list, format_site_list, format_link_list


rank_list = []
site_list = []
link_list = []

if __name__ == '__main__':

    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
               "Accept": "*/*"}
    # 左闭右开!
    for i in range(1, 40):
        if i == 1:
            url = "https://top.chinaz.com/alltop/index.html"
        else:
            url = "https://top.chinaz.com/alltop/index_" + str(i) + ".html"

        format_rank_list, format_site_list, format_link_list = execute_spider(url, headers, session)
        rank_list += format_rank_list
        site_list += format_site_list
        link_list += format_link_list

wf = open('../../output/web/chinaz_page_100_utf8.csv', 'w')
wf.write('rank,name,link\n')
for i in range(len(rank_list)):
    wf.write('%s,%s,%s\n' % (rank_list[i], site_list[i], link_list[i]))
wf.close()
print('ok')
