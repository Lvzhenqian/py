import re
def Qpoland(exp):
    stack = []
    rule = {'+': 1, '-': 1, '*': 2, '/': 2, '(': -1, ')': 1}
    ret = []
    for x in re.split(r'(\W+?)', exp)[::-1]:
        if x is '':
            continue
        if x.isdigit():
            ret.append(x)
        else:
            if len(stack) == 0 or rule[x] >= rule[stack[-1]] or x is ')':
                stack.append(x)
            elif x is '(':
                while True:
                    if stack[-1] is ')':
                        stack.pop()
                        break
                    else:
                        ret.append(stack.pop())
            else:
                while len(stack) > 0:
                    ret.append(stack.pop())
                stack.append(x)
    else:
        while len(stack) > 0:
            ret.append(stack.pop())
    return ''.join(ret)
print(Qpoland('1+3-(5/4)-(3+2)')[::-1])

tmp = []
for x in Qpoland('1+3-(5/4)-(3+2)'):
    if x.isdigit():
        tmp.append(int(x))
    else:
        if x is '+':
            tmp.append(tmp.pop() + tmp.pop())
        if x is '-':
            tmp.append(tmp.pop() - tmp.pop())
        if x is '*':
            tmp.append(tmp.pop() * tmp.pop())
        if x is '/':
            tmp.append(tmp.pop() / tmp.pop())
print(tmp)


