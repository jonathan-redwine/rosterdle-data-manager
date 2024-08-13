
def check_players(first, second, mlb_data):
    shared_teams = []
    for team in mlb_data:
        found_first = False
        found_second = False
        for player in team["roster"]:
            player_info = player.split(' ')
            try:
                player_name = " ".join([player_info[-2], player_info[-1]])
            except:
                player_name = "PLAYER NOT FOUND"
            if found_first or player_name == first:
                found_first = True
            if found_second or player_name == second:
                found_second = True
                
        if found_first and found_second:
            shared_teams.append(str(team["year"]) + " " + team["name"])

    return {
        "teams": shared_teams
    }