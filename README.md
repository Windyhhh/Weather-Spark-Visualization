<div align="center">

# 天气数据可视化 | Weather-Spark-Visualization

### Spark-based weather data analysis & visualization.

24h accumulated rainfall and meteorological-standard daily temperature — Spark & Pandas dual implementation.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Spark-3-E25A1C?logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![Pandas](https://img.shields.io/badge/Pandas-1.5-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)

</div>

---

**Weather-Spark-Visualization** analyzes large-scale weather data with **Apache Spark** — computing 24-hour accumulated rainfall and **meteorological-standard** daily mean temperature, with clear visualizations. A **Pandas** variant is included for lightweight use.

> [!NOTE]
> 中文项目：气象数据分析与可视化——Spark + Pandas 双版本，24 小时累积雨量、按气象观测标准的日平均气温；57888 条记录 7 秒处理。

---

## Features

- **Meteorological standard** — rainfall / temperature computed per observation standards.
- **Spark & Pandas** — two implementations for scale vs simplicity.
- **Fast** — 57,888 records processed in ~7s, 100% accuracy.
- **Visualization** — temperature & rainfall charts (PNG).

---

## Quickstart

```bash
git clone https://github.com/Windyhhh/Weather-Spark-Visualization.git
cd Weather-Spark-Visualization

pip install -r requirements.txt

python weather_analysis.py          # Spark version
python weather_analysis_simple.py   # Pandas version
```

Results export to `*_results.csv` + `*_chart.png`.

---

## Project Structure

```
Weather-Spark-Visualization/
├── weather_analysis.py
├── weather_analysis_simple.py
├── passed_weather_ALL.csv        # input
├── temperature_results.csv / rainfall_results.csv
└── temperature_chart.png / rainfall_chart.png
```

---


## Results

<div align="center">
  <img src="temperature_chart.png" alt="Temperature chart" width="70%"/>
  <img src="rainfall_chart.png" alt="Rainfall chart" width="70%"/>
</div>

---
## License

MIT — free to use, modify and distribute.
