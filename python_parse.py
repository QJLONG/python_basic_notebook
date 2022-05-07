# -*- coding:utf-8 -*-
###
# File: python_parse.py
# Created Date: 2022-05-03
# Author: hummer
# Last Modified: Tuesday May 3rd 2022 8:23:20 pm
###

'''
    简单测试python从命令行中读取参数的方法
    1.sys.argv
    2.getopt模块
    3.
'''

# import sys
# print("参数个数为：%d" % (len(sys.argv)))
# print("参数列表：",sys.argv)

# 参数个数为：3
# 参数列表： ['.\\python_parse.py', 'arg1', 'arg2']

'''
    getopt.getopt 方法用于解析命令行参数列表，语法格式如下：

    getopt.getopt(args, options[, long_options])
    
    args: 要解析的命令行参数列表。

    options : 以字符串的格式定义,options 后的冒号 : 表示如果设置该选项，必须有附加的参数，否则就不附加参数。

    long_options : 以列表的格式定义,long_options 后的等号 = 表示该选项必须有附加的参数，不带等号表示该选项不附加参数。

    该方法返回值由两个元素组成: 第一个是 (option, value) 元组的列表。 第二个是参数列表，包含那些没有 - 或 -- 的参数。
'''

import getopt
import sys

input_file = ''
output_file = ''
try:
    opts,args = getopt.getopt(sys.argv[1:],"hi:o:",["input-file=","output-file="])
except getopt.GetoptError:
    print("test.py -i <inputfile> -o <outputfile")

for opt,arg in opts:
    if opt == "-h":
        print("test.py -i <inputfile> -o <outputfile")
        sys.exit(0)
    elif opt in ["-i","--input-file"]:
        input_file = arg
    elif opt in ["-o","--output-file"]:
        output_file = arg
    
print("input:",input_file)
print("output:",output_file)

