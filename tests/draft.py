def f():
    return None, None


print(f())
if f():
    print('aaa')
else:
    print('bbb')
a = f()
print(*a)
