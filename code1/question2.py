import numpy as np
import pandas as pd
from pulp import *

# 1. 读取当前目录中的 Excel 文件
data1 = pd.read_excel("附件/附件1.xlsx")
data2 = pd.read_excel("附件/附件2.xlsx")

# 2. 清理列名，确保列名正确
data1.columns = data1.columns.str.strip()  # 去除列名中的空格
data2.columns = data2.columns.str.strip()

# 3. 获取地块和作物信息
plots = data1["地块名称"].unique()  # 使用 '地块名称' 来标识地块
crops = data2["作物名称"].unique()  # 使用 '作物名称' 列来标识作物

# 4. 提取相关的参数
yield_per_mu = data2.set_index("作物名称")[
    "种植面积/亩"
].to_dict()  # 假设 '种植面积/亩' 表示产量
planting_cost = {}  # 如果有种植成本信息，请在这里补充
expected_sales = {}  # 如果有预期销售量信息，请在这里补充
price_per_unit = {}  # 如果有销售价格信息，请在这里补充

# 获取地块的面积
land_area = data1.set_index("地块名称")[
    "地块面积/亩"
].to_dict()  # 使用 '地块面积/亩' 来获取地块面积


# 5. 定义蒙特卡洛模拟的不确定性
def simulate_uncertainty(base_value, percentage_range):
    return base_value * np.random.uniform(1 - percentage_range, 1 + percentage_range)


# 6. 进行线性规划的求解
def optimize_planting(yield_per_mu, planting_cost, expected_sales, price_per_unit):
    # 创建线性规划问题
    model = LpProblem("Crop_Planning", LpMaximize)

    # 决策变量，定义每年每块地每种作物的种植面积
    plant_area = LpVariable.dicts(
        "Plant_Area",
        (
            (year, plot, crop)
            for year in range(2024, 2031)
            for plot in plots
            for crop in crops
        ),
        lowBound=0,
        cat="Continuous",
    )

    # 引入一个辅助变量，表示实际销售量，等于产量和预期销售量的最小值
    sales_amount = LpVariable.dicts(
        "Sales_Amount",
        (
            (year, plot, crop)
            for year in range(2024, 2031)
            for plot in plots
            for crop in crops
        ),
        lowBound=0,
        cat="Continuous",
    )

    # 目标函数：最大化总收益
    model += lpSum(
        [
            (
                sales_amount[(year, plot, crop)]
                * simulate_uncertainty(price_per_unit.get(crop, 0), 0.05)
                - plant_area[(year, plot, crop)]
                * simulate_uncertainty(planting_cost.get(crop, 0), 0.05)
            )
            for year in range(2024, 2031)
            for plot in plots
            for crop in crops
        ]
    )

    # 约束条件：
    # 1. 每块地的种植面积不能超过该地块的实际面积
    for year in range(2024, 2031):
        for plot in plots:
            model += (
                lpSum([plant_area[(year, plot, crop)] for crop in crops])
                <= land_area[plot]
            )

    # 2. 不重茬约束：同一地块连续两年不能种同一种作物
    for year in range(2025, 2031):
        for plot in plots:
            for crop in crops:
                model += (
                    plant_area[(year, plot, crop)] + plant_area[(year - 1, plot, crop)]
                    <= 1
                )

    # 3. 三年内必须种植一次豆类作物
    bean_crops = ["大豆", "绿豆"]  # 假设这些是豆类作物
    for plot in plots:
        for t in range(2024, 2029, 3):
            # 添加存在性检查，避免访问不存在的变量
            model += (
                lpSum(
                    [
                        plant_area[(year, plot, crop)]
                        for year in range(t, t + 3)
                        for crop in bean_crops
                        if crop in crops
                    ]
                )
                >= 1
            )

    # 4. 实际销售量应该等于产量和预期销售量的最小值
    for year in range(2024, 2031):
        for plot in plots:
            for crop in crops:
                # 实际销售量不能超过产量
                model += sales_amount[(year, plot, crop)] <= plant_area[
                    (year, plot, crop)
                ] * simulate_uncertainty(yield_per_mu.get(crop, 0), 0.1)
                # 实际销售量不能超过预期销售量
                model += sales_amount[(year, plot, crop)] <= expected_sales.get(crop, 0)

    # 求解模型
    model.solve()

    # 检查求解状态，确保模型成功求解
    if LpStatus[model.status] != "Optimal":
        print(
            f"Error: Model did not find an optimal solution. Status: {LpStatus[model.status]}"
        )
        return None

    # 输出结果
    for v in model.variables():
        if v.varValue is not None and v.varValue > 0:  # 确保 varValue 不为 None
            print(f"{v.name} = {v.varValue}")

    # 返回总收益
    return value(model.objective)


# 7. 运行模拟
results = []
for simulation in range(100):  # 运行100次模拟
    print(f"Running simulation {simulation + 1}")
    total_profit = optimize_planting(
        yield_per_mu, planting_cost, expected_sales, price_per_unit
    )
    if total_profit is not None:
        results.append(total_profit)

# 输出平均收益和方差（如果有成功的模拟）
if results:
    print(f"Average Profit: {np.mean(results)}")
    print(f"Profit Standard Deviation: {np.std(results)}")
else:
    print("No successful simulations found.")
