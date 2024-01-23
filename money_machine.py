from database import Database


class MoneyMachine:


    CURRENCY = "₹"
    COIN_VALUES = {"fives": 5, "tens": 10, "twenties": 20}


    def __init__(self, db):
        self.db = db
        self.profit = self.fetch_profit_from_db()


    def make_payment(self, cost, fives, tens, twenties):
        total_payment = self.process_coins(fives, tens, twenties)
        change = total_payment - cost

        if change >= 0:
            self.profit += cost
            self.update_profit_gui() 
            return True
        else:
            return False
        

    def process_coins(self, fives, tens, twenties):
        total_money = fives * self.COIN_VALUES["fives"] + \
                      tens * self.COIN_VALUES["tens"] + \
                      twenties * self.COIN_VALUES["twenties"]
        return total_money


    def update_profit_gui(self):
        if self.gui_callback:
            self.gui_callback(self.profit)
            self.db.execute_query("UPDATE profits SET profit = %s WHERE id = 1", (self.profit,))


    def fetch_profit_from_db(self):
        query = "SELECT profit FROM profits WHERE id = 1"
        result = self.db.fetch_one(query)
        return result[0] if result else 0
