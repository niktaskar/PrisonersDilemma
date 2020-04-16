import matplotlib.pyplot as plt

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
                    # print(player1.getClass() + ": " + str(p1Action) + "\t" + player2.getClass() + ": " + str(p2Action))
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

                    if isinstance(player1, Game.T4T) or isinstance(player1, Game.Grudger):
                        player1.OPPONENT_MOVES.append(p2Action)
                    elif isinstance(player2, Game.T4T) or isinstance(player2, Game.Grudger):
                        player2.OPPONENT_MOVES.append(p1Action)
                
                if isinstance(self.PLAYERS[i], Game.T4T):
                    self.PLAYERS[i].OPPONENT_MOVES = list()
                    self.PLAYERS[i].CURR_ROUND = 0
                elif isinstance(self.PLAYERS[i], Game.Grudger):
                    self.PLAYERS[i].OPPONENT_MOVES = list()

                if isinstance(self.PLAYERS[j], Game.T4T):
                    self.PLAYERS[j].OPPONENT_MOVES = list()
                    self.PLAYERS[j].CURR_ROUND = 0
                elif isinstance(self.PLAYERS[j], Game.Grudger):
                    self.PLAYERS[j].OPPONENT_MOVES = list()


    def replacePlayers(self, p, scoreList, scores):
        count = int((len(scoreList)*p)/100)
        print("Low Value: " + str(scoreList[int(count)-1]) + "\t High Value: " + str(scoreList[len(scoreList)-int(count)]))
        players = self.PLAYERS
        self.PLAYERS = list()
        toAddAgain = set()
        for key in scores:
            for i in range(count, len(scoreList)):
                if scores.get(key) == scoreList[i]:
                    if i > len(scoreList) - count:
                        print("HIGH VALUES" + str(key))
                        if key.__contains__("Tit-4-Tat"):
                            player = Game.T4T()
                        elif key.__contains__("Grudger"):
                            player = Game.Grudger()
                        elif key.__contains__("Always Cooperate"):
                            player = Game.AC()
                        else:
                            player = Game.AD()
                        
                        if len(self.PLAYERS) < self.NUM_PLAYERS:
                            self.PLAYERS.append(player)

                        # if isinstance(player, Game.T4T) and Game.T4T not in toAddAgain:
                        #     toAddAgain.add(Game.T4T)
                        # elif isinstance(player, Game.Grudger) and Game.Grudger not in toAddAgain:
                        #     toAddAgain.add(Game.Grudger)
                        # elif isinstance(player, Game.AC) and Game.AC not in toAddAgain:
                        #     toAddAgain.add(Game.AC)
                        # elif isinstance(player, Game.AD) and Game.AD not in toAddAgain:
                        #     toAddAgain.add(Game.AD)
                    else:
                        print("MIDDLE VALUES")
                        if key.__contains__("Tit-4-Tat"):
                            player = Game.T4T()
                        elif key.__contains__("Grudger"):
                            player = Game.Grudger()
                        elif key.__contains__("Always Cooperate"):
                            player = Game.AC()
                        else:
                            player = Game.AD()
                        
                        if len(self.PLAYERS) < self.NUM_PLAYERS:
                            self.PLAYERS.append(player)
        
        print(toAddAgain)
        # for i in range(self.NUM_PLAYERS-len(self.PLAYERS)):
        #     if i % toAddAgain.count == 0:
        #         self.PLAYERS.append(toAddAgain[0])
        #     elif i % len(toAddAgain) == 1:
        #         self.PLAYERS.append(toAddAgain[1])
        #     elif i % len(toAddAgain) == 2:
        #         self.PLAYERS.append(toAddAgain[2])
        #     else:
        #         self.PLAYERS.append(toAddAgain[3])

        print()
        
    
    class GameInstance:
        ACTIONS = {"Cooperate": "C", "Defect": "D"}
        OUTCOMES = {"CC": [3,3], "DC": [5,0], "DD": [1,1], "CD": [0,5]}
        player1 = None
        player2 = None

        def __init__(self, p1, p2):
            super().__init__()
            self.player1 = p1
            self.player2 = p2


    def __init__(self, *args):
        super().__init__()
        if len(args)  != 0:
            self.NUM_PLAYERS = args[0]
            self.NUM_ROUNDS = args[1]


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
            self.CURR_ROUND += 1
            if self.CURR_ROUND == 1 or len(self.OPPONENT_MOVES) == 0:
                return Game.GameInstance.ACTIONS.get("Cooperate")
            return self.OPPONENT_MOVES[len(self.OPPONENT_MOVES)-1]

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
            if len(self.OPPONENT_MOVES) > 0 and "D" in self.OPPONENT_MOVES:
                return Game.GameInstance.ACTIONS.get("Defect")
            else:
                return Game.GameInstance.ACTIONS.get("Cooperate")

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


def createGraph(scores, i):
    typeScoreDict = {"Tit-4-Tat": 0, "Grudger": 0, "AC": 0, "AD": 0}
    for key in scores:
        if key.__contains__("Tit-4-Tat"):
            typeScoreDict["Tit-4-Tat"] += scores.get(key)
        elif key.__contains__("Grudger"):
            typeScoreDict["Grudger"] += scores.get(key)
        elif key.__contains__("Cooperate"):
            typeScoreDict["AC"] += scores.get(key)
        else:
            typeScoreDict["AD"] += scores.get(key)

    print(str(typeScoreDict))

    plt.bar(range(len(typeScoreDict)), list(typeScoreDict.values()), align='center')
    plt.xticks(range(len(typeScoreDict)), list(typeScoreDict.keys()))
    plt.savefig("PD_graphs/generation_" + str(i) + ".png")


if __name__ == "__main__":
    n = 4
    m = 5
    p = 25
    k = 3
    previous = Game()
    game = Game(n, m)
    game.generatePlayers()

    print("NUMBER OF PLAYERS IN ROUND 0: " + str(len(game.PLAYERS)))
    game.runGames()

    scores = {str(game.PLAYERS[i].getClass()+"-"+str(i)): sum(game.PLAYERS[i].PAYOUTS) for i in range(len(game.PLAYERS))}
    print("SCORES: " + str(scores))
    scoreList = [scores.get(val) for val in scores]
    scoreList.sort()
    print("SCORELIST: " + str(scoreList))

    createGraph(scores, 0)
    game.replacePlayers(p, scoreList, scores)
    scores = {}
    scoreList = []

    for i in range(1, k):
        print("NUMBER OF PLAYERS IN ROUND " + str(i) + ": " + str(len(game.PLAYERS)))

        game.runGames()
        createGraph(scores, i)

        scores = {str(game.PLAYERS[i].getClass()+"-"+str(i)): sum(game.PLAYERS[i].PAYOUTS) for i in range(len(game.PLAYERS))}
        print("SCORES: " + str(scores))
        scoreList = [scores.get(val) for val in scores]
        scoreList.sort()
        print("SCORELIST: " + str(scoreList))
        game.replacePlayers(p, scoreList, scores)
        scores = {}
        scoreList = []
