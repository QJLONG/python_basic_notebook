import xml.dom.minidom

# 获取xml文档树
dom_tree = xml.dom.minidom.parse('people.xml')
#print(dom_tree)

# 获取所有节点
root = dom_tree.documentElement
# 获取所有peoson节点
persons = root.getElementsByTagName('person')

# 获取person节点中的name，age节点
for p in persons:
    name = p.getElementsByTagName('name')
    age = p.getElementsByTagName('age')
    # 注意获取的子节点都是列表
    print('姓名：',name[0].childNodes[0].data)
    print('年龄： ',age[0].childNodes[0].data)