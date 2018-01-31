from functools import singledispatch

class Test(object):
    """docstring for test"""
    def __init__(self):
        self.a = 1
        self.b = 'a'
        self.c = []
        print(id(self.a))
        print(id(self.b))
        print(id(self.c))

    def ttt(self):
        print("a: ", self.a)
        print("b: ", self.b)
        print("c: ", self.c)
        print("new a : ", id(self.a))
        print("new a : ", id(self.b))
        print("new a : ", id(self.c))
        
if __name__ == '__main__':
    test = Test()
    test.a = 3
    test.b = "new"
    test.c = [3,4,5]
    print(vars(test))
    test.ttt()

# @singledispatch
# def fun(x):
#     print("test : ", x)

# @fun.register(int)
# def _(x):
#     print("test int : ", x)

# @fun.register(str)
# def _(x):
#     print(x)


# if __name__ == '__main__':
#     fun({3})