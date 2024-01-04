import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment

# 定义列的顺序
column_order = ['行业', 'token']


def convert_csv_to_excel(directory):
    # 获取目录下所有的 CSV 文件
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

    # 创建一个空的 DataFrame，用于存储数据
    data = pd.DataFrame()

    # 逐个读取 CSV 文件，并将文件名作为第一列，文件内容作为第二列
    for csv_file in csv_files:
        # 构建 CSV 文件的完整路径
        csv_path = os.path.join(directory, csv_file)

        # 读取 CSV 文件内容
        csv_data = pd.read_csv(csv_path)

        # 获取文件名（去除文件后缀）
        file_name = os.path.splitext(csv_file)[0]

        # 添加文件名和文件内容到 DataFrame
        csv_data['行业'] = file_name
        data = pd.concat([data, csv_data], ignore_index=True)

    # 创建 Excel 文件
    output_path = os.path.join(directory, 'output.xlsx')
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    # 调换列的顺序
    data = data[column_order]

    # 将数据写入 Excel 文件
    data.to_excel(writer, index=False, sheet_name='Sheet1')

    # 获取 Excel 文件的工作簿和工作表
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # 合并相同的单元格
    prev_value = None
    start_row = 2  # 从第二行开始，跳过标题行
    for row in range(start_row, 10000):
        current_value = worksheet['A{}'.format(row)].value
        if current_value != prev_value:
            if prev_value is not None:
                worksheet.merge_cells('A{}:A{}'.format(start_row, row - 1))
            prev_value = current_value
            start_row = row

    # 调整列宽和居中对齐
    for column in worksheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
        for cell in column:
            cell.alignment = Alignment(horizontal='center', vertical='center')

    # 保存 Excel 文件
    writer._save()


if __name__ == '__main__':
    directory = '../../output/company/'
    convert_csv_to_excel(directory)