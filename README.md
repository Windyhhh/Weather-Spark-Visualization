# 🌦️ Weather Spark Visualization | 气象数据分析与可视化（Spark）

> **Big data processing and visualization of meteorological data using Apache Spark. Temperature, precipitation, wind analysis, climate trends, anomaly detection. Spark SQL + Python visualization (matplotlib/plotly).**
>
> 基于 Apache Spark 的气象数据大数据处理与可视化。温度、降水、风场分析、气候趋势、异常检测。Spark SQL + Python 可视化（matplotlib/plotly）。

---

## 🌟 Features | 核心特性

- **Apache Spark** — Large-scale meteorological data processing
- **Temperature Analysis** — Trends, extremes, seasonality
- **Precipitation Analysis** — Rainfall patterns, drought detection
- **Wind Analysis** — Wind speed/direction, wind energy potential
- **Climate Trends** — Long-term climate change analysis
- **Anomaly Detection** — Extreme weather event identification
- **Visualization** — Maps, time series, heatmaps

---

## 🚀 Quick Start | 快速开始

```bash
# Process weather data with Spark
spark-submit weather_analysis.py --input weather_data.csv --output results/

# Generate visualizations
python visualize_weather.py --results results/ --output charts/

# Specific analysis
spark-submit temperature_trends.py --year 2023
spark-submit precipitation_analysis.py --region china
```

---

## 📊 Data Dimensions | 数据维度

| Element | Metrics |
|---------|---------|
| **Temperature** | Max, min, avg, diurnal range, degree days |
| **Precipitation** | Total, intensity, frequency, dry/wet spells |
| **Wind** | Speed, direction, gust, wind power density |
| **Humidity** | Relative humidity, dew point |
| **Pressure** | Sea level pressure, pressure tendency |
| **Sunshine** | Sunshine duration, cloud cover |

---

## 📄 License | 许可证

MIT License.

[GitHub](https://github.com/Windyhhh/Weather-Spark-Visualization)
