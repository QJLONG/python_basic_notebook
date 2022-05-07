from bs4 import BeautifulSoup
import requests,sys

# 获取每一张的文本内容
class novel_dowloader:
    novel_name = ''

    def __init__(self,server,target):
        self.server = server
        self.target = target


    def get_content(self,target):
        target = target
        req = requests.get(target)
        html = req.text
        bf = BeautifulSoup(html,features="html5lib")
        texts = bf.find_all('div',class_ = 'showtxt')
        text = str(texts[0]).replace(
            '<div class="showtxt" id="content"><script>app2();</script><br/><script>read2();</script>', '')
        text = text.replace('<br/><br/>','\n\n')
        return text

    # 获取每一章的链接：
    def get_urls(self,url):
        target = url
        req = requests.get(target)
        req.encoding = 'gbk'
        html = req.text
        bf = BeautifulSoup(html,features='lxml')
        url_html= str(bf.find_all('div',class_ = 'listmain'))
        url_bf =  BeautifulSoup(url_html,features='lxml')
        urls = url_bf.find_all('a')
        urls_dic = {}
        urls_dic['name']=[]
        urls_dic['url']=[]
        for each in urls:
            urls_dic['name'].append(each.text)
            urls_dic['url'].append(self.server+each.get('href'))
        return urls_dic

    #获取小说名
    def get_name(self,url):
        req = requests.get(url)
        req.encoding = 'gbk'
        html = req.text
        bf = BeautifulSoup(html,features='html5lib')
        title = bf.find('h2')
        return title.text

    #将文本内容保存到本地（当前文件夹）
    def write_novel(self,name,path,content):
        if not path:
            path = 'novel1'

        with open(path,'a',encoding='utf-8') as f:
            f.write(name+'\n')
            f.writelines(content)
            f.write('\n\n')


if __name__ == '__main__':
    url = input('please input the url:')
    server = 'https://www.bqktxt.com'
    dl = novel_dowloader(server=server,target='')
    name = '《' +dl.get_name(url) + '》'
    urls = dl.get_urls(url)
    print(name+'开始下载：')
    for i in range(len(urls['url'])):
        dl.write_novel(urls['name'][i],name + '.txt',dl.get_content(urls['url'][i]))
        sys.stdout.write(" 已下载：%.3f%% " %float(i/len(urls['name'])) + '\r')
        sys.stdout.flush()
    print(name+'下载完成！')
