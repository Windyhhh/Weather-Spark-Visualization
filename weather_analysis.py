#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于Spark的气象数据处理与分析
计算城市累积雨量和日平均气温
"""

import os
import math
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def create_spark_session():
    """创建SparkSession"""
    spark = SparkSession.builder \
        .appName("WeatherAnalysis") \
        .master("local[*]") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark

def load_weather_data(spark, file_path):
    """加载气象数据"""
    print("正在加载气象数据...")
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    print(f"数据加载完成，共{df.count()}条记录")
    df.printSchema()
    return df

def task1_calculate_rainfall(spark, df):
    """任务1：计算各个城市过去24小时累积雨量"""
    print("\n" + "="*50)
    print("任务1：计算各个城市过去24小时累积雨量")
    print("="*50)
    
    # 步骤3：筛选字段，将rain1h转为数值型，过滤异常数据
    df_rain = df.select(
        "province", "city_name", "city_code", "rain1h"
    ).filter(
        col("rain1h") < 1000
    ).filter(
        col("rain1h").isNotNull()
    )
    
    # 步骤4：按城市分组，对rain1h求和并排序
    df_rain_sum = df_rain.groupBy("province", "city_name", "city_code") \
        .agg(sum("rain1h").alias("rain24h")) \
        .orderBy(desc("rain24h"))
    
    # 步骤5：缓存转换关系
    df_rain_sum.cache()
    
    # 步骤6：持久化到本地
    df_rain_sum.coalesce(1).write.mode("overwrite").csv("rainfall_results", header=True)
    
    # 步骤7：取前20条数据用于可视化
    top_rainfall = df_rain_sum.head(20)
    
    print(f"累积雨量计算完成，共{df_rain_sum.count()}个城市")
    print("前10名累积降雨量城市：")
    for i, row in enumerate(df_rain_sum.head(10), 1):
        print(f"{i:2d}. {row.province}-{row.city_name}: {row.rain24h}mm")
    
    return top_rainfall

def task2_calculate_temperature(spark, df):
    """任务2：计算各个城市当日平均气温"""
    print("\n" + "="*50)
    print("任务2：计算各个城市当日平均气温")
    print("="*50)
    
    # 步骤3：筛选字段并拆分时间字段
    df_temperature = df.select(
        "province", "city_name", "city_code", "temperature", "time"
    ).filter(
        col("temperature").isNotNull()
    ).filter(
        col("temperature") > -50
    ).filter(
        col("temperature") < 60
    )
    
    # 提取日期和小时字段
    df_temperature = df_temperature.withColumn("date", date_format(col("time"), "yyyy-MM-dd")) \
        .withColumn("hour", hour(col("time")))
    
    # 步骤4：过滤02、08、14、20时的数据
    df_4point_temperature = df_temperature.filter(
        col("hour").isin([2, 8, 14, 20])
    )
    
    # 步骤5：按城市和日期分组，计算平均气温
    df_avg_temperature = df_4point_temperature.groupBy(
        "province", "city_name", "city_code", "date"
    ).agg(
        count("temperature").alias("hour_count"),
        avg("temperature").alias("avg_temperature")
    ).filter(
        col("hour_count") == 4
    ).select(
        "province", "city_name", "city_code", "date", "avg_temperature"
    ).orderBy("avg_temperature")
    
    # 步骤6：缓存转换关系
    df_avg_temperature.cache()
    
    # 步骤7：持久化到本地
    df_avg_temperature.coalesce(1).write.mode("overwrite").json("temperature_results")
    
    # 步骤8：收集数据用于可视化
    lowest_temperatures = df_avg_temperature.head(10)
    
    print(f"日平均气温计算完成，共{df_avg_temperature.count()}个城市")
    print("前10名最低日平均气温城市：")
    for i, row in enumerate(lowest_temperatures, 1):
        print(f"{i:2d}. {row.province}-{row.city_name} ({row.date}): {row.avg_temperature:.1f}°C")
    
    return lowest_temperatures

def draw_rain(rain_list):
    """绘制累积降雨量图表"""
    print("\n正在绘制累积降雨量图表...")
    
    font = FontProperties(fname='simhei.ttf')
    name_list = []
    num_list = []
    
    for item in rain_list:
        name_list.append(item.province[0:2] + '\n' + item.city_name)
        num_list.append(item.rain24h)
    
    index = [i + 0.25 for i in range(0, len(num_list))]
    rects = plt.bar(index, num_list, color='rgby', width=0.5)
    
    plt.xticks([i + 0.25 for i in index], name_list, fontproperties=font)
    plt.ylim(ymax=(int(max(num_list) + 100) / 100) * 100, ymin=0)
    plt.xlabel("城市", fontproperties=font)
    plt.ylabel("雨量(mm)", fontproperties=font)
    plt.title("过去24小时累计降雨量全国前20名", fontproperties=font)
    
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, 
                str(round(height, 1)), ha="center", va="bottom")
    
    plt.tight_layout()
    plt.savefig('rainfall_chart.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("累积降雨量图表已保存为 rainfall_chart.png")

def draw_temperature(temperature_list):
    """绘制日平均气温图表"""
    print("\n正在绘制日平均气温图表...")
    
    font = FontProperties(fname='simhei.ttf')
    name_list = []
    num_list = []
    date = temperature_list[0].date if temperature_list else "未知日期"
    
    for item in temperature_list:
        name_list.append(item.province[0:2] + '\n' + item.city_name)
        num_list.append(float(item.avg_temperature))
    
    index = [i + 0.25 for i in range(0, len(num_list))]
    rects = plt.bar(index, num_list, color='rgby', width=0.5)
    
    plt.xticks([i + 0.25 for i in index], name_list, fontproperties=font)
    plt.ylim(ymax=math.ceil(float(max(num_list))), ymin=math.floor(float(min(num_list))) - 2)
    plt.xlabel("城市", fontproperties=font)
    plt.ylabel("日平均气温(°C)", fontproperties=font)
    plt.title(f"{date}全国日平均气温最低前10名", fontproperties=font)
    
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 0.1, 
                str(round(height, 1)), ha="center", va="bottom")
    
    plt.tight_layout()
    plt.savefig('temperature_chart.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("日平均气温图表已保存为 temperature_chart.png")

def main():
    """主函数"""
    print("="*60)
    print("基于Spark的气象数据处理与分析系统")
    print("="*60)
    
    # 创建SparkSession
    spark = create_spark_session()
    
    try:
        # 加载数据
        data_file = "passed_weather_ALL.csv"
        if not os.path.exists(data_file):
            print(f"错误：找不到数据文件 {data_file}")
            return
        
        df = load_weather_data(spark, data_file)
        
        # 任务1：计算累积雨量
        top_rainfall = task1_calculate_rainfall(spark, df)
        
        # 任务2：计算日平均气温
        lowest_temperatures = task2_calculate_temperature(spark, df)
        
        # 数据可视化
        if top_rainfall:
            draw_rain(top_rainfall)
        
        if lowest_temperatures:
            draw_temperature(lowest_temperatures)
        
        print("\n" + "="*60)
        print("分析完成！结果文件已保存到当前目录")
        print("- 累积雨量结果: rainfall_results/")
        print("- 平均气温结果: temperature_results/")
        print("- 图表文件: rainfall_chart.png, temperature_chart.png")
        print("="*60)
        
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        spark.stop()

if __name__ == "__main__":
    main()