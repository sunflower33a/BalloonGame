import itertools  # Combination Library
from functools import reduce
from operator import mul as multiple

True = -1
False = 1
Deuce = 0


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
        :return:    only for all possible ways of distribute N objects into K spots
        """
        n = n+k-1
        r = k-1
        return self.nCr(n, r)

    def partitions(self, n, k):
        """
            Strategy Enumeration
            :param: n, k
            :return: GENERATOR object of all the strategies
            which are k tuples of n distribution
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


class Player:
    """Player class"""

    def __init__(self, name=""):
        """
                Construct a Student object. Simply sets the values of the attributes.

                :param name: the name of the player
        """
        self.name = name
        self.ball = 0     # numbers of balloons player has
        self.score = 0
        self.strategy = Strategy()     # Strategy Object
        self.sLen = 0

    def __repr__(self):
        return [a for a in self.strategy]

    def  __str__(self):
        return "<Player, Name: %s, Balloons: %d, Score %d, # of Strategies: %d.>" \
                %(self.name, self.ball, self.score, self.sLen)

    def set_strategy(self, k):
        """
        :param k: number of battlefields
        :return:  atrribute strategy is set & strategy len is updated
        """
        self.strategy = self.strategy.plan_enumerations(self.ball, k)
        self.sLen = len(self.strategy)

    def get_strategy(self):
        return self.strategy

    def get_sLen(self):
        return self.sLen