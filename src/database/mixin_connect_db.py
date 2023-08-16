import os
import sys
sys.path.append(os.getcwd())
# from config import CONNECT_DB
from config import CONN_DB


class MixinConnectDB:
    """
    Миксин класс предоставляет методы для подключения и отключения базы данных PostgreSQL.
    """

    def connect_db(self) -> None:
        """
        Метод позволяет подключаться к базе данных PostgreSQL.
        """
        try:
            self.connected = CONN_DB
            print("database connected.")
        except Exception as ex:
            print("Error connecting to the database:", ex)

    def disable_db(self) -> None:
        """
        Метод позволяет отключаться от базы данных PostgreSQL.
        """
        if self.connected:
            self.connected.close()
            print("Database is disabled.")

