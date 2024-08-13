from flask import request
from data.mlb_data_handler import get_mlb_data, parse_all_mlb_teams, get_unique_players
from game.check_players import check_players



def mountRoutes(app, mlb_data):

    # Root
    @app.route('/')
    def index():
        return ''


    # Functional
    @app.route('/seed-data')
    def seedData():
        get_mlb_data()
        return 'success'
    

    @app.route('/parse-mlb-data')
    def parseMlbData():
        parse_all_mlb_teams(mlb_data)
        return 'success'
    

    @app.route('/parse-unique-players')
    def parseUniquePlayers():
        get_unique_players(mlb_data)
        return 'success'


    @app.route('/check-players', methods=['POST'])
    def checkPlayers():
        return check_players(request.json["first"], request.json["second"], mlb_data)
    

    return app