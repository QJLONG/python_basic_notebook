# -*- coding: utf-8 -*- 
# @Time : 2022/4/10 8:36 
# @Author : hummer 
# @File : test_0410.py


import re
content = "Hello 1234567 word_This is a Regex Demo"
result = re.match('^He.*?(\d+).*?',content)
print(result.group(0))
print(result.group(1))