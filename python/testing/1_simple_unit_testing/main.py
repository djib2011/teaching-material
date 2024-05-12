def add(*nums):
    s = 0 
    for num in nums:
        s += num
    return s


def multiply(*nums):
    p = 1
    for num in nums:
        p *= num
    return p

