import mysql.connector
from coffee_maker import CoffeeMaker
from menu import Menu
from money_machine import MoneyMachine
from database import Database


class UserManager:


    def __init__(self, host, user, password, database):
        self.db = Database(host, user, password, database)
        self.money_machine = MoneyMachine(self.db)
        self.coffee_maker = CoffeeMaker(self.db)
        self.menu = Menu(self.db)
        self.users = self.fetch_users() 
        self.owner_passcode = "301191"


    def fetch_users(self):
        query = "SELECT username FROM users"
        try:
            result = self.db.fetch_all(query)
            return [user[0] for user in result] if result else []
        except Exception as e:
            return []
        

    def create_account(self, name, username):
        if self.user_exists(username):
            return False

        query = "INSERT INTO users (name, username) VALUES (%s, %s)"
        values = (name, username)

        try:
            result = self.db.execute_query(query, values)
            if result:
                self.users.append(username) 
                return True
            else:
                return False
        except mysql.connector.errors.IntegrityError as e:
            return False
        

    def order_drink(self, username, drink_name):
        drink = self.menu.find_drink(drink_name)
        if drink:
            price = drink['price']
            if self.money_machine.make_payment(username, price):
                self.coffee_maker.make_coffee(drink)
                return True
        return False
    

    def create_custom_drink(self, name, price):
        query = "INSERT INTO drinks (name, price) VALUES (%s, %s)"
        values = (name, price)

        try:
            result = self.db.execute_query(query, values)
            if result:
                self.menu.refresh_menu()  
                return True
            else:
                return False
        except Exception as e:
            return False
        

    def user_exists(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        result = self.db.fetch_one(query, values)

        return result is not None
