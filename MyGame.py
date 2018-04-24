"""
Game Engine (?) Gambit and pygame
"""

import gambit  # Game Theory Library
from operator import add
import numpy
from MyPlayer import *
from random import choice
from MyStrategy import *

True = -1
False = 1
Deuce = 0


class Level():
    """
        The Game player has three levels when player play against 3 types of computer
        Object Level contains 2 players between ThePlayer and Computer Player
        Each level has at least 5 rounds, a level ends when either of the player gets 5 points
    """

    def __init__(self, player1, player2, my_parent_game, next_lvl):
        self.player1 = player1
        self.player2 = player2
        self.round = 1
        self.parent = my_parent_game
        self.winner = None
        self.next = next_lvl

    def decide_winner(self):
        won_1 = 0
        won_2 = 0
        for p1, p2 in zip(self.player1.choice, self.player2.choice):
            if p1 > p2:
                won_1 += 1
            elif p2 > p1:
                won_2 += 1
        if won_1 > won_2:
            self.winner(self.player1)
        elif won_2 > won_1:
            self.winner(self.player2)
        else:
            self.winner(None)

    def round_winner(self, player=None):
        player.score += 1
        self.round += 1

    def end_level(self):
        if (self.player1.score==5) or (self.player2.score==5):
            # Switch to the next level
            self.parent.current_level = self.next



class Game():
    """
        input: Player objects 1 and 2
    """

    def __init__(self):
        self.ball = 0
        self.k = 3
        self.strategy = []
        self.sLen = 0
        self.current_level = None

        self.the_player = ThePlayer("", self)

        self.random_player = RandomPlayer(self)
        self.random_level = Level(self.the_player, self.random_player, self, None)
        self.random_player.lvl = self.random_level

        self.right_player = RightPlayer(self)
        self.right_level = Level(self.the_player, self.right_player, self, self.random_level)
        self.right_player.lvl = self.right_level

        self.uniform_player = UniformPlayer(self)
        self.uniform_level = Level(self.the_player, self.uniform_player, self, self.right_level)
        self.uniform_player.lvl = self.uniform_level


        self.current_level = self.uniform_level
        self.title = "Colonel Balloon"

        # GAMBIT =======================================
        self.gambit = gambit.Game.new_table((self.sLen, self.sLen))
        self.gambit.title = "Balloon Game"
        # self.mixed = self.gambit.mixeds_strategy_profile()
        self.mixed = [0 for i in range(self.sLen)]

    def randomize_k(self):
        return choice([9, 12, 15, 18])

    def random_ball(self):
        # After letting the player randomize K, the game's strategy is set
        self.ball = self.randomize_k()
        self.set_strategy()

    def generate_payoff(self):
        sub = [0 for i in range(self.k)]
        a = 0
        b = 0
        # Payoff Matrix
        pay = numpy.empty((self.sLen, self.sLen), dtype=self.gambit.Rational)
        for s1 in self.strategy:
            for s2 in self.strategy:
                for i in range(k):
                    if s1[i] > s2[i]:
                        sub[i] = 1
                    elif s1[i] < s2[i]:
                        sub[i] = -1
                    else:
                        sub[i] = 0
                summ = reduce(add, sub)
                # If wanting to have different ball for two players, let player has attribute ball
                # And use self.current_level.player2.ball
                if summ > 0:
                    result = True
                elif summ < 0:
                    result = False
                else:
                    result = Deuce
                pay[a][b] = result
                b += 1
            a += 1
            b = 0
            self.gambit = gambit.Game.from_arrays(pay, numpy.transpose(pay))
            return pay

    def set_strategy(self):
        """
        :param k: number of battlefields
        :return:  atrribute strategy is set & strategy len is updated
        """
        s_object = Strategy()
        self.strategy = s_object.plan_enumerations(self.ball, self.k)
        self.sLen = len(self.strategy)

#
# def main():
#     # Three level with 3 types of strategies: Uniform distribution, Left focus, and uniform
#     print("BLOTTO GAME")
#     p = [Player() for i in range(2)]
#     p[0].name = raw_input("What is your name? ")
#     p[1].name = "Uniform"
#     p[0].ball = choice([6, 9, 12, 15, 18])
#     p[1].ball = p[0].ball
#     k = 3
#     p[0].set_strategy(k)
#     p[1].set_strategy(k)
#     # for pl in p:
#     #     print pl.ball
#     #print p[0], p[1]
#     # print p[0].sLen
#     #print p[0].get_strategy()
#
#
#     print "----------GAMEBIT-------------"
#     # for i in range(0,p[1].get_sLen()):
#     #     print p[1].get_strategy()[i]
#     # Gambit & Strategic game
#     g = gambit.Game.new_table([p[0].get_sLen(), p[1].get_sLen()])
#     g.title = "Balloon Game"
#
#     # Assign player's pure strategies to gambit.strategies
#     strategies = [[] for i in range(2)]
#
#     for i, pl in zip(range(2), p):
#         g.players[i].label = pl.name
#         plan_len = pl.sLen
#         for sIndex, strategy in zip(range(0, plan_len), pl.get_strategy()):
#             strategies[i].append(strategy)
#             g.players[i].strategies[sIndex].label = "%s" %(strategy)
#
#     result = False
#
#     print p[0].sLen,  "Ways to distribute", p[0].ball,"balls over", k,"fields: "
#     for i in g.players[1].strategies:
#         print i.label
#
#
#     # Calculate Payoff from the strategy
#     s1_len = p[0].sLen
#     s2_len = p[1].sLen
#     pay = numpy.empty((s1_len,s2_len), dtype=gambit.Rational)
#     # pay2 = numpy.empty((s2_len,s1_len), dtype=gambit.Rational)
#     # print("s1_len:  %d, s2_len: %d" %(s1_len, s2_len))
#     # print("len(strategies): %d, %d" %(len(strategies[0]), len(strategies[1])))
#     sub = [0 for i in range(k)]
#     a = 0
#     b = 0
#     # Payoff Matrix
#     for s1 in strategies[0]:
#         for s2 in strategies[1]:
#             # print("Strategies P1: %s, P2: %s." %(s1,s2))
#             for i in range(k):
#                 # print s1[i], s2[i]
#                 if s1[i] > s2[i]:
#                     sub[i] = 1
#                 elif s1[i] < s2[i]:
#                     sub[i] = -1
#                 else:
#                     sub[i] = 0
#             summ = reduce(add, sub)
#             if (summ > 0) or ((summ == 0) and (p[0].ball<p[1].ball)):
#                 result = True
#             elif (summ < 0) or ((summ == 0) and (p[0].ball<p[1].ball)):
#                 result = False
#             else:
#                 result = Deuce
#
#             pay[a][b] = result
#             b += 1
#
#         a += 1
#         b = 0
#
#     # create the symmetrical payoff bimatrix
#     g = gambit.Game.from_arrays(pay, numpy.transpose(pay))
#
#     # MIXED STRATEGY
#     mixed = g.mixed_strategy_profile()
#     # Mixed strategy of naive focal point strategy is a
#     # pure strategy of strategy (n/k, n/k, n/k) --> the last strategy's prob = 1.0
#     for s in g.players[1].strategies:
#         mixed.__setitem__(s, 0)
#     # last strategy
#     mixed.__setitem__(g.players[1].strategies[s2_len-1], 1)
#     g.players[1].label = "Uniform"
#     print "Mixed strategies of player", g.players[1].label, ":", mixed[g.players[1]]
#     print "Uniform chooses:", play(mixed[g.players[1]], p[1].get_strategy())
#
# # --------------------------------------------------------------------------
#     # RIGHT FOCUS STRATEGY
#     p[1].name = "Right"
#     g.players[1].label = "Right"
#
#     # Mixed strategy of Right focused strategy is a
#     # probability distribution over the first few pure strategy list (0, a, b)
#     # The greater the b, the more likely the strategy is to played
#     checksum = 0
#     right_focus = 0
#     for s, i in zip(g.players[1].strategies, range(s2_len)):
#         if p[1].get_strategy()[i][0] != 0:
#             mixed.__setitem__(s, 0)
#         else:
#             right_focus += 1
#     unit = right_focus * (right_focus + 1) / 2.0
#     unit = 1 / unit
#     i=0
#     print unit
#     print right_focus
#     while True:
#         if right_focus==0:
#             break
#         mixed.__setitem__(g.players[1].strategies[i], right_focus*unit)
#         checksum += right_focus*unit
#         right_focus -= 1
#         i += 1
#
#     print "Mixed strategies of player", g.players[1].label,":", mixed[g.players[1]]
#     print range(s2_len)
#     print "Check sum: ", checksum
#     print(p[1].get_strategy())
#     right_choice = int(numpy.random.choice(s2_len, 1, mixed[g.players[1]]))
#     print "Right chooses:", play(mixed[g.players[1]], p[1].get_strategy())
#
#
# # ---------------------------------------------------------------------------------------
#     # RANDOMIZE STRATEGY --> SMART
#     p[1].name = "Ran"
#     g.players[1].label = "Ran"
#     # Mixed strategy of Smart strategy is randomize all pure strategy
#     mixed = g.mixed_strategy_profile()
#     print "Mixed strategies of player", g.players[1].label,":", mixed[g.players[1]]
#     print "Check sum: ", checksum
#     print g.players[1].label, "chooses:", play(mixed[g.players[1]], p[1].get_strategy())
#     # NASH EQUILIBRIA
#     solver = gambit.nash.lcp_solve(g)
#     print("Solved the game")
#     print solver
#
#
# def play(prob, strategy):
#     from numpy import cumsum
#     from numpy.random import rand
#     cs = cumsum(prob)  # An array of the weights, cumulatively summed.
#     choice = sum(cs < rand())
#     return strategy[choice]
#
#
# main()
