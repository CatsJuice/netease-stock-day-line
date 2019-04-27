import urllib

# 下载器
class Downloader(object):

    def __init__(self, url):
        self.url = url

    def download(self):
        html_content = urllib.request.urlopen(self.url).read()
        html_content = html_content.decode("utf-8")
        return html_content