"""
Game Engine (?) Gambit and PyGame
"""

import gambit   # Game Theory Library
import itertools  # Combination Library
from functools import reduce
from operator import mul as multiple, add
import numpy
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

# # K is the number of battlefield
# class BallGame(gambit):
#     pass
#
#     def __init__(self, player1, player2):
#         self.players = [player1, player2]
#         #self.


p = [Player() for i in range(2)]
p[0].name = "Anna"
p[1].name = "Thanh"
k = 4
p[0].ball = 6
p[1].ball = 6
p[0].set_strategy(k)
p[1].set_strategy(k)
# for pl in p:
#     print pl.ball
#print p[0], p[1]
print p[0].sLen
#print p[0].get_strategy()



print "----------GAMEBIT-------------"
# for i in range(0,p[1].get_sLen()):
#     print p[1].get_strategy()[i]
# Gambit & Strategic game
g = gambit.Game.new_table([p[0].get_sLen(), p[1].get_sLen()])
g.title = "Balloon Game"

strategies = [[] for i in range(2)]

for i, pl in zip(range(2), p):
    g.players[i].label = pl.name
    plan_len = pl.sLen
    print pl.name
    for sIndex, strategy in zip(range(0, plan_len), pl.get_strategy()):
        strategies[i].append(strategy)
        g.players[i].strategies[sIndex].label = "%s" %(strategy)

sub = [0 for i in range(k)]
a = 0
b = 0
result = False

# No Strategy????????????????
s1_len = p[0].sLen
s2_len = p[1].sLen
pay1 = numpy.empty((s1_len,s2_len), dtype=gambit.Rational)
pay2 = numpy.empty((s2_len,s1_len), dtype=gambit.Rational)
print("s1_len:  %d, s2_len: %d" %(s1_len, s2_len))
print("len(strategies): %d, %d" %(len(strategies[0]), len(strategies[1])))
for s1 in strategies[0]:
    for s2 in strategies[1]:
        # print("Strategies P1: %s, P2: %s." %(s1,s2))
        for i in range(k):
            # print s1[i], s2[i]
            if s1[i] > s2[i]:
                sub[i] = 1
            elif s1[i] < s2[i]:
                sub[i] = -1
            else:
                sub[i] = 0
        sum = reduce(add, sub)
        if (sum > 0) or ((sum == 0) and (p[0].ball<p[1].ball)):
            result = True
        elif (sum < 0) or ((sum == 0) and (p[0].ball<p[1].ball)):
            result = False
        else:
            result = Deuce

        pay1[a][b] = result
        b += 1

    a += 1
    b = 0

print pay1

g = gambit.Game.from_arrays(pay1, numpy.transpose(pay1))
mixed = g.mixed_strategy_profile()
# for p in mixed:
#     print p
#
# print mixed[g.players[0]]

# ----------Nash Equilibrium--------------
# solver = gambit.nash.


# for p in g.players:
#     print p.label
#     for s in p.strategies:
#         print s.label

# GITHUB VERSION:
# """
# Game Engine (?) Gambit and PyGame
# """
#
# import gambit  # Game Theory Library
# import itertools  # Combination Library
# from functools import reduce
# from operator import mul as multiple, add
# import numpy
#
# True = -1
# False = 1
# Deuce = 0
#
#
# class Strategy:
#     """Strategy Class"""
#
#     def __init__(self):
#         pass
#
#     def nCr(self, n, r):
#         r = min(n, n - r)
#         a = reduce(multiple, xrange(n, n - r, -1), 1)
#         b = reduce(multiple, xrange(1, r + 1), 1)
#         return a // b
#
#     def plan_count(self, n, k):
#         """
#         :param n:
#         :param k:
#         :return:    only for all possible ways of distribute N objects into K spots
#         """
#         n = n + k - 1
#         r = k - 1
#         return self.nCr(n, r)
#
#     def partitions(self, n, k):
#         """
#             Strategy Enumeration
#             :param: n, k
#             :return: GENERATOR object of all the strategies
#             which are k tuples of n distribution
#         """
#
#         # return c = n-length tuples in range [0, n+k-1]
#         for c in itertools.combinations(range(n + k - 1), k - 1):
#             z = zip((-1,) + c, c + (n + k - 1,))
#             d = [b - a - 1 for a, b in z]
#             yield d
#
#     def plan_enumerations(self, n, k):
#         """
#
#         :param n,k
#         :return: A list of strategies such that the distribution is non-negative
#                  and each prev. distribution is no greater than the later
#                  k = 3, n = sum(a-c) --> (a,b,c) such that a<=b<=c and a,b,c >=0
#         """
#         plan = list(self.partitions(n, k))
#         copy = list()
#         for p in plan:
#             boo = 1
#             for i in range(k - 1):
#                 if p[i] > p[i + 1]:
#                     boo = 0
#                     break
#             if boo == 1:
#                 copy.append(p)
#         return copy
#
#
# class Test:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#     def __repr__(self):
#         return "<Test a:%s b:%s>" % (self.a, self.b)
#
#     def __str__(self):
#         return "From str method of Test: a is %s, b is %s" % (self.a, self.b)
#
#
# class Player:
#     """Player class"""
#
#     def __init__(self, name=""):
#         """
#                 Construct a Student object. Simply sets the values of the attributes.
#
#                 :param name: the name of the player
#         """
#         self.name = name
#         self.ball = 0  # numbers of balloons player has
#         self.score = 0
#         self.strategy = Strategy()  # Strategy Object
#         self.sLen = 0
#
#     def __repr__(self):
#         return [a for a in self.strategy]
#
#     def __str__(self):
#         return "<Player, Name: %s, Balloons: %d, Score %d, # of Strategies: %d.>" \
#                % (self.name, self.ball, self.score, self.sLen)
#
#     def set_strategy(self, k):
#         """
#         :param k: number of battlefields
#         :return:  atrribute strategy is set & strategy len is updated
#         """
#         self.strategy = self.strategy.plan_enumerations(self.ball, k)
#         self.sLen = len(self.strategy)
#
#     def get_strategy(self):
#         return self.strategy
#
#     def get_sLen(self):
#         return self.sLen
#
#
# # # K is the number of battlefield
# # class BallGame(gambit):
# #     pass
# #
# #     def __init__(self, player1, player2):
# #         self.players = [player1, player2]
# #         #self.
#
#
# p = [Player() for i in range(2)]
# p[0].name = "Anna"
# p[1].name = "Thanh"
# k = 4
# p[0].ball = 6
# p[1].ball = 6
# p[0].set_strategy(k)
# p[1].set_strategy(k)
# # for pl in p:
# #     print pl.ball
# # print p[0], p[1]
# print p[0].sLen
# # print p[0].get_strategy()
#
#
# print "----------GAMEBIT-------------"
# # for i in range(0,p[1].get_sLen()):
# #     print p[1].get_strategy()[i]
# # Gambit & Strategic game
# g = gambit.Game.new_table([p[0].get_sLen(), p[1].get_sLen()])
# g.title = "Balloon Game"
#
# strategies = [[] for i in range(2)]
#
# for i, pl in zip(range(2), p):
#     g.players[i].label = pl.name
#     plan_len = pl.sLen
#     print pl.name
#     for sIndex, strategy in zip(range(0, plan_len), pl.get_strategy()):
#         strategies[i].append(strategy)
#         g.players[i].strategies[sIndex].label = "%s" % (strategy)
#
# sub = [0 for i in range(k)]
# a = 0
# b = 0
# result = False
#
# # No Strategy????????????????
# s1_len = p[0].sLen
# s2_len = p[1].sLen
# pay1 = numpy.empty((s1_len, s2_len), dtype=gambit.Rational)
# pay2 = numpy.empty((s2_len, s1_len), dtype=gambit.Rational)
# print("s1_len:  %d, s2_len: %d" % (s1_len, s2_len))
# print("len(strategies): %d, %d" % (len(strategies[0]), len(strategies[1])))
# for s1 in strategies[0]:
#     for s2 in strategies[1]:
#         # print("Strategies P1: %s, P2: %s." %(s1,s2))
#         for i in range(k):
#             # print s1[i], s2[i]
#             if s1[i] > s2[i]:
#                 sub[i] = 1
#             elif s1[i] < s2[i]:
#                 sub[i] = -1
#             else:
#                 sub[i] = 0
#         sum = reduce(add, sub)
#         if (sum > 0) or ((sum == 0) and (p[0].ball < p[1].ball)):
#             result = True
#         elif (sum < 0) or ((sum == 0) and (p[0].ball < p[1].ball)):
#             result = False
#         else:
#             result = Deuce
#
#         pay1[a][b] = result
#         b += 1
#
#     a += 1
#     b = 0
#
# print pay1
#
# g = gambit.Game.from_arrays(pay1, numpy.transpose(pay1))
# mixed = g.mixed_strategy_profile()
# # for p in mixed:
# #     print p
# #
# # print mixed[g.players[0]]
#
# # ----------Nash Equilibrium--------------
# # solver = gambit.nash.
#
#
# # for p in g.players:
# #     print p.label
# #     for s in p.strategies:
# #         print s.label