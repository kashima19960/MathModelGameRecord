import pulp as lp
import numpy as np
import sys 
sys.stdout=open('output3.txt','w')
# 定义地块、作物、年份、季节等
plots = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5', 
         'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 
         'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 
         'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 
         'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16',
         'F1', 'F2', 'F3', 'F4']
crops = ['黄豆', '黑豆', '红豆', '绿豆', '爬豆', '小麦', '玉米', '谷子', '高粱', '黍子', 
         '荞麦', '南瓜', '红薯', '莜麦', '大麦', '水稻', '豇豆', '刀豆', '芸豆', 
         '土豆', '西红柿', '茄子', '菠菜', '青椒', '菜花', '包菜', '油麦菜', 
         '小青菜', '黄瓜', '生菜', '辣椒', '空心菜', '黄心菜', '芹菜', 
         '大白菜', '白萝卜', '红萝卜', '榆黄菇', '香菇', '白灵菇', '羊肚菌']

years = list(range(2024, 2031))
seasons = [1, 2]

# 定义数据：产量、价格、成本、预期销售量、地块面积等
yield_per_acre = {'刀豆': 2200.0, '包菜': 4100.0, '南瓜': 2850.0, '土豆': 2200.0, '大白菜': 5000.0, '大麦': 500.0, '小青菜': 3600.0, '小麦': 760.0, '榆黄菇': 5000.0, '水稻': 500.0, '油麦菜': 4533.333333333333, '爬豆': 395.0, '玉米': 950.0, '生菜': 4533.333333333333, '白灵菇': 10000.0, '白萝卜': 4000.0, '空心菜': 11000.0, '红萝卜': 3000.0, '红薯': 2100.0, '红豆': 380.0, '绿豆': 331.6666666666667, '羊肚菌': 1000.0, '芸豆': 3266.6666666666665, '芹菜': 6033.333333333333, '茄子': 7200.0, '荞麦': 105.0, '莜麦': 400.0, '菜花': 3633.3333333333335, '菠菜': 3000.0, '西红柿': 2700.0, '谷子': 380.0, '豇豆': 3266.6666666666665, '辣椒': 1800.0, '青椒': 2700.0, '香菇': 4000.0, '高粱': 600.0, '黄心菜': 5466.666666666667, '黄瓜': 13500.0, '黄豆': 380.0, '黍子': 500.0, '黑豆': 475.0} # 从附件读取各作物的亩产量

price_per_jin = {'黄豆': 3.25, '黑豆': 7.5, '红豆': 8.25, '绿豆': 7.0, '爬豆': 6.75, '小麦': 3.5, '玉米': 3.0, '谷子': 6.75, '高粱': 6.0, '黍子': 7.5, '荞麦': 40.0, '南瓜': 1.5, '红薯': 3.25, '莜麦': 5.5, '大麦': 3.5, '水稻': 7.0, '豇豆': 9.6, '刀豆': 8.1, '芸豆': 7.8, '土豆': 4.5, '西红柿': 7.5, '茄子': 6.6, '菠菜': 6.9, '青椒': 6.8, '菜花': 6.6, '包菜': 7.8, '油麦菜': 6.0, '小青菜': 6.9, '黄瓜': 8.4, '生菜': 6.3, '辣椒': 8.7, '空心菜': 5.4, '黄心菜': 5.4, '芹菜': 4.8, '大白菜': 2.5, '白萝卜': 2.5, '红萝卜': 3.25, '榆黄菇': 57.5, '香菇': 19.0, '白灵菇': 16.0, '羊肚菌': 100.0}  # 从附件读取各作物的价格


cost_per_acre ={'刀豆': 1173.3333333333333, '包菜': 3416.6666666666665, '南瓜': 1000.0, '土豆': 2346.6666666666665, '大白菜': 2000.0, '大麦': 350.0, '小青菜': 1933.3333333333333, '小麦': 450.0, '榆黄菇': 3000.0, '水稻': 680.0, '油麦菜': 1933.3333333333333, '爬豆': 350.0, '玉米': 500.0, '生菜': 1933.3333333333333, '白灵菇': 10000.0, '白萝卜': 500.0, '空心菜': 4866.666666666667, '红萝卜': 500.0, '红薯': 2000.0, '红豆': 350.0, '绿豆': 350.0, '羊肚菌': 10000.0, '芸豆': 2346.6666666666665, '芹菜': 1066.6666666666667, '茄子': 2346.6666666666665, '荞麦': 350.0, '莜麦': 400.0, '菜花': 2900.0, '菠菜': 2666.6666666666665, '西红柿': 2346.6666666666665, '谷子': 360.0, '豇豆': 2346.6666666666665, '辣椒': 1166.6666666666667, '青椒': 1933.3333333333333, '香菇': 2000.0, '高粱': 400.0, '黄心菜': 2416.6666666666665, '黄瓜': 3416.6666666666665, '黄豆': 400.0, '黍子': 360.0, '黑豆': 400.0} # 从附件读取各作物的种植成本


expected_sales = {'刀豆': 26880.0, '包菜': 3930.0, '南瓜': 35100.0, '土豆': 30000.0, '大白菜': 150000.0, '大麦': 10000.0, '小青菜': 35480.0, '小麦': 170840.0, '榆黄菇': 9000.0, '水稻': 21000.0, '油麦菜': 4500.0, '爬豆': 9875.0, '玉米': 132750.0, '生菜': 1500.0, '生菜 ': 1350.0, '白灵菇': 18000.0, '白萝卜': 100000.0, '空心菜': 3300.0, '红萝卜': 36000.0, '红薯': 36000.0, '红豆': 22400.0, '绿豆': 33040.0, '羊肚菌': 4200.0, '芸豆': 6240.0, '芹菜': 1800.0, '茄子': 45360.0, '荞麦': 1500.0, '莜麦': 14000.0, '菜花': 3480.0, '菠菜': 900.0, '西红柿': 36210.0, '谷子': 71400.0, '豇豆': 36240.0, '辣椒': 1200.0, '青椒': 2610.0, '香菇': 7200.0, '高粱': 30000.0, '黄心菜': 1620.0, '黄瓜': 13050.0, '黄豆': 57000.0, '黍子': 12500.0, '黑豆': 21850.0}  # 从附件读取各作物的预期销售量

plot_area = {'A1': 80.0, 'A2': 55.0, 'A3': 35.0, 'A4': 72.0, 'A5': 68.0, 'A6': 55.0, 'B1': 60.0, 'B10': 25.0, 'B11': 60.0, 'B12': 45.0, 'B13': 35.0, 'B14': 20.0, 'B2': 46.0, 'B3': 40.0, 'B4': 28.0, 'B5': 25.0, 'B6': 86.0, 'B7': 55.0, 'B8': 44.0, 'B9': 50.0, 'C1': 15.0, 'C2': 13.0, 'C3': 15.0, 'C4': 18.0, 'C5': 27.0, 'C6': 20.0, 'D1': 15.0, 'D2': 10.0, 'D3': 14.0, 'D4': 6.0, 'D5': 10.0, 'D6': 12.0, 'D7': 22.0, 'D8': 20.0, 'E1': 0.6, 'E10': 0.6, 'E11': 0.6, 'E12': 0.6, 'E13': 0.6, 'E14': 0.6, 'E15': 0.6, 'E16': 0.6, 'E2': 0.6, 'E3': 0.6, 'E4': 0.6, 'E5': 0.6, 'E6': 0.6, 'E7': 0.6, 'E8': 0.6, 'E9': 0.6, 'F1': 0.6, 'F2': 0.6, 'F3': 0.6, 'F4': 0.6}    # 从附件读取各地块的面积
      # 从附件1读取各地块的面积

# 替代性和互补性系数：根据作物之间的关系设置
substitution_coefficients = {
    ('小麦', '玉米'): 0.2,  # 小麦与玉米之间的替代性
    # 其他替代性系数...
}

complementary_coefficients = {
    ('黄豆', '玉米'): 0.1,  # 黄豆与玉米之间的互补性
    # 其他互补性系数...
}

# 处理不确定性
def apply_uncertainty(value, lower_bound, upper_bound):
    return value * np.random.uniform(lower_bound, upper_bound)

# 模拟未来的销售量、产量、种植成本和价格
for year in years:
    for crop in crops:
        if crop in ['小麦', '玉米']:
            expected_sales[crop] *= np.random.uniform(1.05, 1.10)  # 小麦和玉米年增长率5%-10%
        else:
            expected_sales[crop] *= np.random.uniform(0.95, 1.05)  # 其他作物±5%变化

        yield_per_acre[crop] = apply_uncertainty(yield_per_acre[crop], 0.9, 1.1)  # 产量±10%变化
        cost_per_acre[crop] *= 1.05  # 成本每年增长5%

        if crop in ['榆黄菇', '香菇', '白灵菇', '羊肚菌']:
            price_per_jin[crop] *= np.random.uniform(0.95, 0.99)  # 食用菌价格每年下降1%-5%
            if crop == '羊肚菌':
                price_per_jin[crop] *= 0.95  # 羊肚菌价格每年下降5%
        elif crop in ['黄豆', '黑豆', '红豆', '绿豆', '爬豆', '小麦', '谷子', '高粱', '黍子', '荞麦', '大麦', '水稻']:
            pass  # 粮食类作物价格基本稳定
        else:
            price_per_jin[crop] *= 1.05  # 蔬菜价格每年增长5%

# 创建优化模型
model = lp.LpProblem("Maximize_Profit_with_Substitution_Complementarity", lp.LpMaximize)

# 创建决策变量（整数规划）
x = lp.LpVariable.dicts("Area", (plots, crops, years, seasons), lowBound=0, cat='Integer')
y = lp.LpVariable.dicts("Crop_Planted", (plots, crops, years, seasons), cat='Binary')
# 目标函数：最大化总利润
total_profit = lp.lpSum([
    (price_per_jin[crop] * lp.lpSum([yield_per_acre[crop] * x[plot][crop][year][season] 
                                     if yield_per_acre[crop] * x[plot][crop][year][season] <= expected_sales[crop] 
                                     else expected_sales[crop] for crop in crops]) + 
    0.5 * price_per_jin[crop] * lp.lpSum([yield_per_acre[crop] * x[plot][crop][year][season] - expected_sales[crop] 
                                          if yield_per_acre[crop] * x[plot][crop][year][season] >= expected_sales[crop] 
                                          else 0 for crop in crops]) - 
    cost_per_acre[crop] * x[plot][crop][year][season])
    for plot in plots for crop in crops for year in years for season in seasons
])

model += total_profit


# 约束1：地块面积不得超过限制
for plot in plots:
    for year in years:
        for season in seasons:
            model += lp.lpSum([x[plot][crop][year][season] for crop in crops]) <= plot_area[plot]

# 约束2：每个地块三年内至少种植一次豆类作物
for plot in plots:
    for year in years:
        model += lp.lpSum([x[plot][crop][year][season] for crop in ['黄豆', '黑豆', '红豆', '绿豆', '豇豆', '刀豆', '芸豆'] for season in seasons]) >= plot_area[plot] / 3

# 引入辅助的二进制决策变量
# 约束3：同一地块不能连续种植相同作物（避免重茬）
for plot in plots:
    for year in years[:-1]:  # 遍历到倒数第二个年份
        for season in seasons:
            for crop in crops:
                # 确保当前年份和季节种植的作物与下一年的相同季节或不同年份的不同季节不重复
                model +=( y[plot][crop][year][season] +y[plot][crop][year+1][season]) <= 1


# 约束4：所有平旱地、梯田和山坡地每年只能种植一季粮食类作物：
for plot in plots[:27]:
    for year in years:
        for season in seasons:
            model+=lp.lpSum([y[plot][crop][year][season] for crop in crops[:17]]) <= 1

# 约束5:水浇地适宜每年种植一季水稻或两季蔬菜：
for year in years:
    for season in seasons:
        model+=lp.lpSum([[y[plot][crop][year][season] for plot in plots[27:35] for crop in crops[16:41]]]) <= 2

# 约束6:普通大棚每年种植两季作物，第一季可种植多种蔬菜（大白菜、白萝卜和红萝卜除外），第二季只能种植食用菌
for year in years:
    for season in seasons:
        model+=lp.lpSum([[y[plot][crop][year][season] for plot in plots[35:55] for crop in crops[17:42]]]) == 2


# 约束7:智慧大棚每年都可种植两季蔬菜（大白菜、白萝卜和红萝卜除外）：
for year in years:
    for season in seasons:
        model+=lp.lpSum([[y[plot][crop][year][season] for plot in plots[51:55] for crop in crops[17:35]]]) == 1


# 约束10:.若在某块水浇地种植两季蔬菜，第一季可种植多种蔬菜（大白菜、白萝卜和红萝卜除外），第二季只能种植大白菜、白萝卜和红萝卜中的一种：
for plot in plot[27:35]:
    for year in years:
        for crop in crops[17:35]:
            model+=y[plot][crop][year][1] == 0
            model+=y[plot][crop][year][2] == 1
        for crop in crops[35:38]:
            model+=y[plot][crop][year][1] == 1
            model+=y[plot][crop][year][2] == 0
# 约束12:食用菌类只能在秋冬季的普通大棚里种植：
for plot in plots[35:51]:
    for crop in crops[38:42]:
        for year in years:
            model+=y[plot][crop][year][1] == 1

# 新增约束条件：替代性与互补性
for (crop1, crop2), coef in substitution_coefficients.items():
    for year in years:
        for season in seasons:
            model += expected_sales[crop2] >= expected_sales[crop2] - coef * lp.lpSum([x[plot][crop1][year][season] for plot in plots])

for (crop1, crop2), coef in complementary_coefficients.items():
    for year in years:
        for season in seasons:
            model += yield_per_acre[crop2] == yield_per_acre[crop2] + coef * lp.lpSum([x[plot][crop1][year][season] for plot in plots])

# 求解模型
model.solve()
print(f"Total Profit: {lp.value(model.objective)}")
# 输出结果并填入表格
print("最优种植方案：")
for plot in plots:
    for crop in crops:
        for year in years:
            for season in seasons:
                if x[plot][crop][year][season].varValue > 0:
                    print(f"地块: {plot}, 作物: {crop}, 年份: {year}, 季节: {season}, 面积: {x[plot][crop][year][season].varValue} 亩")

