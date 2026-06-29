import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("output", exist_ok=True)

# 月度趋势
monthly = pd.read_csv("output/result_monthly_avg.csv")
if not monthly.empty:
    plt.figure()
    plt.plot(monthly['month'], monthly['avg_streams'], marker='o')
    plt.xlabel('Month')
    plt.ylabel('Average Streams')
    plt.title('Monthly Average Streams in 2024')
    plt.grid(True)
    plt.savefig('output/monthly_trend.png')
    plt.close()

# Top10 歌曲
top_songs = pd.read_csv("output/result_top10_songs.csv")
if not top_songs.empty:
    plt.figure(figsize=(10, 6))
    plt.barh(top_songs['track_name'], top_songs['total_streams'], color='skyblue')
    plt.xlabel('Total Streams')
    plt.title('Top 10 Songs by Streams')
    plt.tight_layout()
    plt.savefig('output/top10_songs.png')
    plt.close()

# Top10 歌手
top_artists = pd.read_csv("output/result_top10_artists.csv")
if not top_artists.empty:
    plt.figure(figsize=(10, 6))
    plt.barh(top_artists['artist_names'], top_artists['total_streams'], color='lightgreen')
    plt.xlabel('Total Streams')
    plt.title('Top 10 Artists by Streams')
    plt.tight_layout()
    plt.savefig('output/top10_artists.png')
    plt.close()

# 在榜周数
weeks = pd.read_csv("output/result_weeks_on_chart.csv")
if not weeks.empty:
    top10_weeks = weeks.head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top10_weeks['track_name'], top10_weeks['max_weeks_on_chart'], color='coral')
    plt.xlabel('Max Weeks on Chart')
    plt.title('Top 10 Songs by Weeks on Chart')
    plt.tight_layout()
    plt.savefig('output/weeks_on_chart.png')
    plt.close()
# 5. 排名变化趋势（top 歌曲排名变化）
trend = pd.read_csv("output/result_trend_analysis.csv")
if not trend.empty and 'date' in trend.columns and 'rank' in trend.columns:
    # 按日期排序（字符串日期可直接排序）
    trend_sorted = trend.sort_values('date')
    plt.figure(figsize=(12, 5))
    plt.plot(trend_sorted['date'], trend_sorted['rank'], marker='o', linestyle='-', color='purple')
    plt.gca().invert_yaxis()  # 排名越小越好，倒置Y轴
    plt.xlabel('Date')
    plt.ylabel('Rank')
    plt.title(f'Ranking Trend for Top Song')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/trend_analysis.png')
    plt.close()
# 6. 相关性散点图
corr_data = pd.read_csv("output/song_weeks_streams.csv")
if not corr_data.empty:
    plt.figure(figsize=(10, 6))
    plt.scatter(corr_data['max_weeks'], corr_data['total_streams'], alpha=0.3, s=10)
    plt.xlabel('Max Weeks on Chart')
    plt.ylabel('Total Streams')
    # 读取相关系数
    try:
        with open("output/correlation_result.txt", "r") as f:
            corr_text = f.read().strip()
        plt.title(f'Correlation: {corr_text}')
    except:
        plt.title('Weeks vs Streams')
    plt.grid(True)
    plt.savefig('output/correlation_scatter.png')
    plt.close()
# ---- 7. 每周新上榜歌曲数量（扩展分析） ----
new_songs = pd.read_csv("output/new_songs_per_week.csv")
if not new_songs.empty:
    # 生成“年-周”标签
    new_songs['year_week'] = new_songs['year'].astype(str) + '-W' + new_songs['week'].astype(str)
    
    plt.figure(figsize=(14, 6))
    plt.bar(new_songs['year_week'], new_songs['new_songs'], color='teal', alpha=0.7)
    plt.xlabel('Year-Week')
    plt.ylabel('Number of New Songs')
    plt.title('New Songs Entering Chart per Week')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('output/new_songs_per_week.png')
    plt.close()
print("所有可视化图表已生成到 output/ 目录")