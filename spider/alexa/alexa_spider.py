# encoding:utf-8
import requests
from bs4 import BeautifulSoup


def execute_spider(para_url, para_headers, para_session):
    # 发起request
    req = para_session.get(para_url, headers=para_headers)
    # 解析返回内容
    bs_obj = BeautifulSoup(req.text, 'html.parser')

    origin_rank_list = bs_obj.findAll("div", {"class": "rank-index"})
    origin_link_list = bs_obj.findAll("span", {"class": "domain-link"})

    # 格式化后的排名和链接
    format_rank_list = []
    format_link_list = []

    for rank in origin_rank_list:
        format_rank_list.append(rank.string.encode('utf-8').decode())

    for link in origin_link_list:
        format_link_list.append(link.a['href'].encode('utf-8').decode())

    return format_rank_list, format_link_list


rank_list = []
link_list = []

if __name__ == '__main__':

    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
               "Accept": "*/*"}
    # 左闭右开!
    for i in range(1, 101):
        if i == 1:
            url = "http://www.alexa.cn/siterank/"
        else:
            url = "http://www.alexa.cn/siterank/" + str(i)

        format_rank_list, format_link_list = execute_spider(url, headers, session)
        rank_list += format_rank_list
        link_list += format_link_list

wf = open('../../output/web/alexa.csv', 'w')
wf.write('rank,link\n')
for i in range(len(rank_list)):
    wf.write('%s,%s\n' % (rank_list[i], link_list[i]))
wf.close()
print('ok')
