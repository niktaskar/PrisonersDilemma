import matplotlib.pyplot as plt
from queue import PriorityQueue

class Game:

    NUM_PLAYERS = 0
    PLAYERS = list()
    PREV_GAMES = {}
    NUM_ROUNDS = 0

    def generatePlayers(self):
        for i in range(self.NUM_PLAYERS):
            if i%4 is 2:
                self.PLAYERS.append(Game.T4T())
            elif i%4 is 1:
                self.PLAYERS.append(Game.Grudger())
            elif i%4 is 0:
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

        players = self.PLAYERS
        self.PLAYERS = list()

        pq = PriorityQueue()
        toAddAgain = []
        for key in scores:
            if key.__contains__("Tit-4-Tat"):
                player = Game.T4T()
            elif key.__contains__("Grudger"):
                player = Game.Grudger()
            elif key.__contains__("Always Cooperate"):
                player = Game.AC()
            else:
                player = Game.AD()
            

            pq.put((Game.PlayerScore(player, scores.get(key)), scores.get(key)))

        temp = count
        middleVals = len(scores) - 2*count
        while not pq.empty():
            while temp > 0:
                pq.get()
                temp -= 1
            while middleVals > 0:
                player, value = pq.get()
                pl = player.playerType.getClass()
                if pl.__contains__("Tit-4-Tat"):
                    newPlayer = Game.T4T()
                elif pl.__contains__("Grudger"):
                    newPlayer = Game.Grudger()
                elif pl.__contains__("Always Cooperate"):
                    newPlayer = Game.AC()
                else:
                    newPlayer = Game.AD()

                self.PLAYERS.append(newPlayer)
                middleVals -= 1
            while count > 0:
                player, value = pq.get()
                pl = player.playerType.getClass()
                if pl.__contains__("Tit-4-Tat"):
                    newPlayer = Game.T4T()
                elif pl.__contains__("Grudger"):
                    newPlayer = Game.Grudger()
                elif pl.__contains__("Always Cooperate"):
                    newPlayer = Game.AC()
                else:
                    newPlayer = Game.AD()

                self.PLAYERS.append(newPlayer)
                if pl not in toAddAgain:    
                    toAddAgain.append(pl)
                count -= 1
            
            i = 0
            while len(self.PLAYERS) < len(players):
                if i % len(toAddAgain) == 0:
                    if toAddAgain[i] ==  "Tit-4-Tat":
                        newPlayer = Game.T4T()
                    elif toAddAgain[i] == "Grudger":
                        newPlayer = Game.Grudger()
                    elif toAddAgain[i] == "Always Cooperate":
                        newPlayer = Game.AC()
                    else:
                        newPlayer = Game.AD()
                    self.PLAYERS.append(newPlayer)
                elif i % len(toAddAgain) == 1:
                    if toAddAgain[i] ==  "Tit-4-Tat":
                        newPlayer = Game.T4T()
                    elif toAddAgain[i] == "Grudger":
                        newPlayer = Game.Grudger()
                    elif toAddAgain[i] == "Always Cooperate":
                        newPlayer = Game.AC()
                    else:
                        newPlayer = Game.AD()
                    self.PLAYERS.append(newPlayer)
                elif i % len(toAddAgain) == 2:
                    if toAddAgain[i] ==  "Tit-4-Tat":
                        newPlayer = Game.T4T()
                    elif toAddAgain[i] == "Grudger":
                        newPlayer = Game.Grudger()
                    elif toAddAgain[i] == "Always Cooperate":
                        newPlayer = Game.AC()
                    else:
                        newPlayer = Game.AD()
                    self.PLAYERS.append(newPlayer)
                elif i % len(toAddAgain) == 3:
                    if toAddAgain[i] ==  "Tit-4-Tat":
                        newPlayer = Game.T4T()
                    elif toAddAgain[i] == "Grudger":
                        newPlayer = Game.Grudger()
                    elif toAddAgain[i] == "Always Cooperate":
                        newPlayer = Game.AC()
                    else:
                        newPlayer = Game.AD()
                    self.PLAYERS.append(newPlayer)


    '''
        GameInstance class that holds data corresponding to results of games
        Defines actions that each player can take
        Returns payouts to each player depending on the move played
    '''
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
        PlayerScore class
        Class to encapsulate score and strategy data for each player
        Used in replacePlayers method in order to provide PriorityQueue with comparator
    '''
    class PlayerScore:
        playerType = None
        score = 0

        def __init__(self, playerType, score):
            self.score = score
            self.playerType = playerType
        
        def toString(self):
            return str(self.playerType.getClass()) + ": " + str(self.score)

        def __lt__(self, value):
                return self.score < value.score


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


'''
    Creates bar graphs and saves them in relevant folder
'''
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


    plt.bar(range(len(typeScoreDict)), list(typeScoreDict.values()), align='center')
    plt.xticks(range(len(typeScoreDict)), list(typeScoreDict.keys()))
    plt.savefig("PD_graphs/generation_" + str(i) + ".png")


def countTypes(scores):
    typeCount = {"Tit-4-Tat": 0, "Grudger": 0, "AC": 0, "AD": 0}
    for key in scores:
        if key.__contains__("Tit-4-Tat"):
            typeCount["Tit-4-Tat"] += 1
        elif key.__contains__("Grudger"):
            typeCount["Grudger"] += 1
        elif key.__contains__("Cooperate"):
            typeCount["AC"] += 1
        else:
            typeCount["AD"] += 1

    print(str(typeCount))

    numPlayers = 0
    for key in scores:
        numPlayers += 1
    percentCount = [100*typeCount.get(key)/numPlayers for key in typeCount]
    print(percentCount)


if __name__ == "__main__":
    n = 100
    m = 5
    p = 5
    k = 20
    previous = Game()
    game = Game(n, m)
    game.generatePlayers()

    print("NUMBER OF PLAYERS IN ROUND 0: " + str(len(game.PLAYERS)))
    game.runGames()

    scores = {str(game.PLAYERS[i].getClass()+"-"+str(i)): sum(game.PLAYERS[i].PAYOUTS) for i in range(len(game.PLAYERS))}
    # print("SCORES: " + str(scores))
    scoreList = [scores.get(val) for val in scores]
    scoreList.sort()
    # print("SCORELIST: " + str(scoreList))

    countTypes(scores)
    createGraph(scores, 0)
    game.replacePlayers(p, scoreList, scores)
    scores = {}
    scoreList = []

    for i in range(1, k):
        print("NUMBER OF PLAYERS IN ROUND " + str(i) + ": " + str(len(game.PLAYERS)))

        game.runGames()

        scores = {str(game.PLAYERS[i].getClass()+"-"+str(i)): sum(game.PLAYERS[i].PAYOUTS) for i in range(len(game.PLAYERS))}
        # print("SCORES: " + str(scores))
        scoreList = [scores.get(val) for val in scores]
        scoreList.sort()
        # print("SCORELIST: " + str(scoreList))
        countTypes(scores)
        createGraph(scores, i)

        game.replacePlayers(p, scoreList, scores)
        scores = {}
        scoreList = []
