import random
import time

from stock.classes.Downloader import Downloader
from stock.classes.Parser import Parser
from stock.classes.Saver import Saver

# 控制器
class Controller(object):

    # 构造函数
    def __init__(self, url, kline_filepath, codelist_filepath, date):
        '''
        :param url: 股票基本信息url（ 股城网>行情>沪深A股 ）
        :param kline_filepath:  日线数据文件保存路径
        :param codelist_filepath:  股票代码文件保存路径
        :param date:  查询截止日期
        '''
        self.url = url
        self.kline_filepath = kline_filepath
        self.codelist_filepath = codelist_filepath
        self.date = date
        self.downloader = None  # 下载器实例
        self.parser = None      # 解析器实例
        self.saver = Saver()    # 存储器实例

    # 执行函数
    def start(self):
        page = 6
        all_code = []
        while page <= 181:
            print("当前为第%s页" % page)
            time.sleep(random.random())
            self.downloader = Downloader(self.url % page)
            page += 1
            html_content = self.downloader.download()
            self.parser = Parser(html_content)
            codeList = self.parser.parseSharesCode()
            for code in codeList:
                all_code.append(code)
            # print(codeList)
            self.saver.saveKlineToCSV(codeList=codeList, filepath=self.kline_filepath, date=self.date)
        self.save(codelist=all_code)

    def save(self,codelist):
        self.saver.saveCodeListToCSV(codeList=codelist, filepath=self.codelist_filepath)    # 保存代码到csv
        # self.saver.saveKlineToMySQL(filepath=self.kline_filepath)                         # 保存所有股票的信息到数据库


# 程序入口
if __name__ == '__main__':
    url = 'https://hq.gucheng.com/HSinfo.html?en_hq_type_code=&sort_field_name=px_change_rate&sort_type=desc&page=%s'   # 股城网>行情>沪深A股
    kline_filepath = 'F:\\files\\sharesDatas\\kline\\'                  # 定义数据文件保存路径
    codelist_filepath = 'F:\\files\\sharesDatas\\code_list\\'           # 定义数据文件保存路径
    controller = Controller(url=url, kline_filepath=kline_filepath, codelist_filepath=codelist_filepath, date='20190428')
    controller.start()