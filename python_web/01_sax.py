# __auther__ = hummer
'''
SAX解析（效率高，边读取边解析，不能重复解析）

1.创建一个XMLReader：parser = xml.sax.make_parser()

2.编写一个类继承xml.sax.ContentHandler类,并重写startElement（开始），endElement（结束），characters(接受内容)

3.实例化解析对象:parser.setContentHandler(解析对象)

4.调用解析方法：parser.parse("文档.xml")
'''

import xml.sax

# 2.编写一个类继承xml.sax.ContentHandler类,并重写startElement（开始），endElement（结束），characters(接受内容)
class MyHandler(xml.sax.ContentHandler):

    # 初始化对象属性
    def __init__(self):
        self.name = ''
        self.age = 0
        self.current_tag = ''

    def startElement(self, tag_name, tag_attrs):
        # print('解析开始----------start>',tag_name,tag_attrs)
        # 只处理节点信息
        if 'name' == tag_name:
            # print(tag_name)
            self.current_tag = tag_name

        if 'age' == tag_name:
            # print(tag_name)
            self.current_tag = tag_name

    def endElement(self, tag_name):
        # print('解析结束---------->',tag_name)
        if tag_name == 'name':
            print("Person Name: ",self.name)
        if tag_name == 'age':
            print("Person Age: ",self.age)

    def characters(self, content):
        # print('获取内容->',content)
        if self.current_tag == 'name':
            self.name = content
        if self.current_tag == 'age':
            self.age = content

if __name__ == '__main__':
    # 1.创建一个XMLReader：parser = xml.sax.make_parser()
    parser = xml.sax.make_parser()

    # 关闭命名空间解析
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 3.实例化解析对象
    handler = MyHandler()
    parser.setContentHandler(handler)

    # 4.解析文档
    parser.parse("people.xml")