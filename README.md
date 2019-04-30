# netease-stock-day-line
Python爬虫抓取网易财经日线

**下载：**
- download .zip to local
- `git clone https://github.com/CatsJuice/netease-stock-day-line.git`

**环境前提：**
- Python 3.x
- 第三方库支持（`import`中的所有库）

**使用：**

运行`dayline.py`

**目录结构说明：**

- classes
    - DbManage.py    // 数据库连接类
    - Downloader.py  // 下载器
    - Parser.py      // 解析器
    - Saver.py       // 存储器
- dayline.py: 抓取网易财经日线
- tushare_minute_data.py ： tushare分时数据抓取