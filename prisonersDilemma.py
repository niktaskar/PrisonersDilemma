
class Game:

    NUM_PLAYERS = 0
    PLAYERS = list()
    PREV_GAMES = {}
    NUM_ROUNDS = 0

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

    def runGames(self):
        for i in range(len(self.PLAYERS)):
            for j in range(i+1, len(self.PLAYERS)):
                for turn in range(self.NUM_ROUNDS):
                    player1 = self.PLAYERS[i]
                    player2 = self.PLAYERS[j]
                    gameInstance = Game.GameInstance(player1, player2)
                    p1Action = gameInstance.player1.play()
                    p2Action = gameInstance.player2.play()
                    print(player1.getClass() + ": " + str(p1Action) + "\t" + player2.getClass() + ": " + str(p2Action))
                    if(p1Action == "C" and p2Action == "C"):
                        player1.PAYOUTS.append(gameInstance.OUTCOMES.get("CC")[0])
                        player2.PAYOUTS.append(gameInstance.OUTCOMES.get("CC")[1])
                    elif(p1Action == "C" and p2Action == "D"):
                        player1.PAYOUTS.append(gameInstance.OUTCOMES.get("CD")[0])
                        player2.PAYOUTS.append(gameInstance.OUTCOMES.get("CD")[1])
                    elif(p1Action == "D" and p2Action == "C"):
                        player1.PAYOUTS.append(gameInstance.OUTCOMES.get("DC")[0])
                        player2.PAYOUTS.append(gameInstance.OUTCOMES.get("DC")[1])
                    else:
                        player1.PAYOUTS.append(gameInstance.OUTCOMES.get("DD")[0])
                        player2.PAYOUTS.append(gameInstance.OUTCOMES.get("DD")[1])

                    if isinstance(player1, Game.T4T):
                        player1.OPPONENT_MOVES.append(p2Action)
                    elif isinstance(player2, Game.T4T):
                        player2.OPPONENT_MOVES.append(p1Action)
    
    class GameInstance:
        ACTIONS = {"Cooperate": "C", "Defect": "D"}
        OUTCOMES = {"CC": [3,3], "DC": [5,0], "DD": [1,1], "CD": [0,5]}
        player1 = None
        player2 = None

        def __init__(self, p1, p2):
            super().__init__()
            self.player1 = p1
            self.player2 = p2


    def __init__(self, n, m):
        super().__init__()
        self.NUM_PLAYERS = n
        self.NUM_ROUNDS = m
        self.generatePlayers()
        self.runGames()
        

    '''
        Tit-4-Tat player
        Starts by cooperating in first round
        Plays opponents previous move in subsequent rounds
    '''
    class T4T:
        CURR_ROUND = 0
        OPPONENT_MOVES = list()
        PAYOUTS = list()

        def __init__(self):
            super().__init__()
        
        def play(self):
            if self.CURR_ROUND == 0:
                return Game.GameInstance.ACTIONS.get("Cooperate")
            return self.OPPONENT_MOVES[len(self.OPPONENT_MOVES)-1]
            self.CURR_ROUND += 1

        def getClass(self):
            return "Tit-4-Tat"

    '''
        Grudger player
        Will cooperate until other player defects then will defect
    '''
    class Grudger:
        PAYOUTS = list()
        OPPONENT_MOVES = list()

        def __init__(self):
            super().__init__()

        def play(self):
            if len(self.OPPONENT_MOVES) > 0:
                if self.OPPONENT_MOVES[len(self.OPPONENT_MOVES)-1] == "D":
                    return "D"
            else:
                return "C"

        def getClass(self):
            return "Grudger"

    '''
        Always Cooperate player
        Always chooses cooperate
    '''
    class AC:
        PAYOUTS = list()

        def __init__(self):
            super().__init__()

        def play(self):
            return Game.GameInstance.ACTIONS.get("Cooperate")

        def getClass(self):
            return "Always Cooperate"

    '''
        Always Defect player
        Always chooses defect
    '''
    class AD:
        PAYOUTS = list()

        def __init__(self):
            super().__init__()
        
        def play(self):
            return Game.GameInstance.ACTIONS.get("Defect")
        
        def getClass(self):
            return "Always Defect"


if __name__ == "__main__":
    n = 4
    m = 2
    game = Game(n, m)
    print("Game initialized with " + str(n) + " players and " + str(m) + " rounds")
    for player in game.PLAYERS:
        print(player.getClass() + ": " + str(sum(player.PAYOUTS)))