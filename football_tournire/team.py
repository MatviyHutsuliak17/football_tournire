class Team:
    __name = ''
    __points = 0
    __wins = 0
    __drafts = 0
    __loses = 0

    def __init__(self,  name, points=0, wins=0, drafts=0, loses=0):
        self.__name = name
        self.__points = points
        self.__drafts = drafts
        self.__wins = wins
        self.__loses = loses


    def get_name(self):
        return self.__name
    
    def get_loses(self):
        return self.__loses
    
    def get_drafts(self):
        return self.__drafts
    
    def get_wins(self):
        return self.__wins
    
    def get_points(self):
        return self.__points
    