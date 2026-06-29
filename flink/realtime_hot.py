from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import ReduceFunction
from pyflink.datastream.window import TumblingProcessingTimeWindows, Time
from pyflink.common.typeinfo import Types
import pandas as pd

# 1. 创建流环境
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

# 2. 读取 CSV 数据，构造 (track_name, streams) 元组列表
df = pd.read_csv("file:///spotify-analysis/data/spotify.csv")
data = [(row['track_name'], int(row['streams'])) for _, row in df.iterrows()]

# 3. 创建 DataStream
stream = env.from_collection(data, type_info=Types.TUPLE([Types.STRING(), Types.LONG()]))

# 4. 自定义 ReduceFunction 求和
class SumReduce(ReduceFunction):
    def reduce(self, value1, value2):
        # value1 和 value2 都是 (track_name, streams) 元组
        return (value1[0], value1[1] + value2[1])

# 5. 按歌曲分组 -> 开 1 秒滚动窗口 -> 聚合求和
windowed = stream.key_by(lambda x: x[0]) \
                 .window(TumblingProcessingTimeWindows.of(Time.seconds(1))) \
                 .reduce(SumReduce())

# 6. 打印结果
windowed.print()

# 7. 执行作业
env.execute("Flink Realtime Simulation")