#!/usr/bin/python
#coding:utf8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
s_type = sys.getfilesystemencoding()
print s_type
print '*' * 50
mytype = '测试一下，中文输出'
print mytype.decode('utf-8').encode(s_type)
print mytype
