import sys
A = [
    [1,-1,-1],
    [-1,2,3],
    [1,1,4]
]

E = [
    [1,0,0],
    [0,1,0],
    [0,0,1]
]

print("原矩阵： %s" % A)
for h,i in enumerate(A):
    ts = 0
    for v in i:
        ts += v
    if ts == 0 or len(A) != len(A[h]):
        print("matrix is can't to inverse")
        sys.exit()

for i,v in enumerate(A):
    if i == 1:
        c1 = A[1][0]
        for d1 in range(len(v)):
            A[i][d1] += (A[0][d1] * c1 * -1)
            E[i][d1] += (E[0][d1] * c1 * -1)
    if i == 2:
        c2 = A[2][0]
        for d2 in range(len(v)):
            A[i][d2] += (A[0][d2] * c2 * -1)
            E[i][d2] += (E[0][d2] * c2 * -1)

for i2,v2 in enumerate(A):
    if i2 == 0 :
        c3 = A[i2][1]
        for d3 in range(len(v2)):
            A[i2][d3] += (A[1][d3] * c3 * -1)
            E[i2][d3] += (E[1][d3] * c3 * -1)
    if i2 == 2:
        c4 = A[i2][1]
        for d4 in range(len(v2)):
            A[i2][d4] += (A[1][d4] * c4 * -1)
            E[i2][d4] += (E[1][d4] * c4 * -1)

for i3,v3 in enumerate(A):
    if i3 == 0:
        c5 = A[i3][2]
        for d5 in range(len(v3)):
            A[i3][d5] += (A[2][d5] * c5 * -1)
            E[i3][d5] += (E[2][d5] * c5 * -1)
    if i3 == 1:
        c6 = A[i3][2]
        for d6 in range(len(v3)):
            A[i3][d6] += (A[2][d6] * c6 * -1)
            E[i3][d6] += (E[2][d6] * c6 * -1)
print("增值矩阵：%s" %A)
print("A的逆矩阵：%s"%E)
