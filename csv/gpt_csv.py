import csv
import json

import pandas as pd
import requests

# 读取CSV文件
df = pd.read_csv('all_test_output_1.csv')
# 将结果写入CSV文件
output_file = 'all_test_output_2.csv'

# 定义API请求的URL和头部信息
url = "https://api.openai-sb.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer XXX",
    "Content-Type": "application/json"
}

hangye = ['云计算数据中心', '网络安全', '电力', '石油', '煤炭', '银行', '保险', '证券', '汽车', '半导体', '科研院校',
          '医院', '事业单位', '中央', '省部级', '厅局级', '县处级', '航空', '航天', '船舶', '核工业', '公共通信',
          '信息服务', '能源', '资源', '交通', '水利', '金融', '民用制造业', '公共服务', '党政机关', '国防科技工业']
# 创建一个空的结果列表
results = []

# 定义需要处理的行数范围
order_start = 21
order_end = 70000


def process():
    # 逐行处理CSV文件
    for index, row in df.iterrows():

        order = row['order']  # 获取order字段
        asn_description = row['asn_description']  # 获取asn_description字段作为content字段的值
        count = row['count']  # 获取count字段
        name = row['name']  # 获取name字段
        industry = row['industry']  # 获取industry字段

        if order < order_start:
            # 如果order小于order_start,则维持原样输出
            results.append([order, asn_description, count, name, industry])
        elif order > order_end:
            break
        else:
            asn_description = row['asn_description']  # 获取asn_description字段作为content字段的值
            count = row['count']  # 获取count字段

            content = "你擅长信息检索,尤其是公司名称识别\n"
            content += "你的任务是根据给出的公司英文名称,给出该公司的中文名称name,以及公司所属的行业industry\n"
            content += "现给出公司名称:"
            content += asn_description
            content += "\n"
            content += "所属行业枚举必须是数组其中之一[" + ', '.join(hangye) + "]\n"
            content += "我要求你做结构化输出,你的输出必须是json格式,有两个字段name,industry\n,除json外禁止包含其他任何字符\n"
            content += "输出: 纯文本输出,除了json结构体之外禁止包含其他任何字符,禁止包含任务markdown语言\n"
            content += "json结构体中的name,industry字段的值禁止包含任何符号,只保留纯文本\n"

            # 构建API请求的数据
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            }

            # 发起HTTP请求
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()

            # 提取结果中的content字段
            assistant_message = response_data['choices'][0]['message']['content']

            try:
                # 解析JSON字符串
                data = json.loads(assistant_message)
                # 提取"name"和"industry"字段
                name = data["name"]
                industry = data["industry"]
                # 将解析结果添加到结果列表中
                results.append([order, asn_description, count, name, industry])
            except Exception as e:
                # 在这里处理异常情况下的逻辑
                print("JSON解析异常:", e)
                print("异常字符串:", assistant_message)
                print("异常行号:", order)
                # 将解析结果添加到结果列表中
                results.append([order, asn_description, count, "", ""])

        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['order', 'asn_description', 'count', 'name', 'industry'])  # 写入表头
            writer.writerows(results)  # 写入数据
            print("已写入" + output_file)

    print("处理完成,从第" + str(order_start) + "行到第" + str(order_end) + "行的结果已保存到文件: " + output_file)


if __name__ == '__main__':
    process()
