import csv

import jieba


def cut(text):
    token_list = jieba.cut(text)
    # 加载停用词列表，包含标点符号
    stopwords = ['，', '。', '！', '(', ')', '的', '与']
    # 去除停用词（标点符号）
    filtered_words = [word for word in token_list if word not in stopwords]
    return filtered_words


if __name__ == '__main__':
    # 公共通信
    csv_file = 'info/公共通信.csv'  # CSV 文件路径

    # 创建一个空的字符串数组
    tongxin = []
    tongxin_tokens = []

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # 将每行数据作为字符串添加到数组中
            tongxin.append(','.join(row))

    # 打印字符串数组
    for item in tongxin:
        token_list = cut(item)
        tongxin_tokens.extend(token_list)

    for word in tongxin_tokens:
        print(word)

    csv_file = '../../output/company/公共通信.csv'  # 输出的 CSV 文件路径

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 添加标记行
        writer.writerow(['token'])
        for word in tongxin_tokens:
            writer.writerow([word])
