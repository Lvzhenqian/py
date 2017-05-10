# coding:utf-8
import csv
from collections import namedtuple


def ReadCsv(file):
    with open(file) as f:
        f_csv = csv.reader(f)
        _ = next(f_csv)
        data = namedtuple('data', ['name', 'more', 'master'])
        while True:
            try:
                i = next(f_csv)
                yield data(i[11], i[14], i[15])
            except StopIteration:
                break



def getsite(path):
    rule = {
        "百度": 'baidu_{:0>4}_cgdb'.format,
        "7road官网": '7road_{:0>4}_cgdb'.format,
        "多玩": 'duowan_{:0>4}_cgdb'.format,
        "7k7k": '7k7k_{:0>4}_cgdb'.format,
        "开心网": 'kxwang_{:0>4}_cgdb'.format,
        "奇虎": 'qihu360_{:0>4}_cgdb'.format,
        "淘米": 'taomi_{:0>4}_cgdb'.format,
        "4399": '4399_{:0>4}_cgdb'.format
    }
    site = []
    fill = lambda st:''.join([x for x in st if x in '0123456789'])
    excel = ReadCsv(path)
    fix = [0]
    for lines in excel:
        for ne in lines.more.split('、'):
            n = fill(ne)
            if lines.name:
                fix[0]=lines.name
            if '7road' in fix[0] or '官网' in fix[0]:
                site.append(rule["7road官网"](n))
            if '360' in fix[0] or '奇虎' in fix[0]:
                site.append(rule["奇虎"](n))
            if 'kx' in fix[0] or '开心' in fix[0]:
                site.append(rule["开心网"](n))
            site.append(rule[fix[0]](n))
    return site


s = getsite(r'D:\py\test.csv')
print(s)
