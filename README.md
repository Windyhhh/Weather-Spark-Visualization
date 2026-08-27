<div align="center">

# 🌦️ Weather-Spark-Visualization

### Weather data analysis & visualization.

Spark big-data processing with meteorological analysis and charts.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Spark-3-E25A1C?logo=apachespark&logoColor=white)](https://spark.apache.org/)

</div>

---

**Weather-Spark-Visualization** analyzes weather data with **Apache Spark**, producing meteorological insights and charts (temperature, rainfall).

> [!NOTE]
> 中文项目：天气数据分析可视化——Spark 大数据处理，气象分析。

---

## Quickstart

```bash
git clone https://github.com/Windyhhh/Weather-Spark-Visualization.git
cd Weather-Spark-Visualization

pip install -r requirements.txt

# full analysis
python weather_analysis.py

# simplified version
python weather_analysis_simple.py
```

Results export to CSV + PNG (temperature/rainfall charts).

---

## Features

- **Spark processing** — distributed weather analytics.
- **Meteorological analysis** — temperature and rainfall.
- **Visualization** — chart outputs.

---

## Project Structure

```
Weather-Spark-Visualization/
├── weather_analysis.py
├── weather_analysis_simple.py
├── passed_weather_ALL.csv     # input data
├── temperature_results.csv / rainfall_results.csv
└── temperature_chart.png / rainfall_chart.png
```

---

## License

MIT — free to use, modify and distribute.
