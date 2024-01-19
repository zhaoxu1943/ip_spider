import json

import pandas as pd


def test():
    # 读取文件
    with open('C:/Users/46315/Desktop/ce.txt', 'r', encoding="UTF-8") as file:
        data = file.readlines()
    # 解析JSON并提取asn_description字段
    asn_descriptions = []
    for line in data:
        json_data = json.loads(line)
        asn_description = json_data.get('asn_description')
        if asn_description:
            asn_descriptions.append(asn_description)
    # 去重
    unique_asn_descriptions = list(set(asn_descriptions))
    # 创建DataFrame保存结果
    output_df = pd.DataFrame({'asn_description': unique_asn_descriptions})
    # 将结果保存为CSV文件
    output_df.to_csv('output.csv', index=False)


if __name__ == '__main__':
    test()
