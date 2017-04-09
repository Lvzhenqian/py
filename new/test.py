str1 = 'abcdefghijklmnop'
str2 = 'abcsafjklmnopqrstuvw'


def substring(x, y):
    lst = []
    st = ''
    for s in x:
        if s in y:
            for s2 in y:
                if s == s2:
                    st += s
                    break
        else:
            if st:
                lst.append(st)
            st = ''
    else:
        lst.append(st)
    return max(lst)

print('str  = ',str1)
print('str2 = ',str2)
print('sub  = ',substring(str1, str2))