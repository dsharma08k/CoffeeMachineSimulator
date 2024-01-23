from database import Database

class CoffeeMaker:


    def __init__(self, db, gui_callback=None):
        self.db = db
        self.gui_callback = gui_callback


    def is_resource_sufficient(self, drink):
        can_make = True
        if self.db:

            query = "UPDATE resources SET quantity = quantity - %s WHERE item = %s"
            for item in drink.ingredients:
                values = (drink.ingredients[item], item)
                self.db.execute_query(query, values)

            self.db.connection.commit()

            resource_check_query = "SELECT * FROM resources WHERE item=%s AND quantity >= %s"
            for item in drink.ingredients:
                resource_check_values = (item, drink.ingredients[item])
                result = self.db.execute_query(resource_check_query, resource_check_values)
                if not result:
                    can_make = False

        else:

            for item in drink.ingredients:
                if drink.ingredients[item] > self.resources[item]:
                    can_make = False

        return can_make


    def make_coffee(self, order):
        if self.db:
            query = "UPDATE resources SET quantity = quantity - %s WHERE item = %s"
            for item in order.ingredients:
                values = (order.ingredients[item], item)
                self.db.execute_query(query, values)

        else:
            for item in order.ingredients:
                self.resources[item] -= order.ingredients[item]

        if self.gui_callback:
            self.gui_callback(self.resources)


    def get_current_resources(self):
        if self.db:
            query = "SELECT * FROM resources"
            result = self.db.fetch_all(query)
            if result:
                resources = {item: quantity for _, item, quantity in result}
                return resources
        else:
            return self.resources
