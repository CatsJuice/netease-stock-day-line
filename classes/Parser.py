from bs4 import BeautifulSoup

# 解析器
class Parser(object):

    def __init__(self, html_content):
        self.html_content = html_content

    def parse(self):
        return self.parseSharesCode()

    def parseSharesCode(self):
        '''
        :return: 股票代码数组
        '''
        soup = BeautifulSoup(self.html_content, 'html.parser', from_encoding="utf-8")
        all_tr = soup.find('table',class_='stock_table').find_all('tr')
        codeList = []
        for tr in all_tr:
            tds = tr.find_all('td')
            if len(tds) == 0:
                continue
            td = tds[1]
            code = td.find('a').get_text()
            # print(code)
            if code[0] == '6':
                code = "0" + code
            elif code[0] == '3' or code[0] == '0':
                code = '1' + code
            codeList.append(code)
        return codeList

    def end(self):
        pass