import numpy as np

t = np.array([7, 5])
p = 3
n = 4*(p - 1)
m = np.zeros((n, n))
b = np.zeros(n)
q = np.array([22, 15, 15])


for x in range (0, p-1):
    m[4*x + 1, 4*x] = 1
    m[4*x + 2, 4*x] = 1
    m[4*x + 2, 4*x + 1] = t[x]
    m[4*x + 2, 4*x + 2] = t[x]**2
    m[4*x + 2, 4*x + 3] = t[x]**3
    m[4*x + 3, 4*x + 1] = 1
    m[4*x + 3, 4*x + 2] = 2*t[x]
    m[4*x + 3, 4*x + 3] = 3*t[x]**2
    b[4*x + 1] = q[x]
    b[4*x + 2] = q[x+1]

for x in range (0, p-2):
    m[4*x + 3, 4*x + 5] = -1
    m[4*x + 4, 4*x + 2] = 2
    m[4*x + 4, 4*x + 3] = 6*t[x]
    m[4*x + 4, 4*x + 6] = -2

m[0, 1] = 1


print(m)
print(b)

x = np.linalg.solve(m, b)
print(x)