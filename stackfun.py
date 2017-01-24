#!/usr/bin/env python
import re,sys


def Operation(exp, arithmetic='polan',convert=False):
    stack = []
    for chk in exp:
        if chk is '(':
            stack.append(chk)
        elif chk is ')':
            stack.pop()
    if len(stack) != 0 and stack[-1] is '(':
        print('you expression is lost the ")" please check.')
        sys.exit()
    elif len(stack) != 0 and stack[-1] is ')':
        print('you expression is lost the "(" please check.')
        sys.exit()

    def Qpoland(exp):
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
        return ret
#
    def Npoland(exp,flag=0):
        rule = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 1, ')': -1}
        ret = []
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
        return ret

    if arithmetic is 'polan':
        arithmetic = Qpoland
    else:
        arithmetic = Npoland
        flag = True

    if convert and arithmetic is 'polan':
        return ''.join(Qpoland(exp)[::-1])
    elif convert is 'npolan' or convert:
        return ''.join(Npoland(exp))
    else:
        for i in arithmetic(exp):
            if i.isdigit():
                stack.append(int(i))
            else:
                if i is '+' and flag:
                    stack.append(stack.pop(-2) + stack.pop(-1))
                elif i is '-' and flag:
                    stack.append(stack.pop(-2) - stack.pop(-1))
                elif i is '*' and flag:
                    stack.append(stack.pop(-2) * stack.pop(-1))
                elif i is '/' and flag:
                    stack.append(stack.pop(-2) / stack.pop(-1))
                elif i is '+':
                    stack.append(stack.pop() + stack.pop())
                elif i is '-':
                    stack.append(stack.pop() - stack.pop())
                elif i is '*':
                    stack.append(stack.pop() * stack.pop())
                elif i is '/':
                    stack.append(stack.pop() / stack.pop())
        return int(stack.pop())


if __name__ == '__main__':
    exp = input('please input you expression: ')
    option = input('you wan to operation it or convert it ? please input poland(p),Npoland(n),default is operaion. you choose: ')
    if option.upper() == 'N':
        print(Operation(exp,convert=True))
    elif option.upper() == 'P':
        print(Operation(exp,arithmetic='polan',convert=True))
    else:
        print(Operation(exp))
