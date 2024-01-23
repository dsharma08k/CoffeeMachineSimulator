# CoffeeMachineSimulator
A Coffee Machine Simulator with a Python GUI, utilizing MySQL for data storage.


This guide provides the necessary information to quickly set up the Coffee Machine Simulator. The application relies on a MySQL database with specific tables for resource management, user accounts, drink menu, and profit tracking.


* MySQL Database

1. CREATE DATABASE coffee_machine_db;
2. mysql -u your_username -p coffee_machine_db < database_setup.sql


* Create  necessary tables in MySQL

1.  Create resources table

CREATE TABLE IF NOT EXISTS resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(255) NOT NULL,
    quantity INT NOT NULL
);

2. Create drinks table

CREATE TABLE IF NOT EXISTS drinks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    water INT NOT NULL,
    milk INT NOT NULL,
    coffee INT NOT NULL,
    price FLOAT NOT NULL
);

3. Create users table

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE
);

4.  Create profits table

CREATE TABLE IF NOT EXISTS profits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profit FLOAT NOT NULL
);


* License

This project is licensed under the MIT License. See the LICENSE file for details.