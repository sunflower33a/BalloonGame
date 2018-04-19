"""
*   Strategy.PY
"""
class Strategy:
    """Strategy Class"""

    def __init__(self):
        pass

    def nCr(self, n, r):
        r = min(n, n - r)
        a = reduce(multiple, xrange(n, n - r, -1), 1)
        b = reduce(multiple, xrange(1, r + 1), 1)
        return a // b

    def plan_count(self, n, k):
        """
        :param n:
        :param k:
        :return:    only for all possible ways of distribute N objects into K spots (non-negative)
        """
        n = n + k - 1
        r = k - 1
        return self.nCr(n, r)

    def partitions(self, n, k):
        """
            STARS AND BARS ALGORITHM (NOT MINE)
            :param: n, k
            :return: GENERATOR object of all distribution posibility toa
            assign N objects to K holes
        """

        # return c = n-length tuples in range [0, n+k-1]
        for c in itertools.combinations(range(n + k - 1), k - 1):
            z = zip((-1,) + c, c + (n + k - 1,))
            d = [b - a - 1 for a, b in z]
            yield d

    def plan_enumerations(self, n, k):
        """

        :param n,k
        :return: A list of strategies such that the distribution is non-negative
                 and each prev. distribution is no greater than the later
                 k = 3, n = sum(a-c) --> (a,b,c) such that a<=b<=c and a,b,c >=0
        """
        plan = list(self.partitions(n, k))
        copy = list()
        for p in plan:
            boo = 1
            for i in range(k - 1):
                if p[i] > p[i + 1]:
                    boo = 0
                    break
            if boo == 1:
                copy.append(p)
        return copy
