class Leag:
    __teams = []
    __name = ""

    def __init__(self, name, teams):
        self.__name = name
        self.__teams = teams

    def get_name(self):
        return self.__name
    
    def get_teams(self):
        return self.__teams
    
    def __str__(self):
        return self.__name

