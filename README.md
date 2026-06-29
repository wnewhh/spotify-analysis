
# Spotify Global Chart 2024 数据分析

本项目基于 Kaggle 数据集 [Spotify Global Chart 2024](https://www.kaggle.com/datasets/federicocester97/spotify-global-chart-2024)，使用 Hadoop HDFS 存储数据，并利用 **Apache Spark** 和 **Apache Flink** 两种计算框架完成分析。实现了播放量 Top10、月度热度、在榜周数、排名趋势等基础指标，并增加了相关性分析和每周新歌统计等扩展分析，同时包含可视化图表和框架对比。

---

## 项目结构
```
spotify-analysis/
├── data/
│   ├── Spotify Global Chart 2024.xlsx   # 原始数据
│   └── spotify.csv                      # 预处理后的 CSV（全量数据）
├── hdfs/
│   └── upload.sh                        # 上传数据到 HDFS 脚本
├── spark/
│   ├── top_songs.py                     # 播放量最高歌曲 Top10
│   ├── top_artists.py                   # 播放量最高歌手 Top10
│   ├── monthly_trend.py                 # 月度热度变化
│   ├── weeks_on_chart.py                # 在榜周数统计
│   ├── trend_analysis.py                # 最热歌曲排名趋势
│   ├── correlation_analysis.py          # 歌曲的“在榜最大周数”与“总播放量”相关性分析
│   └── new_songs_per_week.py            # 每周新歌统计
├── flink/
│   ├── batch_top10.py                   # Flink 批处理（与 Spark 对比）
│   └── realtime_hot.py                  # Flink 流处理模拟
├── output/
│   ├── result_top10_songs.csv           # Spark：Top10 歌曲
│   ├── result_top10_artists.csv         # Spark：Top10 歌手
│   ├── result_monthly_avg.csv           # Spark：月度平均播放量
│   ├── result_weeks_on_chart.csv        # Spark：在榜周数 Top20
│   ├── result_trend_analysis.csv        # Spark：最热歌曲排名变化
│   ├── song_weeks_streams.csv           # 每首歌总播放量 & 最大在榜周数
│   ├── correlation_result.txt           # 相关系数
│   ├── new_songs_per_week.csv           # 每周新歌数
│   ├── result_top10_flink.csv           # Flink：Top10 歌曲（与 Spark 对比）
│   └── *.png                            # 7 张可视化图表
├── preprocess.py                        # 数据预处理
├── visualize.py                         # 生成图表
└── README.md
```
---

## 技术栈

- **存储**：Hadoop HDFS 3.3.5
- **批处理**：Apache Spark 3.4.0 (PySpark)
- **流处理模拟**：Apache Flink 1.18.1 (PyFlink)
- **数据处理**：Pandas, NumPy
- **可视化**：Matplotlib
- **环境**：Ubuntu 22.04, Python 3.11

---

## 环境依赖

```bash
# Hadoop、Spark、Flink（已配置）
hadoop version
spark-submit --version
flink --version

# Python 库
pip install pandas openpyxl matplotlib seaborn pyspark apache-flink
```

---

## 运行步骤

### 1. 数据预处理
```bash
python preprocess.py
```
生成 `data/spotify.csv`（列：`date, Source.Name, rank, uri, artist_names, track_name, source, peak_rank, previous_rank, weeks_on_chart, streams`）。  
本次使用全量数据（10,600 条记录）。

### 2. 启动 HDFS 并上传数据
```bash
start-dfs.sh
hdfs dfs -mkdir -p /user/wne/input
hdfs dfs -put -f data/spotify.csv /user/wne/input/
```

### 3. 运行 Spark 作业
```bash
spark-submit spark/top_songs.py
spark-submit spark/top_artists.py
spark-submit spark/monthly_trend.py
spark-submit spark/weeks_on_chart.py
spark-submit spark/trend_analysis.py          
spark-submit spark/correlation_analysis.py    
spark-submit spark/new_songs_per_week.py      
```
> 内存不足时可加 `--driver-memory 4g --executor-memory 4g`。

### 4. 运行 Flink（加分项）
#### 批处理对比（+2 分）
```bash
python flink/batch_top10.py
```
生成 `output/result_top10_flink.csv`，与 Spark 结果对比。

#### 流处理模拟（+3 分）
```bash
python flink/realtime_hot.py
```
使用 1 秒滚动窗口，打印每首歌的播放量总和，截图可作为流处理证明。

### 5. 生成可视化
```bash
python visualize.py
```
输出 7 张 PNG 图片，全部保存在 `output/` 目录。

---

## 结果汇总

| 指标 | 输出文件 | 说明 |
|------|----------|------|
| 播放量最高歌曲 Top10 | `result_top10_songs.csv` | 按总播放量降序 |
| 播放量最高歌手 Top10 | `result_top10_artists.csv` | 按总播放量降序 |
| 月度热度变化 | `result_monthly_avg.csv` | 各月平均播放量 |
| 在榜周数统计 | `result_weeks_on_chart.csv` | 每首歌最大在榜周数 Top20 |
| 排名变化趋势 | `result_trend_analysis.csv` | 最热歌曲每日排名变化 |
| 相关性分析 | `correlation_result.txt` + `song_weeks_streams.csv` | 相关系数 0.454 |
| 每周新歌数 | `new_songs_per_week.csv` | 每周首次上榜歌曲数量 |
| Flink 对比结果 | `result_top10_flink.csv` | 与 Spark 结果一致 |

---

## 框架对比（Spark vs Flink）

- **结果一致性**：Spark 与 Flink 批处理的 Top10 完全相同，验证计算正确性。
- **性能**：本地环境中两者执行时间相近，但 Flink 在流处理场景下延迟更低。

---

## 报告

项目报告 `report.pdf` 包含背景、数据集说明、技术路线、HDFS 操作、预处理、核心算法、结果分析、分工及总结，并附所有图表。



## 注意事项

- 运行 Spark 前确保 HDFS 已启动且数据已上传。
- 路径可根据实际调整（当前为 `/home/wne/spotify-analysis/`）。
- 若数据量过大，可提高 Spark 内存配置或减少抽样比例。

---

## 许可证

仅供课程作业使用，数据来源于 Kaggle，遵循其许可协议。

