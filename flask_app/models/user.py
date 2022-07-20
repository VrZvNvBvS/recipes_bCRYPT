from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
DB_NAME = 'recipes'

FIRST_LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]{2}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]{8}')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def create_user(cls, data):
        query = '''
                INSERT INTO users (first_name,last_name,email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                '''
        response_query_users = connectToMySQL(DB_NAME).query_db(query, data)
        return response_query_users

    @classmethod
    def get_user_by_email(cls, data):
        query = '''
                SELECT * FROM users WHERE email = %(email)s
                '''
        response_user = connectToMySQL(DB_NAME).query_db(query, data)
        if len(response_user) < 1:
            return False
        return cls(*response_user)

    @classmethod
    def get_user_by_id(cls, data):
        query = '''
                SELECT * FROM users WHERE id = %(id)s
                '''
        response_user = connectToMySQL(DB_NAME).query_db(query, data)
        return cls(*response_user)


#VALIDATION!!!!!!!!!!!!!!!!!!!!!!


    @staticmethod
    def validate_registration(register):
        query = '''
                SELECT * FROM users WHERE email=%(email)s
                '''
        response_query_user = connectToMySQL(DB_NAME).query_db(query, register)

        is_valid = True
        print(register)
        if not FIRST_LAST_NAME_REGEX.match(register['firstname']):
            flash('First name must be at least 2 characters!!', 'register')
            is_valid = False
        if not FIRST_LAST_NAME_REGEX.match(register['lastname']):
            flash('Last name must be at least 2 characters!!', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(register['email']):
            flash("Email must have valid email format!!!", 'register')
            is_valid = False
        if not register['password1'] == register['password2']:
            flash('Passwords do NOT match!', 'register')
            is_valid = False
        if not PASSWORD_REGREX.match(register['password1']):
            flash("Password requires a minimum of 8 characters!!!!!!!!", 'register')
            is_valid = False
        if len(response_query_user) >= 1:
            flash("Invalid Login Credentials!!", 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(login):
        is_valid = True
        query = '''
                SELECT * FROM users WHERE email=%(email)s
                '''
        response_query_user = connectToMySQL(DB_NAME).query_db(query, login)

        if not len(response_query_user) >= 1:
            flash("Invalid Login Credentials!", "login")
            is_valid = False
            return {'user': response_query_user, 'is_valid': is_valid}

        return {'user': response_query_user[0], 'is_valid': is_valid}
