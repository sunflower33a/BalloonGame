"""
Game Engine (?) Gambit and PyGame
"""

import gambit   # Game Theory Library
import itertools, math  # Combination Library
from functools import reduce
from operator import mul as multiple, pos
import numpy

class Strategy:
    """Strategy Class"""

    def __init__(self):
        # self.n = n
        # self.k = k
        # # self.len = self.plan_count(n, k)
        pass

    def nCr(self, n, r):
        r = min(n, n - r)
        a = reduce(multiple, xrange(n, n - r, -1), 1)
        b = reduce(multiple, xrange(1, r + 1), 1)
        return a // b

    def plan_count(self, n, k):
        n = n+k-1
        r = k-1
        return self.nCr(n, r)

    # Returns a list of strategies
    def plan_enumeration(self, n, k):
        """
                Strategy Enumeration
                :param: n, k
                :return: iterable object of all the strategies
                         which are k tuples of n distribution
                """

        # return c = n-length tuples in range [0, n+k-1]
        for c in itertools.combinations(range(n + k - 1), k-1):
            z = zip((-1,) + c, c + (n + k - 1,))
            d = [b - a - 1 for a, b in z]
            yield d

class Test:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "<Test a:%s b:%s>" % (self.a, self.b)

    def __str__(self):
        return "From str method of Test: a is %s, b is %s" % (self.a, self.b)


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
        self.sLen = Strategy()

    def set_strategy(self, k):
        """
        :param k: number of battlefields
        :return:  atrribute strategy is set & strategy len is updated
        """
        self.strategy = self.strategy.plan_enumeration(self.ball, k)
        self.sLen = self.sLen.plan_count(self.ball, k)

    def get_strategy(self):
        return self.strategy

    def get_sLen(self):
        return self.sLen

# # K is the number of battlefield
# class BallGame(gambit):
#     pass
#
#     def __init__(self, player1, player2):
#         self.players = [player1, player2]
#         #self.


player = [Player() for i in range(2)]
player[0].name = "Anna"
player[1].name = "Thanh"
k = 3
player[0].ball = 10
player[1].ball = 7
player[0].set_strategy(k)
player[1].set_strategy(k)

#print player[0].get_sLen()
#player.get_strategy

# for s in player[0].get_strategy():
#      print s

print "----------GAMEBIT-------------"
# for i in range(0,player[1].get_sLen()):
#     print player[1].get_strategy()[i]
# Gambit & Strategic game
g = gambit.Game.new_table([player[0].get_sLen(), player[1].get_sLen()])
g.title = "Balloon Game"
for i, p in zip(range(2), player):
    g.players[i].label = p.name
    plan_len = p.get_sLen()
    print p.name
    for sIndex, strategy in zip(range(0, plan_len), p.get_strategy()):
        g.players[i].strategies[sIndex].label = "%s" %(strategy)

s1_len = player[0].get_sLen()
s2_len = player[1].get_sLen()
pay1 = numpy.empty((s1_len,s2_len), dtype=gambit.Rational)
pay2 = numpy.empty((s2_len,s1_len), dtype=gambit.Rational)
sub = [3]
a = 0
b = 0
result = False

# No Strategy????????????????
for s1 in player[0].get_strategy():
    print s1
    for p2 in player[1].get_strategy():
        for i in range(k):
            if s1 > s2: sub[i]=1
            elif s1 < s2: sub[i]=-1
            else: sub[i]=0
        if reduce(pos, sub) > 0:
                result = True
        else: result = False
        pay1[a][b] = result
        pay2[b][a] = not result
        b+=1
    a+=1




# for p in g.players:
#     print p.label
#     for s in p.strategies:
#         print s.label