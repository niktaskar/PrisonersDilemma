
class Game:

    NUM_PLAYERS = 0
    PLAYERS = list()

    def generatePlayers(self):
        for i in range(self.NUM_PLAYERS):
            if i%4 is 0:
                self.PLAYERS.append(Game.T4T())
            elif i%4 is 1:
                self.PLAYERS.append(Game.Grudger())
            elif i%4 is 2:
                self.PLAYERS.append(Game.AC())
            else:
                self.PLAYERS.append(Game.AD())

    def __init__(self, n):
        super().__init__()
        self.NUM_PLAYERS = n
        self.generatePlayers()

    class T4T:
        def __init__(self):
            super().__init__()
            print("T4T")

    class Grudger:
        def __init__(self):
            super().__init__()
            print("Grudger")

    class AC:
        def __init__(self):
            super().__init__()
            print("AC")

    class AD:
        def __init__(self):
            super().__init__()
            print("AD")


if __name__ == "__main__":
    game = Game(4)
    print("Game initialized with 4 players")