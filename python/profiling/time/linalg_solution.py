import numpy as np
from scipy import linalg
from itertools import product


def create_arrays(dim1, dim2):
    arr = np.arange(dim1 * dim2)
    arr = np.random.random(size=dim1*dim2)
    return arr.reshape(dim1, dim2), arr.reshape(dim2, dim1)


def make_sparse(arr, perc_to_keep=0.05):
    num_elements_to_keep = int(arr.size * perc_to_keep)
    indices_to_drop = np.random.permutation(arr.size)[num_elements_to_keep:]
    row_inds, col_inds = np.unravel_index(indices_to_drop, arr.shape) 
    arr[row_inds, col_inds] = 0
    return arr


def linalg_ops(arr):
    exp = linalg.expm(arr)
    invexp = linalg.inv(exp)
    pexp = linalg.pinv(invexp)
    return pexp
    

def exp_product(arr1, arr2):
    prod = arr1 @ arr2
    return linalg_ops(prod)


def compute_stats(arr):
    stats = {'max': arr.max(),
             'min': arr.min(),
             'mean': arr.mean(),
             'std': arr.std(),
             'det': linalg.det(arr),
             'norm': linalg.norm(arr)}
    return stats


if __name__ == '__main__':

    dims1 = [1, 10, 100, 1000]
    dims2 = [5, 50, 500]

    for dim1, dim2 in product(dims1, dims2):
        A, B = create_arrays(dim1, dim2)
                 
        A = make_sparse(A)
        B = make_sparse(B)

        C = exp_product(A, B)

        stats = compute_stats(C)

        print(f'--- STATS FOR {dim1=}, {dim2=} ---')

        for name, value in stats.items():
            print(f'  {name}: {value:.2f}')

