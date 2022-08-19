from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import like


class Game:
    db = 'games'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.info = data['info']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.likes = []
        self.user = None

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM game;'
        results = connectToMySQL(cls.db).query_db(query)
        games = []
        for row in results:
            games.append(cls(row))
        return games

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM game WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) <1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO game (title, info, user_id) VALUES (%(title)s, %(info)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE game SET title=%(title)s, info=%(info)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM game WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getAllWithCreators(cls):
        query = 'SELECT * FROM game LEFT JOIN user ON game.user_id = user.id;'
        results = connectToMySQL(cls.db).query_db(query)
        allGames = []
        for row in results:
            game = cls(row)
            creatorData = {
                'id' : results['user.id'],
                'firstName' : results['firstName'],
                'lastName' : results['lastName'],
                'email' : results['email'],
                'password' : results['password'],
                'createdAt' : results['user.createdAt'],
                'updatedAt' : results['user.updatedAt']
            }
            game.user = user.User(creatorData)
            allGames.append(game)
        return allGames
    
    @classmethod
    def gameCreator(cls, data): 
        query = 'SELECT * FROM game LEFT JOIN user ON game.user_id = user.id WHERE game.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        else: 
            userData = {
                'id' : results[0]['user.id'],
                'firstName' : results[0]['firstName'],
                'lastName' : results[0]['lastName'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'createdAt' : results[0]['user.createdAt'],
                'updatedAt' : results[0]['user.updatedAt']
            }
            return user.User(userData)
    
    @classmethod
    def getGameWithCreator(cls, data):
        game = cls.getOne(data)
        game.user = cls.gameCreator(data)
        return game

    @classmethod
    def gameLikes(cls, data):
        query = 'SELECT * FROM game LEFT JOIN user_like ON game.id = user_like.game_id LEFT JOIN user ON user_like.user_id = user.id WHERE game.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        allLikes = []
        if len(results) < 1:
            return False
        else:
            for row in results:
                print("gameLikes Each Row: ", row)
                userData = {
                    'id' : results['user.id'],
                    'firstName' : results['firstName'],
                    'lastName' : results['lastName'],
                    'email' : results['email'],
                    'password' : results['password'],
                    'createdAt' : results['user.createdAt'],
                    'updatedAt' : results['user.updatedAt']
                }
                print('userData before class assign:', userData)
                liker = user.User(userData)
                print("liker after class assign before append:", liker)
                allLikes.append(liker)
                print("allLikes list after append:", allLikes)
        return allLikes

    @classmethod
    def oneGameWithCreatorAndLikes(cls, data): 
        game = cls.getOne(data)
        game.user = cls.gameCreator(data)
        game.likes = cls.gameLikes(data)
        return game

    @classmethod
    def allGamesWithCreatorAndLikes(cls):
        query = 'SELECT * FROM game;'
        results = connectToMySQL(cls.db).query_db(query)
        allGames = []
        for row in results:
            game = cls(row)
            data = {
                'id': game.id
            }
            game.user = cls.gameCreator(data)
            game.likes = cls.gameLikes(data)
            allGames.append(game)
        return allGames