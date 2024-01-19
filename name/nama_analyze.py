import datetime

all_name_list = []
new_name_list = []
all_name_file = "namelist/all.txt"  # 指定包含文件名的文本文件名
new_name_file = "namelist/new.txt"  # 指定包含新文件名的文本文件名


def test():
    with open(all_name_file, encoding="UTF-8") as file:
        content1 = file.read()
        content1 = process_str(content1)
    # 使用分号分割每个文件名，并存储在一个列表中
    all_name_list = content1.split(";")

    with open(new_name_file, encoding="UTF-8") as file:
        content2 = file.read()
        content2 = process_str(content2)
    new_name_list = content2.split(";")

    set_all = set(all_name_list)  # 转换为集合
    set_new = set(new_name_list)  # 转换为集合

    # 所有的比最新的多的就是离职的
    lizhi_list = set_all - set_new
    # 最新的比所有的多的就是入职的
    ruzhi_list = set_new - set_all

    current_date = datetime.date.today()  # 获取当前日期

    formatted_date = current_date.strftime("%Y/%m/%d")  # 将日期格式化为指定格式

    print("建库日期:2024/01/19,当前日期:" + formatted_date)
    print("离职人员:")
    print(lizhi_list)
    print("入职人员:")
    print(ruzhi_list)


def process_str(string):
    # 去除回车符 (\r)
    string = string.replace("\r", "")
    # 去除换行符 (\n)
    string = string.replace("\n", "")
    # 去除制表符 (\t)
    string = string.replace("\t", "")
    # 去除空格
    string = string.replace(" ", "")
    return string


# 使用方式: 首先将new.txt,放入all.txt
# 然后将最新的名单放进new.txt
# 运行程序,即可得到离职人员和入职人员
if __name__ == '__main__':
    test()
