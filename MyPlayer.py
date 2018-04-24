class MyPlayer():
    """
        Inheritances of Player class, extended for 3 types of computer players
    """
    def __init__(self, name, parent_game=None):
        # Player.__init__(self, name)
        self.name = name
        self.score = 0
        self.parent = parent_game
        self.ball = self.parent.ball  # numbers of balloons player has
        self.strategy = self.parent.strategy  # the game has the same strategy space
        self.choice = None
        self.mixed = []

    # Randomly choose strategy based on probability,
    # return the chosen strategy
    def play(self, prob):
        from numpy import cumsum
        from numpy.random import rand
        cs = cumsum(prob)  # An array of the weights, cumulatively summed.
        choice_index = sum(cs < rand())
        self.choice = self.strategy[choice_index]

    def print_mixed(self):
        # Update Mixed
        self.mixed = self.parent.mixed
        print "Mixed strategies of player", self.name, ":", self.mixed
        print self.name, "chooses:", self.play(self.mixed)

    def mixed_strategy(self):
        pass


class RandomPlayer(MyPlayer):
    def __init__(self, parent_level):
        MyPlayer.__init__(self, "Random", parent_level)

    def mixed_strategy(self):
        # Mixed strategy of Smart strategy is randomize all pure strategy
        for mixed_index in self.parent.sLen:
            self.parent.mixed[mixed_index] = float(1/sLen)
        self.print_mixed()


class UniformPlayer(MyPlayer):
    def __init__(self, parent_level):
        MyPlayer.__init__(self, "Uniform", parent_level)

    def mixed_strategy(self):
        for i in range(len(self.parent.mixed)):
            self.parent.mixed[i] = 0
        # last strategy = 1
        self.parent.mixed[self.parent.sLen-1] = 1
        self.print_mixed()


class RightPlayer(MyPlayer):
    def __init__(self, parent_level):
        MyPlayer.__init__(self, "Right", parent_level)

    def mixed_strategy(self):
        for i in range(len(self.parent.mixed)):
            self.parent.mixed[i] = 0
            # Mixed strategy of Right focused strategy is a
            # probability distribution over the first few pure strategy list (0, a, b)
            # The greater the b, the more likely the strategy is to played
            checksum = 0
            right_focus = 0
            for s in self.parent.strategy:
                mixed_index = self.parent.mixed.index(s)
                if s[0] != 0:
                    s[mixed_index] = 0
                else:
                    right_focus += 1
            unit = right_focus * (right_focus + 1) / 2.0
            unit = 1 / unit
            i = 0
            print unit
            print right_focus
            while True:
                if right_focus == 0:
                    break
                self.parent.mixed[i] = right_focus * unit
                checksum += right_focus * unit
                right_focus -= 1
                i += 1

            if checksum is not 1:
                print("Mixed checksum is WRONG: ", checksum)
            else:
                print("Checksum is correct")

            self.print_mixed()


class ThePlayer(MyPlayer):
    def __init__(self, name, parent_level):
        MyPlayer.__init__(self, name, parent_level)

