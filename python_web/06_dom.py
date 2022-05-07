import xml.dom.minidom

dom_tree = xml.dom.minidom.parse('movie.xml')

# 获取所有movie节点
movies = dom_tree.getElementsByTagName('movie')

for m in movies:
    title = m.getAttribute('title')
    print('电影名：',title)
    ty = m.getElementsByTagName('type')[0]
    print('电影类型：',ty.childNodes[0].data)
    year = m.getElementsByTagName('year')
    if len(year) != 0:
        print('拍摄时间：',year[0].childNodes[0].data)
    print()