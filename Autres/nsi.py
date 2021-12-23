from math import *
def f(x):
    return (100*exp(-0.12*x))
a = 0
b = 5

while(abs(b-a) > 0.01):
    m = (a + b) / 2
    if f(m) > 80:
        a = m
    else:
        b = m

print(a, b)
