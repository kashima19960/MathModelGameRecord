import pandas as pd

"""1 从附件读取各作物的亩产量"""
# file_path = '附件处理后/2023年统计的相关数据.csv'
# data = pd.read_csv(file_path)
# # 使用作物名称和作物编号创建一个复合键，并提取亩产量列
# # 如果作物名称重复，将亩产量值合并为一个列表
# yield_per_acre = data.groupby('作物名称')['亩产量/斤'].mean().to_dict()
# # 打印字典内容
# print(yield_per_acre)
"""2 从附件读取各作物的价格"""

# # 读取CSV文件
# data = pd.read_csv("temp.csv")
# # 定义一个函数来计算价格区间的中间值
# def calculate_middle_price(price_range):
#     if pd.isna(price_range):
#         return None
#     min_price, max_price = map(float, price_range.split("-"))
#     return round((min_price + max_price) / 2, 3)

# for index, row in data.iterrows():
#     original_price = row['销售单价/(元/斤)']
#     middle_price = calculate_middle_price(original_price)
#     print(middle_price)
#     data.at[index, '销售单价/(元/斤)'] = middle_price
# data.to_csv("temp.csv")
# 使用作物名称作为索引，提取销售单价列，并计算每个价格区间的中间值
# price_per_jin = (
#     data.set_index("作物名称")["预期销售额"]
#     .to_list()
# )
# # 打印字典内容
# print(price_per_jin)


""" 3 从附件读取各作物的种植成本"""
# file_path = '附件处理后/2023年统计的相关数据.csv'
# data = pd.read_csv(file_path)
# # 使用作物名称作为索引，提取种植成本列，并确保作物名称重复时成本被正确处理
# cost_per_acre = data.groupby('作物名称')['种植成本/(元/亩)'].mean().to_dict()
# print(cost_per_acre)

"""4 从附件读取各作物的预期销售量"""
# # 重新读取上传的CSV文件
# file_path_csv = '附件处理后\预期销售额汇总.csv'
# # 读取数据
# data = pd.read_csv(file_path_csv)
# # 计算每个作物的种植面积*亩产量
# data['预期销售额'] = data['种植面积/亩'] * data['亩产量/斤']
# expected_sales = data.groupby('作物名称')['预期销售额'].sum().to_dict()
# print(expected_sales)

"""5 从附件读取各地块的面积"""
# file_path = '附件处理后/乡村的现有耕地.csv'
# data = pd.read_csv(file_path)
# # 使用作物名称作为索引，提取种植成本列，并确保作物名称重复时成本被正确处理
# plot_area = data.groupby('地块名称')['地块面积/亩'].mean().to_dict()
# print(plot_area)

# """6 合并两张表"""
# df1=pd.read_csv("2023年的农作物种植情况temp.csv")
# df2=pd.read_csv("2023年统计的相关数据temp.csv")
# df3=pd.merge(df1,df2,on=['作物名称','地块类型'],how='inner'
#              )
# df3.to_csv("temp.csv",index=False)

"""7 将地块名称的数字转换成A1类的字符   """
# path="test3.csv"
# df= pd.read_csv(path)

# sequence_to_land_plot = {1: 'A1', 2: 'A2', 3: 'A3', 4: 'A4', 5: 'A5', 6: 'A6', 7: 'B1', 8: 'B2', 9: 'B3', 10: 'B4', 11: 'B5', 12: 'B6', 13: 'B7', 14: 'B8', 15: 'B9', 16: 'B10', 17: 'B11', 18: 'B12', 19: 'B13', 20: 'B14', 21: 'C1', 22: 'C2', 23: 'C3', 24: 'C4', 25: 'C5', 26: 'C6', 27: 'D1', 28: 'D2', 29: 'D3', 30: 'D4', 31: 'D5', 32: 'D6', 33: 'D7', 34: 'D8', 35: 'E1', 36: 'E2', 37: 'E3', 38: 'E4', 39: 'E5', 40: 'E6', 41: 'E7', 42: 'E8', 43: 'E9', 44: 'E10', 45: 'E11', 46: 'E12', 47: 'E13', 48: 'E14', 49: 'E15', 50: 'E16', 51: 'F1', 52: 'F2', 53: 'F3', 54: 'F4'}
# # Convert the sequence numbers to land plot names using the mapping dictionary
# df['地块名称'] = df['地块名称'].map(sequence_to_land_plot)

# acre_yield={'刀豆': 1, '包菜': 2, '南瓜': 3, '土豆': 4, '大白菜': 5, '大麦': 6, '小青菜': 7, '小麦': 8, '榆黄菇': 9, '水稻': 10, '油麦菜': 11, '爬豆': 12, '玉米': 13, '生菜': 14, '白灵菇': 15, '白萝卜': 16, '空心菜': 17, '红萝卜': 18, '红薯': 19, '红豆': 20, '绿豆': 21, '羊肚菌': 22, '芸豆': 23, '芹菜': 24, '茄子': 25, '荞麦': 26, '莜麦': 27, '菜花': 28, '菠菜': 29, '西红柿': 30, '谷子': 31, '豇豆': 32, '辣椒': 33, '青椒': 34, '香菇': 35, '高粱': 36, '黄心菜': 37, '黄瓜': 38, '黄豆': 39, ' 黍子': 40, '黑豆': 41}
# acre_yield={j:i for i ,j in acre_yield.items()}
# print(acre_yield)
# df['作物']=df['作物'].map(acre_yield)
# df.to_csv(path, index=False)


"""8 往模板里面填充数值"""
# 加载 test1_1.csv 和 result1_1_2024.csv 文件
df = pd.read_csv('test3.csv')
for i in range(2024,2031):
    result_year_df = pd.read_csv(f'模板文件/result1_1_{i}.csv')
    # 筛选出 test1_1.csv 中年份为2024的所有行
    for year in range(2024,2031):
        rows_year = df[df['年份'] == year]

        # 对于每一行，找到 result1_1_2024.csv 中对应的行号和列号，并填入面积值
        for _, row in rows_year.iterrows():
            land_name = row['地块名']  # 获取地块名
            crop_name = row['作物']  # 获取作物名
            area = row['面积/亩']  # 获取面积值
            
            # 使用地块名在 result1_1_2024_df 中找到对应的行号
            row_index = result_year_df.index[result_year_df['地块名'] == land_name].tolist()
            # 如果找到了地块名，使用作物名找到对应的列号
            if row_index:
                row_index = row_index[0]
                if crop_name in result_year_df.columns:
                    col_index = result_year_df.columns.get_loc(crop_name)
                    # 在对应的行号和列号填入面积值
                    result_year_df.iat[row_index, col_index] = area

        # 将修改后的 result1_1_2024_df 保存到新的 CSV 文件
        output_path = f'结果/result3_{year}.csv'
        result_year_df.to_csv(output_path, index=False)

## 合并csv文件
