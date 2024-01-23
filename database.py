import mysql.connector

class Database:


    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host="your_host",
            user="your_user",
            password="your_password",
            database="your_database_name"
        )
        self.cursor = self.connection.cursor()
        self.create_tables()


    def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS resources (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item VARCHAR(255) NOT NULL,
            quantity INT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.connection.commit()


    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        self.consume_results()
        self.connection.commit()
        return True


    def fetch_one(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)

            result = self.cursor.fetchone()
            return result
        
        except Exception as e:
            return None


    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()


    def consume_results(self):
        try:
            while self.cursor.nextset():
                pass
            while self.cursor.fetchone() is not None:
                pass
        except mysql.connector.errors.InterfaceError:
            pass


    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
