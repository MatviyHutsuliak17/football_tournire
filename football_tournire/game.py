from team import Team

class Game:
    __homeTeam = ''
    __awayTeam = ''
    __awayTeamScore = 0
    __homeTeamScore = 0
    __gameTime = 0
    __id = 0

    def __init__(self, homeTeam, awayTeam, homeTeamScore, awayTeamScore, gameTime, id):
        self.__homeTeam = homeTeam
        self.__awayTeam = awayTeam
        self.__homeTeamScore = homeTeamScore
        self.__awayTeamScore = awayTeamScore
        self.__gameTime = gameTime
        self.__id = id

    def find_winner(self):
        if self.__homeTeamScore > self.__awayTeamScore:
            self.__homeTeam._Team__points += 3
            self.__homeTeam._Team__wins += 1
            self.__awayTeam._Team__loses += 1

        elif self.__homeTeamScore < self.__awayTeamScore:
            self.__awayTeam._Team__points += 3
            self.__awayTeam._Team__wins += 1
            self.__homeTeam._Team__loses += 1

        else:
            self.__homeTeam._Team__points += 1
            self.__homeTeam._Team__drafts += 1
            self.__awayTeamScore._Team__points += 1
            self.__awayTeam._Team__drafts += 1

    def get_away_team_name(self):
        return self.__awayTeam._Team__name
    
    def get_home_team_name(self):
        return self.__homeTeam._Team__name
    
    def get_game_time(self):
        return self.__gameTime
    
    def __eq__(self, other):
        if isinstance(other, Game):
            return self.__id == other.__id
        return False