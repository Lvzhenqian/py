import re
def Npoland(exp,flag=0):
    rule = {'+': 1, '-': 1, '*': 3, '/': 4, '(': 1, ')': -1}
    ret = []
    stack = []
    for j in re.split(r'(\W+?)', exp):
        if j is '':
            continue
        if j.isdigit():
            ret.append(j)
        else:
            if flag == 1 and j is '-':
                ret.append(j)
                flag = 0
            elif len(stack) == 0 or rule[j] >= rule[stack[-1]]:
                stack.append(j)
            elif j is ')':
                while True:
                    if stack[-1] is '(':
                        stack.pop()
                        flag = 1
                        break
                    else:
                        ret.append(stack.pop())
            else:
                while len(stack) > 0:
                    ret.append(stack.pop())
                stack.append(j)
    else:
        while len(stack) > 0:
            ret.append(stack.pop())
    return ''.join(ret)
print(Npoland('1+3-(5/4)-3+2'))

tmp = []
for x in Npoland('1+3-(5/4)-3+2'):
    if x.isdigit():
        tmp.append(int(x))
    else:
        if x is '+':
            tmp.append(tmp.pop(-2) + tmp.pop())
        if x is '-':
            tmp.append(tmp.pop(-2) - tmp.pop())
        if x is '*':
            tmp.append(tmp.pop(-2) * tmp.pop())
        if x is '/':
            tmp.append(tmp.pop(-2) / tmp.pop())
print(tmp)
