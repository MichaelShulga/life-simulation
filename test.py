import numpy as np

MATRIX = [
    [1, 2, 4],
    [12, 432, 54],
    [324, 54, 4]
]

a = np.matrix(MATRIX)
index = [0, 0]
print(a)

num_neighbor = 1

left = max(0, index[0] - num_neighbor)
right = max(0, index[0] + num_neighbor + 1)

bottom = max(0, index[1] - num_neighbor)
top = max(0, index[1] + num_neighbor + 1)

sample = a[left:right, bottom:top]

print(sample)
print(sample.sum())

for i in MATRIX:
    for j in i:
        print(j)
