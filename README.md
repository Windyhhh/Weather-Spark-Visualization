# 🌦️ 天气数据分析可视化 | Weather Spark Visualization

> **基于 Apache Spark 的天气大数据分析与可视化——气象数据处理、时空分析、趋势预测、可视化大屏。**
>
> *Weather big data analysis and visualization based on Apache Spark — meteorological data processing, spatio-temporal analysis, trend forecasting, visualization dashboard.*

---

## ⭐ 核心卖点 | Why Star This

| 卖点 | Feature | 一句话 |
|------|---------|--------|
| 🐘 **Spark 处理** | Spark Processing | 分布式处理海量气象数据 |
| 🌡️ **气象分析** | Meteorological | 温度、降水、风速多维分析 |
| 🗺️ **时空分析** | Spatio-Temporal | 空间 + 时间维度气象分析 |
| 📈 **趋势预测** | Trend Forecast | 气象要素变化趋势分析 |
| 📊 **可视化大屏** | Dashboard | ECharts 气象数据可视化 |

---

## 🏆 技术栈 | Tech Stack

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Apache Spark](https://img.shields.io/badge/Spark-3.0+-orange?logo=apachespark)
![PySpark](https://img.shields.io/badge/PySpark-3.0+-orange?logo=apachespark)
![Pandas](https://img.shields.io/badge/Pandas-1.3+-blue?logo=pandas)
![ECharts](https://img.shields.io/badge/ECharts-5.0+-orange?logo=apacheecharts)
![Flask](https://img.shields.io/badge/Flask-2.0+-black?logo=flask)

---

## 🚀 快速开始 | Quick Start

```bash
git clone https://github.com/Windyhhh/Weather-Spark-Visualization.git
cd Weather-Spark-Visualization

# 1. 安装依赖
pip install -r requirements.txt

# 2. 数据预处理
python src/preprocess.py --input data/weather.csv

# 3. Spark 气象分析
spark-submit src/spark_weather_analysis.py --data data/processed/

# 4. 趋势预测
python src/trend_forecast.py --data data/processed/

# 5. 启动可视化
python app.py --port 5000
# 访问 http://localhost:5000
```

---

## 📂 项目结构 | Project Structure

```
Weather-Spark-Visualization/
├── src/                       # 核心代码
│   ├── preprocess.py          # 数据预处理
│   ├── spark_weather_analysis.py # Spark 气象分析
│   ├── trend_forecast.py      # 趋势预测
│   └── temporal_analysis.py   # 时序分析
├── app.py                     # 可视化应用
├── frontend/                  # 可视化前端
├── data/                      # 数据
└── requirements.txt
```

---

## 🔬 核心实现 | Core Implementation

### Spark 气象分析 | Spark Weather Analysis

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max, min, month, desc

def weather_analysis(data_path):
    spark = SparkSession.builder.appName("Weather-Analysis").getOrCreate()
    df = spark.read.csv(data_path, header=True, inferSchema=True)
    
    # 1. 城市平均温度
    city_temp = df.groupBy("city") \
        .agg(avg("temperature").alias("avg_temp"),
             max("temperature").alias("max_temp"),
             min("temperature").alias("min_temp"))
    
    # 2. 月度降水分析
    df = df.withColumn("month", month(col("date")))
    monthly_rain = df.groupBy("month") \
        .agg(avg("rainfall").alias("avg_rainfall"))
    
    # 3. 极端天气统计
    extreme = df.filter(col("temperature") > 35 | col("temperature") < -10)
    
    return city_temp, monthly_rain, extreme
```

---

## 📊 可视化看板 | Dashboard

```
🌦️ 全国气象数据分析
┌────────────┬────────────┬────────────┐
│ 平均温度 15℃│ 平均降水 85mm│ 极端天气 12次│
├────────────┴────────────┴────────────┤
│ 📈 城市温度排行    │ 📊 月度降水趋势     │
│  广州 28℃        │  1月 ██  2月 ███   │
│  上海 22℃        │  3月 ████ 4月 █████│
│  北京 18℃        │  5月 ████ 6月 ██████│
└──────────────────┴───────────────────┘
```

---

## 🎯 应用场景 | Use Cases

- 🌍 **气象部门**：气象数据分析
- 🏙️ **城市管理**：气候与城市规划
- 🎓 **大数据教学**：Spark 气象分析项目
- 📊 **农业气象**：农业气象决策支持

---

## 📄 License

MIT License — 自由使用、修改和分发。

---

> 💡 **Spark 天气大数据可视化，Star ⭐ 洞察气象万象！**
