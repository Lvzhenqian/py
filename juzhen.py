A = [
    [1, 2,1],
    [0, 1, 4],
    [1, 9, 1]
]


def determinant(deter: list) -> int:
    for num, value in enumerate(A[len(deter) - 1]):
        A[len(deter) - 2][num] += (A[len(deter) - 2][-1] * -1 / A[len(deter) - 1][-1]) * value
        A[0][num] += (A[0][-1] * -1 / A[len(deter) - 1][-1]) * value
    A[0][1] += (A[0][1] * -1 / A[len(deter) - 1][1]) * value
    print(A)
    return A[0][0] * A[1][1] * A[2][2]


print(determinant(A))
