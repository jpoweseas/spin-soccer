class Team:

    def __init__(self, players):
        self.score = 0
        self.players = players

    def inc_score(self):
        self.score += 1