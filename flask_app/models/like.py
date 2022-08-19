from flask_app.config.mysqlconnection import connectToMySQL

class Like:
    db = 'games'
    def __init__(self, data):
        self.id = data['id']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.game_id = data['game_id']

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM user_like;'
        results = connectToMySQL(cls.db).query_db(query)
        likes = []
        for row in results:
            likes.append(cls(row))
        return likes

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM user_like WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO user_like (user_id, game_id) VALUES (%(user_id)s, %(game_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM user_like WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)