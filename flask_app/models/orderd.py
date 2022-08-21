from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Ordered:
    db = 'flask_store'
    def __init__(self, data):
        self.id = data['id']
        self.product_id = data['product_id']
        self.user_id = data['user_id']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO orderd (product_id, user_id) VALUES (%(product_id)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM orderd WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
