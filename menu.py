from database import Database

class MenuItem:


    def __init__(self, name, water, milk, coffee, cost):
        self.name = name
        self.cost = cost
        self.ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee
        }


class Menu:


    def __init__(self, db):
        self.db = db
        self.menu = self.fetch_menu_items()


    def fetch_menu_items(self):
        query = "SELECT * FROM drinks"
        try:
            result = self.db.fetch_all(query)
            menu_items = []
            for row in result:
                menu_items.append(MenuItem(row[1], row[2], row[3], row[4], row[5]))
            return menu_items
        except Exception as e:
            return []


    def add_custom_drink(self, custom_drink):
        self.menu.append(custom_drink)
        query = "INSERT INTO drinks (name, water, milk, coffee, price) VALUES (%s, %s, %s, %s, %s)"
        values = (custom_drink.name, custom_drink.ingredients["water"], custom_drink.ingredients["milk"], custom_drink.ingredients["coffee"], custom_drink.cost)
        self.db.execute_query(query, values)
        

    def get_items(self):
        options = ""
        for item in self.menu:
            options += f"{item.name}/"
        return options


    def find_drink(self, order_name):
        for item in self.menu:
            if item.name == order_name:
                return item
