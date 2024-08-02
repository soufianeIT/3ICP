from flask import request, redirect, make_response, render_template
from flask_restful import Resource, reqparse
from models import db, User, Session, Game, Configuration
from datetime import datetime

player_parser = reqparse.RequestParser()
player_parser.add_argument('username', type=str, required=True, help="Name of the player")

class PlayerResource(Resource):
    def get(self, player_id=None):
        if player_id in request.args:
            player = User.query.get(request.args.get('player_id'))
            
            if player:
                return player.serialize(), 200
            return {'message': 'Player not found'}, 404
        else:
            players = User.query.all()
            return [player.serialize() for player in players], 200

    def post(self):
        if request.form:
            print("Hello Heath")
            print(request.form['username'])
            player = User(username=request.form['username'], isGuest=0, createdAt=datetime.now())
            print(player)
        else:
            print("Hello Mars")
            args = player_parser.parse_args()
            print(args)
            player = User(username=args['username'], isGuest=0, createdAt=datetime.now())

        db.session.add(player)
        db.session.commit()
        if request.form:
            return redirect('/players')
        else:
            return {'message': 'Player created', 'id': player.id}, 201

session_parser = reqparse.RequestParser()
session_parser.add_argument('start_date', type=str, required=True, help="Start date of the session")
session_parser.add_argument('creator_id', type=int, required=True)
session_parser.add_argument('players', type=list, location='json')

class SessionResource(Resource):
    def get(self, session_id=None):
        if session_id:
            session = Session.query.get(session_id)
            if session:
                return {
                    'id': session.id,
                    'start_date': session.start_date,
                    'end_date': session.end_date,
                    'creator_id': session.creator_id,
                    'players': [player.id for player in session.players]
                }, 200
            return {'message': 'Session not found'}, 404
        else:
            sessions = Session.query.all()
            return [session.serialize() for session in sessions], 200

    def post(self):
        args = session_parser.parse_args()
        session = Session(start_date=datetime.utcnow(), end_date=None, creator_id=args['creator_id'],)
        db.session.add(session)
        if args['players']:
            for player_id in args['players']:
                player = User.query.get(player_id)
                if player:
                    session.players.append(player)
        db.session.commit()
        return {'message': 'Session created', 'id': session.id}, 201

    def put(self):
        
        data = request.get_json()
        session_id = data['session_id']
        
        session = Session.query.get(session_id)
        if session:
            session.end_date = datetime.utcnow()
            db.session.commit()
            return {'message': 'Session updated', 'id': session.id}, 200
        return {'message': 'Session not found'}, 404

game_parser = reqparse.RequestParser()
game_parser.add_argument('start_date', type=str, required=True)
game_parser.add_argument('end_date', type=str)
game_parser.add_argument('score', type=int, required=True)
game_parser.add_argument('session_id', type=int, required=True)
game_parser.add_argument('player_id', type=int, required=True)

class GameResource(Resource):
    def get(self, game_id=None):
        if game_id:
            game = Game.query.get(game_id)
            if game:
                return {
                    'id': game.id,
                    'start_date': game.start_date,
                    'end_date': game.end_date,
                    'score': game.score,
                    'session_id': game.session_id,
                    'player_id': game.player_id
                }, 200
            return {'message': 'Game not found'}, 404
        
        games = Game.query.all()
        return [game.serialize() for game in games], 200

class ConfigurationResource(Resource):
    def get(self, id=None):
        if (id):
            config = Configuration.query.get(id)
            if config is None:
                return make_response(render_template('pages-error-404.html'))
            return config.serialize(), 200

    def post(self, id=None):
        if request.form.get('_method') == 'PUT':
            return self.put(id=id)

    def put(self, id=None):
        data = request.form
        if (id):
            config = Configuration.query.get(id)
            if config is None:
                return {"message": "No configuration found"}, 404
            config.diceCount = data['default_dice_count']
            config.gameCount = data['max_games_per_session']
            config.playerCount = data['player_count']
            config.updated_at = datetime.utcnow()
            db.session.commit()
            return config.serialize(), 200
        else:
            make_response(render_template('pages-error-404.html')), 404