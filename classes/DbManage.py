import pymysql

# 数据库
class DbManager(object):

    def __init__(self):
        self.name = "root"
        self.passsword = "98981010asd"
        self.conn = None
        self.db = None

    def connect(self):
        self.conn = pymysql.connect('localhost', self.name, self.passsword, charset='utf8')
        self.db = self.conn.cursor()

    def executeSqlTxt(self, sqlTxt):
        return self.db.execute(sqlTxt)

    def close(self):
        self.db.close()
        self.conn.close()