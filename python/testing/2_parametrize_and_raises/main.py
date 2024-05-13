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


def divide(*nums):
    """
    divide(a, b, c, d) == a / b / c / d
    """    

    if len(nums) < 1:
        raise ValueError('Pass at least two values to the function')

    if len(nums) == 1:
        return nums[0]

    nominator = nums[0]
    denominator = multiply(*nums[1:])
    
    print(f'{nominator = }')
    print(f'{denominator = }')

    return nominator / denominator
