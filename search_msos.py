"""
A MSOS is a perfect 3x3 square, where
 - each fields value is unique within the square and
 - each field holds a square number

This approach is based on the fact that a MSOS
is defined by 3 unique square numbers as pointed out here:
https://www.mathpages.com/home/kmath417/kmath417.htm


a² | b² | c²
------------
d² | e² | f²
------------
g² | h² | k²

"""
import concurrent.futures

# dummy values, overwritten in the main branch
N = 1

SQUARES = [i**2 for i in range(N)]

INT_SQRT_DICT = {}
for i in range(N):
    INT_SQRT_DICT[i**2] = i

# faster (?) lookup version
def int_sqrt(i):
    return INT_SQRT_DICT.get(i, None)

# checks whether the five given numbers define a parker square
# and in that case returns the square
def is_square(E, n, m):
    a_sq, b_sq, c_sq, d_sq, e_sq, f_sq, g_sq, h_sq, k_sq = (
        E+n, E-n-m, E+m, E-n+m, E, E+n-m, E-m, E+n+m, E-n
    )
    row_sum = a_sq + b_sq + c_sq
    if (
            d_sq + e_sq + f_sq != row_sum or
            g_sq + h_sq + k_sq != row_sum or
            a_sq + d_sq + g_sq != row_sum or
            b_sq + e_sq + h_sq != row_sum or
            c_sq + f_sq + k_sq != row_sum or
            a_sq + e_sq + k_sq != row_sum or
            g_sq + e_sq + c_sq != row_sum
    ):
        return None

    used_nums = {
        int_sqrt(a_sq),
        int_sqrt(b_sq),
        int_sqrt(c_sq),
        int_sqrt(d_sq),
        int_sqrt(e_sq),
        int_sqrt(f_sq),
        int_sqrt(g_sq),
        int_sqrt(h_sq),
        int_sqrt(k_sq),
    }
    if len(used_nums) != 9 or None in used_nums:
        return None
    return [[a_sq, b_sq, c_sq],[d_sq, e_sq, f_sq], [g_sq, h_sq, k_sq]]

def try_rem(iE):
    i, E = iE
    print(f"{E}", end="\r")
    for (j, Epn) in enumerate(SQUARES[i+1:], start=i+1):
        # we can discard half of the search space due to symmetry
        for Epm in SQUARES[j+1:]:
            n = Epn - E
            m = Epm - E
            res = is_square(E, n, m)
            if res is not None:
                return res
    return None


def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        for res in executor.map(try_rem, enumerate(SQUARES)):
            if res is not None:
                print(res)
                exit(0)

if __name__ == '__main__':
    # Exponential search for a square
    N = 4000
    while True:
        print(N)
        SQUARES = [i ** 2 for i in range(N)]

        INT_SQRT_DICT = {}
        for i in range(N):
            INT_SQRT_DICT[i ** 2] = i
        main()
        N = N*2
