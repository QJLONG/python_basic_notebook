'''DOM解析
    1.在内存中创建一个文档 doc = xml.com.minidom.Document()
    2.创建爱你一个根节点：root = doc.createElement('节点名')
    3.将根节点添加到文档对象中：doc.appendChild(root)
    4.创建子节点并添加到根节点中：root.appendChild(子节点)
    5.写出xml文档：doc.writexml(文件,indent="\n",addindent="\t",encoding="utf-8")
'''

import xml.dom.minidom


# 1.在内存中创建一个文档 doc = xml.com.minidom.Document()
doc = xml.dom.minidom.Document()

# 2.创建爱你一个根节点：root = doc.createElement('节点名')
root = doc.createElement('people')

# 设置根节点的属性 id="people"
root.setAttribute("id","people")

# 3.将根节点添加到文档对象中：doc.appendChild(root)
doc.appendChild(root)

# 4.创建子节点并添加到根节点中：root.appendChild(子节点)
# 准备数据
data = [{'name':'王晶晶','age':28},{'name':'至尊宝','age':300}]

# 循环创建子节点和文本节点
for i in data:
    # 创建节点person
    node_person = doc.createElement('people')

    # 创建节点name
    node_name = doc.createElement('name')
    # 创建name的文本节点
    node_name.appendChild(doc.createTextNode(i['name']))

    node_person.appendChild(node_name)

    # 创建节点age
    node_age = doc.createElement('age')
    # 创建age的文本节点
    node_age.appendChild(doc.createTextNode(str(i['age'])))

    node_person.appendChild(node_age)

    root.appendChild(node_person)

# 5.写出xml文档：doc.writexml(文件,indent="\n",addindent="\t",encoding="utf-8")
with open('people_create.xml','w',encoding='utf-8') as f:
    doc.writexml(f,indent='\n',addindent='\t',encoding='utf-8')