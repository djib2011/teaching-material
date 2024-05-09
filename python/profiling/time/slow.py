import time


def func1():
    a = 2
    time.sleep(0.5)
    return a


def func2():
    a = 5 + 2 - 1
    time.sleep(2)


def func3():
    a = 4 * 2
    b = 3 + 1
    time.sleep(5)
    return b / a



if __name__ == '__main__':

    func_execution_order = [func1, func2, func3, func2, func1, func2, func3]
    
    for func in func_execution_order:
        print('Executing:', func.__name__)
        func()

