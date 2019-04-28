import os
import pandas as pd
import numpy as np
import random
import pymysql
import time
import urllib
import http.client
import csv
import requests

from stock.classes.DbManage import DbManager

# 存储器
class Saver(object):

    def __init__(self):
        self.db = DbManager()

    # 存日线到.CSV
    def saveKlineToCSV(self, codeList, filepath, date):
        '''
        存储为CSV文件，传入股票代码列表
        :param codeList:
        :return:
        '''
        for code in codeList:
            http.client.HTTPConnection._http_vsn = 10
            http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
            print('正在获取股票%s数据' % code[1:])
            url = 'http://quotes.money.163.com/service/chddata.html?code=%s&end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP' % (code, date)
            urllib.request.urlretrieve(url, filepath+code[1:]+'.csv')
            # r = requests.get(url)
            # with open(filepath+code+'.csv', "wb") as content:
            #     content.write(r.content)
            time.sleep(random.random() * 1)

    # 存日线到MySQL
    def saveKlineToMySQL(self, filepath):
        # 连接数据库
        name = "your-data-base-username"
        passsword = "your-password"
        db = pymysql.connect('localhost', name, passsword, charset='utf8')
        cursor = db.cursor()

        # 创建数据库shares
        cursor.execute('create database if not exists shares')
        cursor.execute('use shares')
        fileList = os.listdir(filepath)

        # 遍历保存的csv文件
        for filename in fileList:
            data = pd.read_csv(filepath + filename, encoding="gbk")
            # 创建数据表，若存在则跳过
            try:
                print('正在创建数据表stock_%s' % filename[0:6])
                sqlTxt = "create table shares_%s" % filename[0:6] + "(日期 date, 股票代码 VARCHAR(10),     名称 VARCHAR(10),\
                           收盘价 float,    最高价    float, 最低价 float, 开盘价 float, 前收盘 float, 涨跌额    float, \
                           涨跌幅 float, 换手率 float, 成交量 bigint, 成交金额 bigint, 总市值 bigint, 流通市值 bigint)"
                cursor.execute(sqlTxt)
            except:
                print("数据表已存在")

            # 遍历读取数据进行存储
            print('正在存储shares_%s' % filename[0:6])
            length = len(data)
            for i in range(length):
                record = tuple(data.loc[i])

                # 插入数据
                try:
                    sqlTxt2 = "INSERT INTO `shares_%s` " % filename[0:6] + "(日期, 股票代码, 名称, 收盘价, 最高价, 最低价, 开盘价, 前收盘, 涨跌额, 涨跌幅, 换手率, 成交量, 成交金额, 总市值, 流通市值) values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
                    sqlTxt2 = sqlTxt2.replace('nan', 'null').replace('None', 'null').replace('none', 'null')
                    cursor.execute(sqlTxt2)
                except:
                    break
        cursor.close()
        db.commit()
        db.close()

    # 存股票代码到.CSV
    def saveCodeListToCSV(self, codeList, filepath):

        with open(filepath+"6.csv", 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for code in codeList:
                csv_writer.writerow(code)

    # 矩阵转置
    def trans(self, m):
        for i in range(len(m)):
            for j in range(i):
                m[i][j], m[j][i] = m[j][i], m[i][j]
        return m

    # 存财务数据到.CSV
    def saveCwDataToCSV(self, filepath, uri):

        fileList = os.listdir('F:\\files\\sharesDatas\\kline\\')
        for filename in fileList:
            # 设置HTTP协议为1.0
            http.client.HTTPConnection._http_vsn = 10
            http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

            code = filename[0:6]
            print('正在获取股票%s财务数据' % code)
            url = uri % code
            r = requests.get(url)
            with open(filepath+ "temp\\" + code + '.csv', "wb") as content:
                content.write(r.content)

            # 对刚保存的.csv进行处理（转置）
            filename = filepath+'temp\\'+code +'.csv'
            data = pd.read_csv(filename, encoding="gbk")

            arr = []
            head = list(data.columns)
            head.pop()
            arr.append(head)
            for i in range(len(data)) :
                temp_arr = list(data.loc[i])
                temp_arr.pop()
                arr.append(temp_arr)

            new_data = np.transpose(arr).tolist()  # 矩阵转置，并转为list

            # 重新写入.csv生成新的文件
            out = open(filepath + code + '.csv', 'a', newline='')
            csv_write = csv.writer(out, dialect='excel')
            for row in new_data:
                csv_write.writerow(row)

            time.sleep(random.random() * 1)

    # 存财务数据到MySQL
    def saveCwDataToMySQL(self, filepath):
        pass