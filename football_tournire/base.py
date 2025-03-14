import sqlite3
from datetime import datetime
from game import Game
from leag import Leag
from team import Team

class Base:
    """This class makes sql commands"""

    db_conn = sqlite3.connect('C:\\Users\\Matviy\\Tecinter\\football_tournire\\db')
    cursor_cmd = db_conn.cursor()


    cmd_leagues_sql = """SELECT * FROM League"""
    cmd_teams_sql = """SELECT name, LeagueId FROM Team"""
    cmd_games_sql = """SELECT * FROM Game"""

    def get_leagues(self, i):
        self.cursor_cmd.execute(self.cmd_leagues_sql)
        result_leagues = self.cursor_cmd.fetchall()
        self.cursor_cmd.execute(self.cmd_teams_sql)
        result_teams = self.cursor_cmd.fetchall()

        leagues = []
        str_teams = []


        for league_row in result_leagues:
            temp_teams = []
            for team_row in result_teams:
                if team_row[1] == league_row[1]:
                    str_teams.append(team_row[0])
                    temp_teams.append(team_row[0])
            leagues.append(Leag(league_row[0], temp_teams))

            
        if i == 'l':
            return leagues
        
        teams = []
        for team in str_teams:
            teams.append(Team(team))
        return teams
    

    def make_game(self, hometeam, awayTeam, homeTeamScore, awayTeamScore, time):
        self.cursor_cmd.execute(f"INSERT INTO Game('homeTeam', 'awayTeam', 'homeTeamScore', 'awayTeamScore', time) VALUES('{hometeam}', '{awayTeam}', {homeTeamScore}, {awayTeamScore}, '{time}')")
        self.db_conn.commit()



