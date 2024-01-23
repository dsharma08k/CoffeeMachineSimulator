from user_manager import UserManager
from gui import CoffeeMachineGUI

db_host="your_host",
db_user="your_user",
db_password="your_password",
db_database="your_database_name"

user_manager = UserManager(host=db_host, user=db_user, password=db_password, database=db_database)
coffee_machine_gui = CoffeeMachineGUI(user_manager)
coffee_machine_gui.run()
