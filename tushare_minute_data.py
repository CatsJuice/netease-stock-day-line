import random
import time

import pandas as pd
from tqdm import tqdm
import tushare as ts
import os

class TickData(object):

    def __init__(self, kline_prefix, tick_prefix, latest_date, days=10):
        self.kline_prefix = kline_prefix        # 日线目录前缀
        self.tick_prefix = tick_prefix          # 分时数据目录前缀
        self.latest_date = latest_date          # 最新日期
        self.days = days                        # 要抓取的天数

    def get_tick_data(self):
        # 1. 读取所有日线列表， 获取股票代码和股票日期
        fileList = os.listdir(self.kline_prefix)
        start = False
        for j in tqdm(range(len(fileList))):
            filename = fileList[j]
            if filename == '600146.csv':
                start = True
                continue
            elif not start:
                continue
            code = filename[0:6]
            try:
                df = pd.read_csv(self.kline_prefix + filename, encoding="gbk")
            except:
                print("Error while open file: " + filename)
                continue
            # 2. 验证数据完整性
            # 2.1 数据是否足够长
            # 2.2 第一个日期是否是当前最新的， 不是的话忽略
            if len(df[0:self.days].values) < self.days or df[0:1].values[0][0] != self.latest_date:
                continue
            # 3. 为当前股票创建文件夹
            # 3.1 判断是否存在不存在则创建
            if not os.path.exists(self.tick_prefix + code):
                os.makedirs(self.tick_prefix + code)
            new_tick_prefix = tick_prefix + str(code) + "\\"
            # 遍历筛选后的 行
            print(" [Downloading...]" + str(code)+"下载中", end=' ')
            count = 1
            for item in df[0:self.days].values:
                date = item[0]
                # 4. 下载分时数据
                data = ts.get_tick_data(code, date=date, src='tt')
                date_str = date.replace('-', '')
                data.to_csv(new_tick_prefix + str(date_str) + '.csv')
                print("#"+str(count), end=' ')
                count += 1
                time.sleep(random.random()*1)


if __name__ == '__main__':
    kline_prefix = "F:\\files\\sharesDatas\\kline\\"                 # 日线目录前缀
    tick_prefix = "F:\\files\\sharesDatas\\tushare_tick_data\\"      # 分时数据目录前缀
    days = 20       # 要抓取的天数
    latest_date = '2019-04-26'
    tick_data = TickData(kline_prefix, tick_prefix, latest_date, days)
    tick_data.get_tick_data()