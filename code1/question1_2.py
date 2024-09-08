import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, value
import sys

sys.stdout = open("test1_2.csv", "w",encoding="utf-8")
# 读取地块数据和作物种植数据
land_data = pd.read_excel(
    "附件/附件1.xlsx"
)  # 假设第一张表有地块编号、地块面积、地块类型
crop_data = pd.read_excel("附件/附件2.xlsx")  # 假设第二张表包含了2023年的种植情况

# 打印列名，确保我们使用正确的列名
# print(land_data.columns)

acre_yield = {
    "刀豆": 2200.0,
    "包菜": 4100.0,
    "南瓜": 2850.0,
    "土豆": 2200.0,
    "大白菜": 5000.0,
    "大麦": 500.0,
    "小青菜": 3600.0,
    "小麦": 760.0,
    "榆黄菇": 5000.0,
    "水稻": 500.0,
    "油麦菜": 4533.333333333333,
    "爬豆": 395.0,
    "玉米": 950.0,
    "生菜": 4533.333333333333,
    "白灵菇": 10000.0,
    "白萝卜": 4000.0,
    "空心菜": 11000.0,
    "红萝卜": 3000.0,
    "红薯": 2100.0,
    "红豆": 380.0,
    "绿豆": 331.6666666666667,
    "羊肚菌": 1000.0,
    "芸豆": 3266.6666666666665,
    "芹菜": 6033.333333333333,
    "茄子": 7200.0,
    "荞麦": 105.0,
    "莜麦": 400.0,
    "菜花": 3633.3333333333335,
    "菠菜": 3000.0,
    "西红柿": 2700.0,
    "谷子": 380.0,
    "豇豆": 3266.6666666666665,
    "辣椒": 1800.0,
    "青椒": 2700.0,
    "香菇": 4000.0,
    "高粱": 600.0,
    "黄心菜": 5466.666666666667,
    "黄瓜": 13500.0,
    "黄豆": 380.0,
    "黍子": 500.0,
    "黑豆": 475.0,
}  # 从附件读取各作物的亩产量

expected_sales = {
    "刀豆": 26880.0,
    "包菜": 3930.0,
    "南瓜": 35100.0,
    "土豆": 30000.0,
    "大白菜": 150000.0,
    "大麦": 10000.0,
    "小青菜": 35480.0,
    "小麦": 170840.0,
    "榆黄菇": 9000.0,
    "水稻": 21000.0,
    "油麦菜": 4500.0,
    "爬豆": 9875.0,
    "玉米": 132750.0,
    "生菜": 1500.0,
    "生菜 ": 1350.0,
    "白灵菇": 18000.0,
    "白萝卜": 100000.0,
    "空心菜": 3300.0,
    "红萝卜": 36000.0,
    "红薯": 36000.0,
    "红豆": 22400.0,
    "绿豆": 33040.0,
    "羊肚菌": 4200.0,
    "芸豆": 6240.0,
    "芹菜": 1800.0,
    "茄子": 45360.0,
    "荞麦": 1500.0,
    "莜麦": 14000.0,
    "菜花": 3480.0,
    "菠菜": 900.0,
    "西红柿": 36210.0,
    "谷子": 71400.0,
    "豇豆": 36240.0,
    "辣椒": 1200.0,
    "青椒": 2610.0,
    "香菇": 7200.0,
    "高粱": 30000.0,
    "黄心菜": 1620.0,
    "黄瓜": 13050.0,
    "黄豆": 57000.0,
    "黍子": 12500.0,
    "黑豆": 21850.0,
}  # 从附件读取各作物的预期销售量
sale_price = {
    "黄豆": 3.25,
    "黑豆": 7.5,
    "红豆": 8.25,
    "绿豆": 7.0,
    "爬豆": 6.75,
    "小麦": 3.5,
    "玉米": 3.0,
    "谷子": 6.75,
    "高粱": 6.0,
    "黍子": 7.5,
    "荞麦": 40.0,
    "南瓜": 1.5,
    "红薯": 3.25,
    "莜麦": 5.5,
    "大麦": 3.5,
    "水稻": 7.0,
    "豇豆": 9.6,
    "刀豆": 8.1,
    "芸豆": 7.8,
    "土豆": 4.5,
    "西红柿": 7.5,
    "茄子": 6.6,
    "菠菜": 6.9,
    "青椒": 6.8,
    "菜花": 6.6,
    "包菜": 7.8,
    "油麦菜": 6.0,
    "小青菜": 6.9,
    "黄瓜": 8.4,
    "生菜": 6.3,
    "辣椒": 8.7,
    "空心菜": 5.4,
    "黄心菜": 5.4,
    "芹菜": 4.8,
    "大白菜": 2.5,
    "白萝卜": 2.5,
    "红萝卜": 3.25,
    "榆黄菇": 57.5,
    "香菇": 19.0,
    "白灵菇": 16.0,
    "羊肚菌": 100.0,
}
cost = {
    "刀豆": 1173.3333333333333,
    "包菜": 3416.6666666666665,
    "南瓜": 1000.0,
    "土豆": 2346.6666666666665,
    "大白菜": 2000.0,
    "大麦": 350.0,
    "小青菜": 1933.3333333333333,
    "小麦": 450.0,
    "榆黄菇": 3000.0,
    "水稻": 680.0,
    "油麦菜": 1933.3333333333333,
    "爬豆": 350.0,
    "玉米": 500.0,
    "生菜": 1933.3333333333333,
    "白灵菇": 10000.0,
    "白萝卜": 500.0,
    "空心菜": 4866.666666666667,
    "红萝卜": 500.0,
    "红薯": 2000.0,
    "红豆": 350.0,
    "绿豆": 350.0,
    "羊肚菌": 10000.0,
    "芸豆": 2346.6666666666665,
    "芹菜": 1066.6666666666667,
    "茄子": 2346.6666666666665,
    "荞麦": 350.0,
    "莜麦": 400.0,
    "菜花": 2900.0,
    "菠菜": 2666.6666666666665,
    "西红柿": 2346.6666666666665,
    "谷子": 360.0,
    "豇豆": 2346.6666666666665,
    "辣椒": 1166.6666666666667,
    "青椒": 1933.3333333333333,
    "香菇": 2000.0,
    "高粱": 400.0,
    "黄心菜": 2416.6666666666665,
    "黄瓜": 3416.6666666666665,
    "黄豆": 400.0,
    "黍子": 360.0,
    "黑豆": 400.0,
}
# 转换为列表
acre_yield = list(acre_yield.values())
expected_sales = list(expected_sales.values())
sale_price = list(sale_price.values())
cost = list(cost.values())

# 创建线性规划模型
model = LpProblem("Crop_Optimization", LpMaximize)

# 假设有3个作物，使用列表长度确定作物数量
num_crops = len(acre_yield)
# 决策变量：x_ij_t 表示在第 t 年，地块 i 上种植作物 j 的面积
# i 为地块索引，j 为作物索引，t 为年份索引
x = LpVariable.dicts(
    "x",
    [
        (i, j, t)
        for i in range(len(land_data))
        for j in range(num_crops)
        for t in range(2024, 2031)
    ],
    lowBound=0,
)

# 新的二进制变量 y_ij_t 表示某个地块 i 在第 t 年是否种植作物 j
y = LpVariable.dicts(
    "y",
    [
        (i, j, t)
        for i in range(len(land_data))
        for j in range(num_crops)
        for t in range(2024, 2031)
    ],
    lowBound=0,
    upBound=1,
    cat="Binary",
)

# 辅助变量：用于表示min和max
min_production = LpVariable.dicts(
    "min_production",
    [
        (i, j, t)
        for i in range(len(land_data))
        for j in range(num_crops)
        for t in range(2024, 2031)
    ],
    lowBound=0,
)

excess_production = LpVariable.dicts(
    "excess_production",
    [
        (i, j, t)
        for i in range(len(land_data))
        for j in range(num_crops)
        for t in range(2024, 2031)
    ],
    lowBound=0,
)

# 定义目标函数：包括正常销售收益和超额部分以50%价格销售的收益，减去种植成本
profit = lpSum(
    [
        min_production[(i, j, t)] * sale_price[j]
        + excess_production[(i, j, t)] * 0.5 * sale_price[j]
        - x[(i, j, t)] * cost[j]
        for i in range(len(land_data))
        for j in range(num_crops)
        for t in range(2024, 2031)
    ]
)

model += profit

# 约束条件1：每个地块的种植面积不能超过地块实际面积
for i in range(len(land_data)):
    for t in range(2024, 2031):
        model += (
            lpSum([x[(i, j, t)] for j in range(num_crops)])
            <= land_data["地块面积/亩"][i]
        )

# 约束条件2：不重茬种植（同一地块不能连续两年种植相同的作物）
for i in range(len(land_data)):
    for j in range(num_crops):
        for t in range(2025, 2031):  # 从2025年开始检查不重茬
            model += y[(i, j, t)] + y[(i, j, t - 1)] <= 1  # 不允许连续两年种植同一作物

# 约束条件3：豆类作物三年内至少种植一次（假设豆类作物为作物编号0和1）
for i in range(len(land_data)):
    for T in [2024, 2027]:
        model += (
            lpSum(
                [
                    y[(i, j, t)]
                    for j in range(2)  # 假设作物0和作物1是豆类
                    for t in range(T, T + 3)
                ]
            )
            >= 1
        )  # 三年内至少种植一次豆类作物

# 约束条件4：min_production <= 产量且不能超过预期销售量
for i in range(len(land_data)):
    for j in range(num_crops):
        for t in range(2024, 2031):
            # 总产量
            production = x[(i, j, t)] * acre_yield[j]
            # min_production 不能超过预期销售量，并且不能大于实际产量
            model += min_production[(i, j, t)] <= expected_sales[j]
            model += min_production[(i, j, t)] <= production
            # excess_production 是超出部分
            model += (
                excess_production[(i, j, t)] == production - min_production[(i, j, t)]
            )

# 约束条件5：x 和 y 之间的关系，确保 x_ij_t 为0时，y_ij_t 也为0
M = 100000  # 一个较大的常数
for i in range(len(land_data)):
    for j in range(num_crops):
        for t in range(2024, 2031):
            model += x[(i, j, t)] <= y[(i, j, t)] * M

# 求解模型
model.solve()

# 输出结果
print(f"地块名称,作物,年份,面积/亩")
for i in range(len(land_data)):
    for j in range(num_crops):
        for t in range(2024, 2031):
            if x[(i, j, t)].varValue > 0:
                print(
                    f"{i+1},{j},{t},{x[(i, j, t)].varValue} "
                )


path="test1_2.csv"
df= pd.read_csv(path)

sequence_to_land_plot = {1: 'A1', 2: 'A2', 3: 'A3', 4: 'A4', 5: 'A5', 6: 'A6', 7: 'B1', 8: 'B2', 9: 'B3', 10: 'B4', 11: 'B5', 12: 'B6', 13: 'B7', 14: 'B8', 15: 'B9', 16: 'B10', 17: 'B11', 18: 'B12', 19: 'B13', 20: 'B14', 21: 'C1', 22: 'C2', 23: 'C3', 24: 'C4', 25: 'C5', 26: 'C6', 27: 'D1', 28: 'D2', 29: 'D3', 30: 'D4', 31: 'D5', 32: 'D6', 33: 'D7', 34: 'D8', 35: 'E1', 36: 'E2', 37: 'E3', 38: 'E4', 39: 'E5', 40: 'E6', 41: 'E7', 42: 'E8', 43: 'E9', 44: 'E10', 45: 'E11', 46: 'E12', 47: 'E13', 48: 'E14', 49: 'E15', 50: 'E16', 51: 'F1', 52: 'F2', 53: 'F3', 54: 'F4'}
# Convert the sequence numbers to land plot names using the mapping dictionary
df['地块名称'] = df['地块名称'].map(sequence_to_land_plot)

acre_yield={'刀豆': 1, '包菜': 2, '南瓜': 3, '土豆': 4, '大白菜': 5, '大麦': 6, '小青菜': 7, '小麦': 8, '榆黄菇': 9, '水稻': 10, '油麦菜': 11, '爬豆': 12, '玉米': 13, '生菜': 14, '白灵菇': 15, '白萝卜': 16, '空心菜': 17, '红萝卜': 18, '红薯': 19, '红豆': 20, '绿豆': 21, '羊肚菌': 22, '芸豆': 23, '芹菜': 24, '茄子': 25, '荞麦': 26, '莜麦': 27, '菜花': 28, '菠菜': 29, '西红柿': 30, '谷子': 31, '豇豆': 32, '辣椒': 33, '青椒': 34, '香菇': 35, '高粱': 36, '黄心菜': 37, '黄瓜': 38, '黄豆': 39, ' 黍子': 40, '黑豆': 41}
acre_yield={j:i for i ,j in acre_yield.items()}
print(acre_yield)
df['作物']=df['作物'].map(acre_yield)
df.to_csv(path, index=False)
