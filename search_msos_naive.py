"""
A MSOS is a perfect 3x3 square, where
 - each fields value is unique within the square and
 - each field holds a square number

It is uniquely determined by the upper left 2x2 contained square
and the value on the top right,
which are each also uniquely determined by their square root.
This restricts the search space for finding a parker square
to the combinations of 5 unique numbers.


a² | b² | c²
------------
d² | e² | f²
------------
g² | h² | k²

"""
from functools import lru_cache
import concurrent.futures

N = 1000000

# finds the integer square root of i
@lru_cache(maxsize=N)
def int_sqrt_binsearch(i):
    l, h = 0, i/2
    while l < h:
        m = (l+h)//2
        if m**2 < i:
            l = m+1
        else:
            h = m
    return l if l**2 == i else None


INT_SQRT_DICT = {}
for i in range(N):
    INT_SQRT_DICT[i**2] = i

# faster (?) lookup version
def int_sqrt_lookup(i):
    return INT_SQRT_DICT.get(i, None)

def int_sqrt(i):
    return int_sqrt_lookup(i)
    #if i < N:
    #    return int_sqrt_lookup(i)
    #else:
    #    return int_sqrt_binsearch(i)

# checks whether the five given numbers define a MSOS
# and in that case returns the square
def is_square(a, b, c, d, e):
    used_nums = {a,b,c,d,e}
    if len(used_nums) != 5:
        return None
    a_sq, b_sq, c_sq, d_sq, e_sq = a**2, b**2, c**2, d**2, e**2
    row_sum = a_sq + b_sq + c_sq
    f_sq = row_sum - e_sq - d_sq
    f = int_sqrt(f_sq)
    if f is None or f**2 != f_sq:
        return None
    g_sq = row_sum - d_sq - a_sq
    g = int_sqrt(g_sq)
    if g is None or g**2 != g_sq:
        return None
    h_sq = row_sum - e_sq - b_sq
    h = int_sqrt(h_sq)
    if h is None or h**2 != h_sq:
        return None
    k_sq = row_sum - f_sq - c_sq
    k = int_sqrt(k_sq)
    if k is None or k**2 != k_sq:
        return None

    used_nums.update([f,g,h,k])
    if len(used_nums) == 9 and a_sq + e_sq + k_sq == row_sum and g_sq + e_sq + c_sq == row_sum:
        return [[a_sq, b_sq, c_sq],[d_sq, e_sq, f_sq], [g_sq, h_sq, k_sq]]
    else:
        return None


def try_rem(a, n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                for e in range(n):
                    res = is_square(a, b, c, d, e)
                    if res is not None:
                        return res
            print(f"{a}, {b}, {c}", end="\r")
    return None

def main(n):

    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        for res in executor.map(try_rem, range(n), (n for _ in range(n))):
            if res is not None:
                print(res)

if __name__ == '__main__':
    main(100)