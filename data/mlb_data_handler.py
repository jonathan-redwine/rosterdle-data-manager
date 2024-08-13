import statsapi
from datetime import datetime
import json


def get_mlb_data():
    # Get MLB teams
    teams = statsapi.get('teams', {})
    mlb_teams = [
        {
            "id": team["id"],
            "name": team["name"]
        }
        for team in teams["teams"] 
        if team["sport"].get('name', '') == "Major League Baseball"
    ]

    # Define year range
    years = range(2023, datetime.now().year + 1)
    
    # Get every team's roster for all years
    all_mlb_teams = []
    for team in mlb_teams:
        for year in years:
            try:
                roster = statsapi.roster(team["id"], rosterType=None, season=year, date=None)
                all_mlb_teams.append({
                    "id": team["id"],
                    "name": team["name"],
                    "year": year,
                    "roster": roster.split('\n')
                })
            except:
                print('Could not get roster for team {teamName} in {year}'.format(
                    teamName=team["name"],
                    year=year
                ))

    # Write JSON to file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_mlb_teams, f, ensure_ascii=True, indent=4)

    return all_mlb_teams


def load_mlb_data():
    with open('data.json', 'r') as f:
        try:
            mlb_data = json.load(f)
        except Exception as error:
            mlb_data = [error]

        return mlb_data
    

def get_unique_players(data):
    players = []
    player_id = 0
    for team in data:
        for player in team["roster"]:
            player_info = player.split(' ')
            try:
                player_name = " ".join([player_info[-2], player_info[-1]])
            except:
                pass
            if not player_name in [p["name"] for p in players]:
                players.append({
                    "id": player_id,
                    "name": player_name
                })
                player_id += 1
    
    # Write unique players JSON to file
    with open('unique_players.json', 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=True, indent=4)


def parse_all_mlb_teams(teams):
    print("PARSING ALL DATA!")
    unique_players = get_unique_players(teams)
    all_players = {}
    for team in teams:
        team_name = str(team["year"]) + " " + team["name"]
        for player in team["roster"]:
            player_info = player.split(' ')
            try:
                player_name = " ".join([player_info[-2], player_info[-1]])
            except:
                pass
            
            this_player_id = get_this_player_id(unique_players, player_name)
            these_teammates = [get_player_name(p) for p in team["roster"] if valid_player_name(p)]
            if this_player_id in list(all_players.keys()):
                all_players[this_player_id]["teams"].append(team_name)
            else:
                all_players[this_player_id] = {
                    "id": this_player_id,
                    "name": player_name,
                    "teams": [team_name],
                    "teammates": []
                }
            for teammate_name in these_teammates:
                if teammate_name is not player_name:
                    teammate_id = get_this_player_id(unique_players, teammate_name)
                    if teammate_id in [t["id"] for t in all_players[this_player_id]["teammates"]]:
                        # THIS COULD CAUSE IT NOT TO WORK, assign by reference?
                        this_teammate = [t for t in all_players[this_player_id]["teammates"] if t["id"] == teammate_id][0]
                        this_teammate["shared_teams"].append(team_name)
                    else:
                        all_players[this_player_id]["teammates"].append({
                            "id": teammate_id,
                            "shared_teams": [team_name]
                        })
        print('Finished {team}'.format(team=team_name))

    # Write unique players JSON to file
    with open('unique_players.json', 'w', encoding='utf-8') as f:
        json.dump(unique_players, f, ensure_ascii=True, indent=4)

    # Write all players JSON to file
    with open('all_players.json', 'w', encoding='utf-8') as f:
        json.dump(all_players, f, ensure_ascii=True, indent=4)


def get_this_player_id(all_players, player_name):
    this_player = [p for p in all_players if p["name"] == player_name][0]
    return this_player["id"]



def get_player_name(player):
    player_info = player.split(' ')
    return " ".join([player_info[-2], player_info[-1]])


def valid_player_name(player):
    player_info = player.split(' ')
    try:
        " ".join([player_info[-2], player_info[-1]])
        return True
    except:
        return False