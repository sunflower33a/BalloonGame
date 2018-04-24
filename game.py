"""
Game Engine (?) Gambit and pygame
"""

import gambit   # Game Theory Library
import itertools  # Combination Library
from functools import reduce
from operator import mul as multiple, add
import numpy
# from numpy import random
from random import choice
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

#   ATTEMPT TO OVERRIDE CLASS METHOD STRATEGY SO THAT THE LABEL IS TUPLE AND NOT STRING
# class Strategy(gambit.Strategy):
#     def __init__(self):




def main():
    # Three level with 3 types of strategies: Uniform distribution, Left focus, and uniform
    print("BLOTTO GAME")
    p = [Player() for i in range(2)]
    p[0].name = raw_input("What is your name? ")
    p[1].name = "Uniform"
    p[0].ball = choice([6, 9, 12, 15, 18])
    p[1].ball = p[0].ball
    k = 3
    p[0].set_strategy(k)
    p[1].set_strategy(k)
    # for pl in p:
    #     print pl.ball
    #print p[0], p[1]
    # print p[0].sLen
    #print p[0].get_strategy()


    print "----------GAMEBIT-------------"
    # for i in range(0,p[1].get_sLen()):
    #     print p[1].get_strategy()[i]
    # Gambit & Strategic game
    g = gambit.Game.new_table([p[0].get_sLen(), p[1].get_sLen()])
    g.title = "Balloon Game"

    # Assign player's pure strategies to gambit.strategies
    strategies = [[] for i in range(2)]

    for i, pl in zip(range(2), p):
        g.players[i].label = pl.name
        plan_len = pl.sLen
        for sIndex, strategy in zip(range(0, plan_len), pl.get_strategy()):
            strategies[i].append(strategy)
            g.players[i].strategies[sIndex].label = "%s" %(strategy)

    sub = [0 for i in range(k)]
    a = 0
    b = 0
    result = False

    print p[0].sLen,  "Ways to distribute", p[0].ball,"balls over", k,"fields: "
    for i in g.players[1].strategies:
        print i.label

    # Calculate Payoff from the strategy
    s1_len = p[0].sLen
    s2_len = p[1].sLen
    pay = numpy.empty((s1_len,s2_len), dtype=gambit.Rational)
    # pay2 = numpy.empty((s2_len,s1_len), dtype=gambit.Rational)
    # print("s1_len:  %d, s2_len: %d" %(s1_len, s2_len))
    # print("len(strategies): %d, %d" %(len(strategies[0]), len(strategies[1])))
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
            summ = reduce(add, sub)
            if (summ > 0) or ((summ == 0) and (p[0].ball<p[1].ball)):
                result = True
            elif (summ < 0) or ((summ == 0) and (p[0].ball<p[1].ball)):
                result = False
            else:
                result = Deuce

            pay[a][b] = result
            b += 1

        a += 1
        b = 0

    # create the symmetrical payoff bimatrix
    g = gambit.Game.from_arrays(pay, numpy.transpose(pay))

    # MIXED STRATEGY
    mixed = g.mixed_strategy_profile()

    # Mixed strategy of naive focal point strategy is a
    # pure strategy of strategy (n/k, n/k, n/k) --> the last strategy's prob = 1.0
    for s in g.players[1].strategies:
        mixed.__setitem__(s, 0)
    # last strategy
    mixed.__setitem__(g.players[1].strategies[s2_len-1], 1)
    g.players[1].label = "Uniform"
    print "Mixed strategies of player", g.players[1].label, ":", mixed[g.players[1]]
    print "Uniform chooses:", play(mixed[g.players[1]], p[1].get_strategy())

# --------------------------------------------------------------------------
    # LEFT FOCUS STRATEGY
    p[1].name = "Left"
    g.players[1].label = "Left"

    # Mixed strategy of Left focused strategy is a
    # probability distribution over the first few pure strategy list (0, a, b)
    # The greater the b, the more likely the strategy is to played
    checksum = 0
    right_focus = 0
    for s, i in zip(g.players[1].strategies, range(s2_len)):
        if p[1].get_strategy()[i][0] != 0:
            mixed.__setitem__(s, 0)
        else:
            right_focus += 1
    unit = right_focus * (right_focus + 1) / 2.0
    unit = 1 / unit
    i=0
    print unit
    print right_focus
    while True:
        if right_focus==0:
            break
        mixed.__setitem__(g.players[1].strategies[i], right_focus*unit)
        checksum += right_focus*unit
        right_focus -= 1
        i += 1

    print "Mixed strategies of player", g.players[1].label,":", mixed[g.players[1]]
    print range(s2_len)
    print "Check sum: ", checksum
    print(p[1].get_strategy())
    right_choice = int(numpy.random.choice(s2_len, 1, mixed[g.players[1]]))
    print "Right chooses:", play(mixed[g.players[1]], p[1].get_strategy())


# ---------------------------------------------------------------------------------------
    # RANDOMIZE STRATEGY --> SMART
    p[1].name = "Ran"
    g.players[1].label = "Ran"
    # Mixed strategy of Smart strategy is randomize all pure strategy
    mixed = g.mixed_strategy_profile()
    print "Mixed strategies of player", g.players[1].label,":", mixed[g.players[1]]
    print "Check sum: ", checksum
    print g.players[1].label, "chooses:", play(mixed[g.players[1]], p[1].get_strategy())
    # NASH EQUILIBRIA
    solver = gambit.nash.lcp_solve(g)
    print("Solved the game")
    print solver


# Randomly choose strategy based on probability,
# return the chosen strategy
def play(prob, strategy):
    from numpy import cumsum
    from numpy.random import rand
    cs = cumsum(prob)  # An array of the weights, cumulatively summed.
    choice = sum(cs < rand())
    return strategy[choice]


main()