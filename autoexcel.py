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
    for lines in excel:
        for ne in lines.more.split('、'):
            n = fill(ne)
            print(lines.name)
            if not lines.name:
                continue
            if '7road' in lines.name or '官网' in lines.name:
                site.append(rule["7road官网"](n))
            if '360' in lines.name or '奇虎' in lines.name:
                site.append(rule["奇虎"](n))
            if 'kx' in lines.name or '开心' in lines.name:
                site.append(rule["开心网"](n))
            site.append(rule[lines.name](n))
    return site


s = getsite(r'd:\test.csv')
print(s)
