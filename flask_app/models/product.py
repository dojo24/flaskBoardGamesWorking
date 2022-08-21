from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import orderd

class Product:
    db = 'flask_store'
    def __init__(self, data):
        self.id = data['id']
        self.item = data['item']
        self.info = data['info']
        self.price = data['price']
        self.user_id = data['user_id']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.creator = []
        self.ordered = []
        self.who = None


    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM product;'
        results = connectToMySQL(cls.db).query_db(query)
        products = []
        for row in results:
            products.append(cls(row))
        return products

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM product WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO product (item, info, price, user_id) VALUES (%(item)s, %(info)s, %(price)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE product SET item=%(item)s, info=%(info)s, price=%(price)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM product WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def creator(cls, data):
        query = 'SELECT * FROM product LEFT JOIN user on product.user_id = user.id WHERE product.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        # print('creator method results:', results)
        product = cls(results[0])
        creator = {
            'id': results[0]['user.id'],
            'firstName': results[0]['firstName'],
            'lastName': results[0]['lastName'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'createdAt': results[0]['user.createdAt'],
            'updatedAt': results[0]['user.updatedAt']
        }
        product.creator = user.User(creator)
        # print('the user:', product.creator)
        return product

    @classmethod
    def ordered(cls, data): # Used for count
        query = 'SELECT * FROM product LEFT JOIN orderd ON product.id = orderd.product_id WHERE product.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        allOrdered = []
        for row in results:
            # product = cls(row)
            if not row['product_id'] == None:
                orderedData = {
                    'id': row['orderd.id'],
                    'product_id': row['product_id'],
                    'user_id': row['user_id'],
                    'createdAt': row['orderd.createdAt'],
                    'updatedAt': row['orderd.updatedAt']
                }
                ordered = orderd.Ordered(orderedData)
                allOrdered.append(ordered)
        return allOrdered

    @classmethod
    def allItemsNumberOrdered(cls):
        query = 'SELECT * FROM product;'
        results = connectToMySQL(cls.db).query_db(query)
        allOrdered = []
        for row in results:
            item = cls(row)
            data = {
                'id': item.id
            }
            item.ordered = cls.ordered(data)
            allOrdered.append(item)
        return allOrdered

    @classmethod
    def whoOrdered(cls, data):
        query = 'SELECT * FROM product LEFT JOIN orderd ON product.id = orderd.product_id LEFT JOIN user ON orderd.user_id = user.id WHERE product.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        theOrders = []
        for row in results:
            item = cls(row)
            if not row['user.id'] == None:
                orderer = {
                    'id': row['user.id'],
                    'firstName': row['firstName'],
                    'lastName': row['lastName'],
                    'email': row['email'],
                    'password': row['password'],
                    'createdAt': row['user.createdAt'],
                    'updatedAt': row['user.updatedAt']
                }
                item.who = user.User(orderer)
                theOrders.append(item)
        return theOrders

        