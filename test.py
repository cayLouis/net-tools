
def tip(fun):
    print("mkmk")
    def wrapper(*lis, **dict):
        print("start")
        fun(*lis, **dict)
        print("end")
    return wrapper

@tip
def test(*a, **b):
    print(len(a))

a = tip(test)
a(123)
