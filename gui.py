import tkinter as tk
from tkinter import simpledialog, messagebox,ttk
from user_manager import UserManager
from coffee_maker import CoffeeMaker
from menu import Menu,MenuItem
from money_machine import MoneyMachine
from database import Database


class CoffeeMachineGUI:


    def __init__(self, user_manager, user=None, password=None, database=None):

        self.root = tk.Tk()
        self.user_manager = user_manager

        self.window = None
        self.profit_label = None

        self.root.title("Coffee Machine Simulator")
        self.user_manager.money_machine.gui_callback = self.update_profit_label

        self.label_title = tk.Label(self.root, text="Coffee Machine Simulator", font=("Helvetica", 16))
        self.label_title.pack(pady=10)

        self.label_resources = tk.Label(self.root, text="")
        self.label_resources.pack(pady=10)

        self.coffee_maker = CoffeeMaker(user_manager.coffee_maker.db, gui_callback=self.update_resources_label)

        self.button_create_account = tk.Button(self.root, text="Create Account", command=self.create_account)
        self.button_create_account.pack(pady=5)

        self.button_buy_coffee = tk.Button(self.root, text="Buy Coffee", command=self.buy_coffee)
        self.button_buy_coffee.pack(pady=5)

        self.button_view_functionality = tk.Button(self.root, text="View Functionality",
                                                   command=self.view_functionality)
        self.button_view_functionality.pack(pady=5)
     

    def create_account(self):

        name = simpledialog.askstring("Create Account", "Enter your name:")
        username = simpledialog.askstring("Create Account", "Enter a unique username:")

        if name and username:
            if self.user_manager.create_account(name, username):
                messagebox.showinfo("Account Created",
                                    f"Account created successfully for {name} with username {username}")
            else:
                messagebox.showerror("Account Creation Failed", "Username already exists. Please choose another username.")
        else:
            messagebox.showerror("Invalid Input", "Please enter both name and username.")


    def buy_coffee(self):
        username = simpledialog.askstring("Buy Coffee", "Enter your username:")
        if username:
            if username in self.user_manager.users:
                options = self.user_manager.menu.get_items()
                choice = simpledialog.askstring("Buy Coffee", f"What would you like? ({options}): ")

                if choice:
                    drink = self.user_manager.menu.find_drink(choice)
                    self.show_payment_frame(drink, username)
                else:
                    messagebox.showerror("Invalid Drink", "Please choose a valid drink.")
            else:
                messagebox.showerror("Account Not Found", "No account found for the given username. Please create an account.")
        else:
            messagebox.showerror("Invalid Username", "Please enter a valid username.")


    def view_functionality(self):
        passcode_attempt = simpledialog.askstring("View Functionality", "Enter the 6-digit passcode:")

        if passcode_attempt == self.user_manager.owner_passcode:
            functionality_window = tk.Toplevel(self.root)
            functionality_window.title("Machine Functionality")

            button_profit = tk.Button(functionality_window, text="Profit", command=self.show_profit)
            button_profit.pack(pady=5)

            self.button_view_resources = tk.Button(functionality_window, text="View Resources", command=self.view_resources)
            self.button_view_resources.pack(pady=5)

            button_create_custom_drink = tk.Button(functionality_window, text="Create Custom Drink",
                                                command=self.create_custom_drink)
            button_create_custom_drink.pack(pady=5)

            button_turn_off = tk.Button(functionality_window, text="Turn Off", command=self.root.destroy)
            button_turn_off.pack(pady=5)
        else:
            messagebox.showerror("Access Denied", "Incorrect passcode. Access denied.")


    def show_payment_frame(self, drink, username):
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Payment")

        label_cost = tk.Label(payment_window, text=f"Cost: {MoneyMachine.CURRENCY}{drink.cost}")
        label_cost.grid(row=0, column=0, columnspan=3, pady=10)

        label_fives = tk.Label(payment_window, text="Five Rupee:")
        label_fives.grid(row=1, column=0, pady=5, padx=10)
        entry_fives = tk.Entry(payment_window, width=5)
        entry_fives.grid(row=1, column=1, pady=5)

        label_tens = tk.Label(payment_window, text="Ten Rupee:")
        label_tens.grid(row=2, column=0, pady=5, padx=10)
        entry_tens = tk.Entry(payment_window, width=5)
        entry_tens.grid(row=2, column=1, pady=5)

        label_twenties = tk.Label(payment_window, text="Twenty Rupee:")
        label_twenties.grid(row=3, column=0, pady=5, padx=10)
        entry_twenties = tk.Entry(payment_window, width=5)
        entry_twenties.grid(row=3, column=1, pady=5)

        button_pay = tk.Button(payment_window, text="Pay", command=lambda: self.make_payment(drink, username, entry_fives.get(), entry_tens.get(), entry_twenties.get(), payment_window))
        button_pay.grid(row=4, column=0, columnspan=2, pady=15)

        self.label_payment_status = tk.Label(payment_window, text="")
        self.label_payment_status.grid(row=5, column=0, columnspan=2, pady=10)


    def make_payment(self, drink, username, fives, tens, twenties, payment_window):
        fives = int(fives) if fives else 0
        tens = int(tens) if tens else 0
        twenties = int(twenties) if twenties else 0

        if self.user_manager.coffee_maker.is_resource_sufficient(drink):
            if self.user_manager.money_machine.make_payment(drink.cost, fives, tens, twenties):
                success_message = f"Payment Successful! Enjoy your {drink.name}, {username}."
                self.label_payment_status.config(text=success_message, fg="green")
            else:
                error_message = "Insufficient funds. Please add money to your account."
                self.label_payment_status.config(text=error_message, fg="red")
        else:
            resource_error = "Sorry, there are not enough resources to make this drink."
            self.label_payment_status.config(text=resource_error, fg="red")

        payment_window.after(2000, payment_window.destroy)
            

    def create_custom_drink(self):
        custom_name = simpledialog.askstring("Create Custom Drink", "Enter the name of the custom drink:")
        custom_water = simpledialog.askinteger("Create Custom Drink", "Enter the water amount (in ml):")
        custom_milk = simpledialog.askinteger("Create Custom Drink", "Enter the milk amount (in ml):")
        custom_coffee = simpledialog.askinteger("Create Custom Drink", "Enter the coffee amount (in g):")
        custom_cost = simpledialog.askfloat("Create Custom Drink", "Enter the cost of the custom drink:")

        if custom_name and custom_water is not None and custom_milk is not None and custom_coffee is not None and custom_cost is not None:
            custom_drink = MenuItem(name=custom_name, water=custom_water, milk=custom_milk, coffee=custom_coffee, cost=custom_cost)
            self.user_manager.menu.add_custom_drink(custom_drink)
            messagebox.showinfo("Custom Drink Created", f"Custom drink '{custom_name}' created successfully.")


    def run(self):
        self.root.mainloop()


    def show_profit(self):
        if not hasattr(self, "window") or not isinstance(self.window, tk.Toplevel):
            self.window = tk.Toplevel(self.root)
            self.profit_label = tk.Label(self.window, text="")
            self.profit_label.pack(pady=10)
            self.window.protocol("WM_DELETE_WINDOW", self.on_profit_window_close)

        profit_report = f"Profit: ₹{self.user_manager.money_machine.fetch_profit_from_db()}"

        if self.profit_label and self.profit_label.winfo_exists():
            self.profit_label.config(text=profit_report)


    def on_profit_window_close(self):
        self.profit_label = None
        self.window.destroy()


    def update_profit_label(self, profit):
        if hasattr(self, "window") and isinstance(self.window, tk.Toplevel):
            if self.profit_label is None:
                self.profit_label = tk.Label(self.window, text="")
                self.profit_label.pack(pady=10)

            if self.profit_label.winfo_exists():
                self.profit_label.config(text=f"Profit: ₹{profit}")


    def update_resources_label(self, resources):
        resources_text = "Resources:\n"
        for item, quantity in resources.items():
            resources_text += f"{item.capitalize()}: {quantity}ml\n"
        self.label_resources.config(text=resources_text)


    def view_resources(self):
        resources_window = tk.Toplevel(self.root)
        resources_window.title("Current Resources")

        current_resources = self.user_manager.coffee_maker.get_current_resources()
        resources_text = "Current Resources\n\n"
        for item, quantity in current_resources.items():
            resources_text += f"{item.capitalize()}: {quantity}ml\n"

        label_resources = tk.Label(resources_window, text=resources_text)
        label_resources.pack(pady=10)
        