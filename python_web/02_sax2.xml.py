import xml.sax

# 创建一个person类
class person(object):

    def __init__(self,name,age):
        self.name = name
        self.age = age

    def __str__(self):
            return 'Person Name: {s.name},Person Age: {s.age}'.format(s = self)


# 创建一个MyHandler类继承xml.sax.ContentHandler
class MyHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.persons = []


    def startElement(self, tag_name, tag_attrs):
        if tag_name == 'person':
            # print(tag_name,tag_attrs['name'],tag_attrs['age'])
            # 创建person对象并加入persons列表中
            self.persons.append(person(tag_attrs["name"],tag_attrs["age"]))
    def endElement(self, tag_name):
        pass

    def characters(self, content):
        pass


if __name__ == '__main__':
    # 创建一个XMLReader
    parser = xml.sax.make_parser()
    # 关闭命名空间
    parser.setFeature(xml.sax.handler.feature_namespaces,0)
    # 创建一个解析对象
    handler = MyHandler()
    parser.setContentHandler(handler)
    # 解析文档
    parser.parse("people2.xml")

    for i in handler.persons:
        print(i)