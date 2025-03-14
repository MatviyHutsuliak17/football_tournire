import tkinter as tk
import sqlite3
from tkinter import ttk
from game import Game
from base import Base
from datetime import datetime

# Functions
def update():
    """This function updates table"""

    update_table()
    tab3_content()


def tab3_check():
    pass


def change_detail(homeTeam, awayTeam, homeTeamScore, awayTeamScore, gameTime):
    """This function displays avaible games for change"""

    if temp_widgets:
        hide_widgets(temp_widgets)

    confirmButtontab3 = tk.Button(tab3, text="Підтвердити", command= lambda: change(homeTeam, awayTeam, homeTeamScore, awayTeamScore, gameTime))

    warnLableTab3.place(x=0, y=30)
    gameTimeLableTab3.place(x=20, y=50)
    tab3Entry.place(x=0, y=70)

    selectedLeaguetab3 = tk.StringVar()
    selectedLeaguetab3.set(leaguesOptions[0])
    show_teams_tab3(leagues[0])

    leaguesOptionsControl3 = tk.OptionMenu(tab3, selectedLeaguetab3, *leagues, command=lambda value: show_teams_tab3(value))
    leaguesOptionsControl3.place(x=300, y=90)   

    confirmButtontab3.place(x=0, y=90)

    tab3Entry.delete(0, tk.END)
    tab3Entry.insert(0, f"{homeTeam}/{awayTeam}/{homeTeamScore}/{awayTeamScore}/{gameTime}")

    temp_widgets.extend([leaguesOptionsControl3, tab3Entry, gameTimeLableTab3, warnLableTab3, confirmButtontab3])
    

def change(homeTeam, awayTeam, homeTeamScore, awayTeamScore, gameTime):
    """This function changes information of game"""

    if temp_widgets:
        hide_widgets(temp_widgets)

    db_conn = sqlite3.connect('C:\\Users\\Matviy\\Tecinter\\football_tournire\\db')
    cursor_cmd = db_conn.cursor()
    cmd_games_sql = """SELECT * FROM Game"""
    cursor_cmd.execute(cmd_games_sql)

    tab3Content = tab3Entry.get().split('/')
    new_home_score = int(tab3Content[2])
    new_away_score = int(tab3Content[3])
    new_game_time = tab3Content[4]

    update_query = """
        UPDATE Game
        SET homeTeamScore = ?, awayTeamScore = ?, time = ?
        WHERE homeTeam = ? AND awayTeam = ? AND homeTeamScore = ? AND awayTeamScore = ? AND time = ?
    """
    cursor_cmd.execute(update_query, (new_home_score, new_away_score, new_game_time, homeTeam, awayTeam, homeTeamScore, awayTeamScore, gameTime))

    db_conn.commit()
    db_conn.close()


    read_games()
    tab3_content()


def tab3_content():
    """This function displays tab3 content"""
    
    if temp_widgets:
        hide_widgets(temp_widgets)

    db_conn = sqlite3.connect('C:\\Users\\Matviy\\Tecinter\\football_tournire\\db')
    cursor_cmd = db_conn.cursor()
    cmd_games_sql = """SELECT * FROM Game"""
    cursor_cmd.execute(cmd_games_sql)
    result_games = cursor_cmd.fetchall()

    i = 0
    for game_row in result_games:
        i += 30

        homeTeam = game_row[0]
        awayTeam = game_row[1]

        homeTeamScore = game_row[2]
        awayTeamScore = game_row[3]

        gameTimeRead = game_row[4]

        gameTimeTab3 = datetime.strptime(gameTimeRead.strip(), "%Y-%m-%d %H:%M")

        for game in games:
            if game.get_home_team_name() == homeTeam and awayTeam == game.get_away_team_name() and game.get_game_time() == gameTimeTab3 and gameTimeTab3 >= datetime.now():
                btn = tk.Button(tab3, text=f"{homeTeam}:{homeTeamScore} {awayTeam}{awayTeamScore} {gameTimeRead[-1]}",  
                        command=lambda homeTeam=homeTeam, awayTeam=awayTeam, homeTeamScore=homeTeamScore, awayTeamScore=awayTeamScore, gameTime=gameTimeRead.strip():  
                        change_detail(homeTeam, awayTeam, homeTeamScore, awayTeamScore, gameTime))  
                btn.place(x=0, y=i)  
                temp_widgets.append(btn)
                break


def check():
    """This function checks Entries"""
    time = gameTime.get()
    try:
        datetime.strptime(time, "%Y-%m-%d %H:%M")
        reset()
    except ValueError:
        incorrectLable.place(x=160, y=230)


def update_table():
    """This function updates table"""

    global table

    if table is not None:
        table.destroy()

    read_games()
    print_table()


def print_table():
    """This function prints table"""

    global table

    sorted_teams = sorted(teams, key=lambda v: v.get_points(), reverse=True)
    columns = ('team', 'L', 'W', 'D', 'P')

    table = ttk.Treeview(tab1, columns=columns, show='headings')
    data = []
    
    for team in sorted_teams:
        print(team.get_name(), team.get_points())
        data.append((team.get_name(), team.get_loses(), team.get_wins(), team.get_drafts(), team.get_points()))

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=80, anchor="center")

    for row in data:
        table.insert("", tk.END, values=row)

    table.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)


def reset():
    """This function resets selcted game"""

    make_game(selectedHomeTeam.get(), selectedAwayTeam.get(), homeGoalsEntry.get(), awayGoalsEntry.get(), gameTime.get())

    if incorrectLable.winfo_ismapped():
        incorrectLable.place_forget()

    gameTime.delete(0, tk.END)

    homeGoalsEntry.delete(0, tk.END)
    awayGoalsEntry.delete(0, tk.END)

    selectedLeague.set(leaguesOptions[0])
    selectedLeague2.set(leaguesOptions[0])

    selectedHomeTeam.set(teamsOptions[0])
    selectedAwayTeam.set(teamsOptions[0])



def read_games():
    """This function reads games"""
    games.clear()

    db_conn = sqlite3.connect('C:\\Users\\Matviy\\Tecinter\\football_tournire\\db')
    cursor_cmd = db_conn.cursor()
    cmd_games_sql = """SELECT * FROM Game"""
    cursor_cmd.execute(cmd_games_sql)
    result_games = cursor_cmd.fetchall()

    for game_row in result_games:

        homeTeam = game_row[0]
        awayTeam = game_row[1]

        homeTeamScore = game_row[2]
        awayTeamScore = game_row[3]

        gameTimeRead = game_row[4]

        home_team_obj = None
        away_team_obj = None

        for team in teams:
            if home_team_obj and away_team_obj:
                break
            if team.get_name() == homeTeam:
                home_team_obj = team
            elif team.get_name() == awayTeam:
                away_team_obj = team
        if home_team_obj and away_team_obj:
            temp_game = Game(home_team_obj, away_team_obj, homeTeamScore, awayTeamScore, datetime.strptime(gameTimeRead, "%Y-%m-%d %H:%M"), game_row[-1])
            if temp_game not in added_games:
                games.append(temp_game)

    for game in games:
        if game.get_game_time() <= datetime.now() and game not in added_games:
            game.find_winner()
            added_games.append(game)
        


def make_game(homeTeam, awayTeam, homeTeamGoals, awayteamGoals, gameTime):
    """This function makes game"""

    base.make_game(homeTeam, awayTeam, homeTeamGoals, awayteamGoals, gameTime)
    
    read_games()
    tab3_content()
    update_table()


def hide_widgets(widgets):
    """This function hides widgets"""
    for widget in widgets:
        widget.place_forget()





def show_away_teams(league):
    """This function shows away teams"""

    global selectedAwayTeam

    if temp_widgets_away_teams:
        hide_widgets(temp_widgets_away_teams)

    teamsOptions = [team for team in league.get_teams()]

    selectedAwayTeam = tk.StringVar()
    selectedAwayTeam.set(teamsOptions[0])

    teamsOptionsControl =  tk.OptionMenu(tab2, selectedAwayTeam, *teamsOptions)
    teamsOptionsControl.place(x=300, y=70)
        
    temp_widgets_away_teams.append(teamsOptionsControl)

def show_teams_tab3(league):
    teamsOptions = [team for team in league.get_teams()]

    selectedHomeTeam = tk.StringVar()
    selectedHomeTeam.set(teamsOptions[0])

    teamsOptionsControl =  tk.OptionMenu(tab3, selectedHomeTeam, *teamsOptions)
    teamsOptionsControl.place(x=300, y=130)

    temp_widgets.append(teamsOptionsControl)


def show_home_teams(league):
    """This function shows home teams"""

    global selectedHomeTeam, teamsOptions

    if temp_widgets_home_teams:
        hide_widgets(temp_widgets_home_teams)

    teamsOptions = [team for team in league.get_teams()]

    selectedHomeTeam = tk.StringVar()
    selectedHomeTeam.set(teamsOptions[0])

    teamsOptionsControl =  tk.OptionMenu(tab2, selectedHomeTeam, *teamsOptions)
    teamsOptionsControl.place(x=40, y=70)
        
    temp_widgets_home_teams.append(teamsOptionsControl)


# window settings
window = tk.Tk()
window.geometry("500x300+500+300")

# Base
base = Base()

# variables
added_games = []
teams = base.get_leagues(i='t')
games = []
leagues = base.get_leagues(i='l')
temp_widgets_home_teams = []
temp_widgets_away_teams = []
temp_widgets = []


# Buttons, Lables, tabControl ....
    # TabControl
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

    # TabControl
tabControl.add(tab1, text="Таблиця")
tabControl.add(tab2, text="Додати гру")
tabControl.add(tab3, text="Зміни")

tabControl.pack(expand=1, fill="both")
    # Lables
homeLable = tk.Label(tab2, text='Виберіть домашню команду')
awayLable = tk.Label(tab2, text='Виберіть гостьову команду')

gameTimeLable = tk.Label(tab2, text="Введіть час проведення гри в форматі: Y-m-d H:M")
incorrectLable = tk.Label(tab2, text="Не правильно написано час!!! Не вводіть БУКВИ!!!")
gameTimeLable.place(x=170, y=170)


homeLable.place(x=40, y=20)
awayLable.place(x=300, y=20)
    # Option Menu
leaguesOptions = [i.get_name() for i in leagues]

selectedLeague = tk.StringVar()
selectedLeague.set(leaguesOptions[0])
show_home_teams(leagues[0])

leaguesOptionsControl = tk.OptionMenu(tab2, selectedLeague, *leagues, command=lambda value: show_home_teams(value))
leaguesOptionsControl.place(x=40, y=40)

selectedLeague2 = tk.StringVar()
selectedLeague2.set(leaguesOptions[0])
show_away_teams(leagues[0])

leaguesOptionsControl2 = tk.OptionMenu(tab2, selectedLeague2, *leagues, command=lambda value: show_away_teams(value))
leaguesOptionsControl2.place(x=300, y=40)
    #Entry
awayGoalsEntry = tk.Entry(tab2)
awayGoalsEntry.place(x=303 ,y=120)

homeGoalsEntry = tk.Entry(tab2)
homeGoalsEntry.place(x=43, y=120)

gameTime = tk.Entry(tab2)
gameTime.place(x=180, y=200)
    # Buttons
changesButton = tk.Button(tab3, text='')

confirmButton = tk.Button(tab2, text='Підтвердити', command=check)
confirmButton.place(x=200, y=245)

# call-up functions
read_games()
print_table()
tab3_content()
updateButton = tk.Button(tab1, text='Оновити', command=update)
updateButton.place(x=400, y=0)
    #tab3 Content  
tab3Entry = tk.Entry(tab3, width=60)

gameTimeLableTab3 = tk.Label(tab3, text="Введіть час проведення гри в форматі: Y-m-d H:M")

warnLableTab3 = tk.Label(tab3, text='Дані записані в форматі: домашня команда/голи домашньої команди/гостьова команда/голи гостьової команди/дата гри')

# window updating
window.mainloop()