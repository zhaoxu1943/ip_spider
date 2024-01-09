import csv
import glob
import os

import jieba

import excel

# 来源目标路径
directory = 'info/'
# 获取目录下所有的CSV文件路径
csv_files = glob.glob(os.path.join(directory, '*.csv'))

output_directory = '../../output/company/'


def cut(text):
    # 使用精确模式对文本进行分词
    token_list = jieba.cut(text, cut_all=False)
    # 加载停用词列表，包含标点符号
    stopwords = ['，', '。', '！', '(', ')', '的', '与', '（', ' ', '）', '、', '；', '“', '”', '：', '《', '》', '？', '【', '】',
                 '……', 'of', '-']
    capital_cities = ["中国", "北京", "天津", "石家庄", "太原", "呼和浩特", "沈阳", "长春", "哈尔滨", "上海", "南京",
                      "杭州",
                      "合肥", "福州", "南昌",
                      "济南", "郑州", "武汉", "长沙", "广州", "南宁", "海口", "重庆", "成都", "贵阳", "昆明", "拉萨",
                      "西安", "兰州", "西宁",
                      "银川", "乌鲁木齐", "台北", "香港", "澳门"]
    stop_words2 = ["和", "的", "他", "她", "它", "们", "是", "在", "有", "我", "你", "他们", "我们", "你们", "她们",
                   "它们", "这", "那", "这些", "那些", "不", "也", "就", "还", "只", "但", "已经", "还是", "因为",
                   "所以", "如果", "虽然", "然而", "而且", "而是", "这样", "那样", "一样", "这个", "那个", "一个",
                   "一些", "一点", "很", "非常", "真的"]
    stop_words3 = ["大", "成", "化", "局", "总部", "公司", "有限责任", "科技", "有限公司", "控股公司", "合作", "机构",
                   "个人", "行业", "登记", "科技", "责任", "技术", "管理", "项目", "股份", "开发", "生产", "工业"]
    stopwords.extend(capital_cities)
    stopwords.extend(stop_words2)
    stopwords.extend(stop_words3)
    # 去除停用词（标点符号）
    filtered_words = [word for word in token_list if
                      word not in stopwords and len(word) >= 3 and not word.__contains__('公司')]
    return filtered_words


if __name__ == '__main__':
    for csv_file in csv_files:
        # 在这里进行对每个CSV文件的操作
        print("处理文件:", csv_file)

        # 创建一个空的字符串数组
        origin_company_names = []
        cut_tokens = []

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # 将每行数据作为字符串添加到数组中
                origin_company_names.append(','.join(row))

        # 打印字符串数组
        for item in origin_company_names:
            token_list = cut(item)
            cut_tokens.extend(token_list)

        # 每个文件去重
        cut_tokens = list(set(cut_tokens))

        # 构建输出的CSV文件路径
        output_csv_file = os.path.join(output_directory, os.path.basename(csv_file))

        with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 添加标记行
            writer.writerow(['token'])
            for word in cut_tokens:
                writer.writerow([word])

        # 调用 excel.py 中的方法，将 CSV 文件转换为 Excel 文件
        excel.convert_csv_to_excel(output_directory)
