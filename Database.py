import sqlite3
import io


class Database:
    # Инициализация
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    # Создание БД
    def create_db(self, nameDb, scriptDbName):
        try:
            conn = sqlite3.connect(nameDb, check_same_thread=False)
            conn.row_factory = sqlite3.Row

            with io.open(scriptDbName, encoding='utf-8') as file:
                self.__db.cursor().executescript(file.read())
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка создания БД " + str(e))
            return False

        return True

    # Добавление нового предмета в БД
    def add_item(self, name):
        try:
            self.__cur.execute("INSERT INTO items VALUES(NULL, ?, ?)", (name, 0))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка добавления элемента " + str(e))
            return False

        return True

    def get_items(self):
        try:
            with sqlite3.connect("main.db", check_same_thread=False) as con:
                cur = con.cursor()

                cur.execute(f"SELECT * FROM items")
                con.commit()

                res = cur.fetchall()

                if not res:
                    print("Данные не найдены в таблице")
                    return False

                return res

        except sqlite3.Error as e:
            print("Ошибка получения элементов " + str(e))
            return False

    ######################################################################

    # Добавление нового предмета в БД
    def add_item_schedule(self, relativeItemId, status, startH, startM, endH, endM):
        try:
            self.__cur.execute("INSERT INTO schedule VALUES(NULL, ?, ?, ?, ?, ?, ?)",
                               (relativeItemId, status, startH, startM, endH, endM))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка добавления элемента " + str(e))
            return False

        return True

    def get_schedule(self):
        try:
            with sqlite3.connect("main.db", check_same_thread=False) as con:
                cur = con.cursor()

                cur.execute(f"SELECT * FROM schedule")
                con.commit()

                res = cur.fetchall()

                if not res:
                    print("Данные не найдены в таблице")
                    return False

                return res

        except sqlite3.Error as e:
            print("Ошибка получения элементов " + str(e))
            return False

    def insert_state_by_id(self, item_id, state):
        try:
            with sqlite3.connect("main.db", check_same_thread=False) as con:
                cur = con.cursor()

                cur.execute(f"UPDATE items SET isBuyed = {state} WHERE id = {item_id}")
                con.commit()

        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
            return False

        return True