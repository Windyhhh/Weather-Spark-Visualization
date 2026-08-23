#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于Pandas的气象数据处理与分析
计算城市累积雨量和日平均气温
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import warnings
warnings.filterwarnings('ignore')

def load_weather_data(file_path):
    """加载气象数据"""
    print("正在加载气象数据...")
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"数据加载完成，共{len(df)}条记录")
        print("数据列：", list(df.columns))
        return df
    except Exception as e:
        print(f"数据加载失败：{e}")
        return None

def task1_calculate_rainfall(df):
    """任务1：计算各个城市过去24小时累积雨量"""
    print("\n" + "="*50)
    print("任务1：计算各个城市过去24小时累积雨量")
    print("="*50)
    
    # 数据清理：过滤异常数据
    df_rain = df.copy()
    df_rain['rain1h'] = pd.to_numeric(df_rain['rain1h'], errors='coerce')
    df_rain = df_rain[df_rain['rain1h'] < 1000]  # 过滤异常值
    df_rain = df_rain.dropna(subset=['rain1h'])
    
    # 按城市分组计算累积雨量
    rainfall_summary = df_rain.groupby(['province', 'city_name', 'city_code']).agg({
        'rain1h': 'sum'
    }).reset_index()
    rainfall_summary.columns = ['省份', '城市', '城市代码', '24小时累积雨量(mm)']
    rainfall_summary = rainfall_summary.sort_values('24小时累积雨量(mm)', ascending=False)
    
    # 保存结果
    rainfall_summary.to_csv('rainfall_results.csv', index=False, encoding='utf-8-sig')
    
    print(f"累积雨量计算完成，共{len(rainfall_summary)}个城市")
    print("前10名累积降雨量城市：")
    for i, row in rainfall_summary.head(10).iterrows():
        print(f"{rainfall_summary.index.get_loc(i)+1:2d}. {row['省份']}-{row['城市']}: {row['24小时累积雨量(mm)']}mm")
    
    return rainfall_summary.head(20)

def task2_calculate_temperature(df):
    """任务2：计算各个城市当日平均气温"""
    print("\n" + "="*50)
    print("任务2：计算各个城市当日平均气温")
    print("="*50)
    
    # 数据清理
    df_temp = df.copy()
    df_temp['temperature'] = pd.to_numeric(df_temp['temperature'], errors='coerce')
    df_temp = df_temp[(df_temp['temperature'] > -50) & (df_temp['temperature'] < 60)]
    df_temp = df_temp.dropna(subset=['temperature', 'time'])
    
    # 转换时间格式
    df_temp['time'] = pd.to_datetime(df_temp['time'])
    df_temp['hour'] = df_temp['time'].dt.hour
    df_temp['date'] = df_temp['time'].dt.date
    
    # 筛选02、08、14、20时的数据
    four_point_data = df_temp[df_temp['hour'].isin([2, 8, 14, 20])]
    
    # 按城市和日期分组，计算平均气温
    temp_summary = four_point_data.groupby(['province', 'city_name', 'city_code', 'date']).agg({
        'temperature': ['count', 'mean']
    }).reset_index()
    
    temp_summary.columns = ['省份', '城市', '城市代码', '日期', '有效时次', '日平均气温(°C)']
    
    # 只保留有4个时次数据的记录
    temp_summary = temp_summary[temp_summary['有效时次'] == 4]
    temp_summary = temp_summary.sort_values('日平均气温(°C)')
    
    # 保留一位小数
    temp_summary['日平均气温(°C)'] = temp_summary['日平均气温(°C)'].round(1)
    
    # 保存结果
    temp_summary.to_csv('temperature_results.csv', index=False, encoding='utf-8-sig')
    
    print(f"日平均气温计算完成，共{len(temp_summary)}个城市")
    print("前10名最低日平均气温城市：")
    for i, row in temp_summary.head(10).iterrows():
        print(f"{temp_summary.index.get_loc(i)+1:2d}. {row['省份']}-{row['城市']} ({row['日期']}): {row['日平均气温(°C)']}°C")
    
    return temp_summary.head(10)

def draw_rain(rain_list):
    """绘制累积降雨量图表"""
    print("\n正在绘制累积降雨量图表...")
    
    try:
        font = FontProperties(fname='simhei.ttf')
    except:
        font = FontProperties()
    
    name_list = []
    num_list = []
    
    for _, item in rain_list.iterrows():
        name_list.append(item['省份'][0:2] + '\n' + item['城市'])
        num_list.append(item['24小时累积雨量(mm)'])
    
    index = [i + 0.25 for i in range(0, len(num_list))]
    rects = plt.bar(index, num_list, color='lightblue', width=0.5)
    
    plt.xticks([i + 0.25 for i in index], name_list, fontproperties=font, fontsize=8)
    plt.ylim(ymax=max(num_list) * 1.1, ymin=0)
    plt.xlabel("城市", fontproperties=font)
    plt.ylabel("雨量(mm)", fontproperties=font)
    plt.title("过去24小时累计降雨量全国前20名", fontproperties=font)
    
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + max(num_list) * 0.01, 
                str(round(height, 1)), ha="center", va="bottom", fontsize=8)
    
    plt.tight_layout()
    plt.savefig('rainfall_chart.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("累积降雨量图表已保存为 rainfall_chart.png")

def draw_temperature(temperature_list):
    """绘制日平均气温图表"""
    print("\n正在绘制日平均气温图表...")
    
    try:
        font = FontProperties(fname='simhei.ttf')
    except:
        font = FontProperties()
    
    name_list = []
    num_list = []
    date = str(temperature_list.iloc[0]['日期']) if len(temperature_list) > 0 else "未知日期"
    
    for _, item in temperature_list.iterrows():
        name_list.append(item['省份'][0:2] + '\n' + item['城市'])
        num_list.append(float(item['日平均气温(°C)']))
    
    index = [i + 0.25 for i in range(0, len(num_list))]
    rects = plt.bar(index, num_list, color='orange', width=0.5)
    
    plt.xticks([i + 0.25 for i in index], name_list, fontproperties=font, fontsize=8)
    plt.ylim(ymin=min(num_list) - 2, ymax=max(num_list) + 2)
    plt.xlabel("城市", fontproperties=font)
    plt.ylabel("日平均气温(°C)", fontproperties=font)
    plt.title(f"{date}全国日平均气温最低前10名", fontproperties=font)
    
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 0.2, 
                str(round(height, 1)), ha="center", va="bottom", fontsize=8)
    
    plt.tight_layout()
    plt.savefig('temperature_chart.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("日平均气温图表已保存为 temperature_chart.png")

def main():
    """主函数"""
    print("="*60)
    print("基于Pandas的气象数据处理与分析系统")
    print("="*60)
    
    # 加载数据
    data_file = "passed_weather_ALL.csv"
    df = load_weather_data(data_file)
    
    if df is None:
        print("数据加载失败，程序退出")
        return
    
    # 显示数据基本信息
    print(f"\n数据概况：")
    print(f"- 总记录数：{len(df)}")
    print(f"- 城市数量：{df['city_name'].nunique()}")
    print(f"- 省份数量：{df['province'].nunique()}")
    print(f"- 时间范围：{df['time'].min()} 到 {df['time'].max()}")
    
    try:
        # 任务1：计算累积雨量
        top_rainfall = task1_calculate_rainfall(df)
        
        # 任务2：计算日平均气温
        lowest_temperatures = task2_calculate_temperature(df)
        
        # 数据可视化
        if not top_rainfall.empty:
            draw_rain(top_rainfall)
        
        if not lowest_temperatures.empty:
            draw_temperature(lowest_temperatures)
        
        print("\n" + "="*60)
        print("分析完成！结果文件已保存到当前目录")
        print("- 累积雨量结果: rainfall_results.csv")
        print("- 平均气温结果: temperature_results.csv")
        print("- 图表文件: rainfall_chart.png, temperature_chart.png")
        print("="*60)
        
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()