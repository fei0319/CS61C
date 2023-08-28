from numpy import array as matrix
from random import randint
import os


def randmat(n, m):
    return matrix([randint(0, 10) for _ in range(n * m)]).reshape(n, m)


def relu(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] < 0:
                mat[i][j] = 0


def read_int(content):
    return int.from_bytes(content, byteorder="little")


def read_matrix(file_name):
    with open(file_name, mode='rb') as f:
        content = f.read()
        row = read_int(content[0:4])
        col = read_int(content[4:8])
        content = content[8:]
        mat = []
        for i in range(row * col):
            mat.append(read_int(content[i * 4:(i+1) * 4]))
        mat = matrix(mat).reshape(row, col)
    return mat


def write_matrix(file_name, mat):
    file_name = os.path.join("..", file_name)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, mode='wb') as f:
        row, col = mat.shape
        f.write(row.to_bytes(4, 'little'))
        f.write(col.to_bytes(4, 'little'))
        for i in mat:
            for j in i:
                f.write(int(j).to_bytes(4, 'little'))
