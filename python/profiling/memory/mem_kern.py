import random
import time


@profile
def create_random_list(size):
    created_list = []
    for _ in range(size):
        created_list.append(random.random())
    return created_list


if __name__ == '__main__':

    num_lists_1 = 100
    num_lists_2 = 100
    num_delete = 50

    min_size = 10
    max_size = 10000

    # 1. Create lists
    sizes = [random.randint(min_size, max_size) for _ in range(num_lists_1)]
    master_list = []

    for i, size in enumerate(sizes):
        new_list = create_random_list(size)
        master_list.append(new_list)
        print(f'Created new list ({i+1}/{len(sizes)}) of size {size}')

    time.sleep(0.1)

    # 2. Delete lists
    del_list_ids = random.choices(range(num_lists_1), k=num_delete)

    for i in sorted(del_list_ids, reverse=True):
        del master_list[i]

    time.sleep(0.1)

    # 3. Create lists (round 2)
    sizes = [random.randint(min_size, max_size) for _ in range(num_lists_2)]

    for i, size in enumerate(sizes):
        new_list = create_random_list(size)
        master_list.append(new_list)
        print(f'Created new list ({i+1}/{len(sizes)}) of size {size}')

    time.sleep(0.1)

