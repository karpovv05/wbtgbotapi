import sqlite3



class sqliteCommand:

    def createTable(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE Users (id INTEGER PRIMARY KEY, adToken TEXT);')
        connection.commit()
        connection.close()


    def addPerson(self,tgId,adApi):
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Users VALUES (?, ?);', (tgId, adApi))
            connection.commit()
            connection.close()
            return 'Вы добавлены в базу данных'
        except:
            return 'Вы уже есть в базе данных'


    def showAll(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT adToken FROM Users")
        rows = cursor.fetchall()
        answer = []
        for row in rows:
            answer.append(row)
        connection.close()
        return answer


    def delAll(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Users;')
        connection.commit()
        connection.close()




    def changeApi(self,tgId,adApi):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM Users WHERE id = "{tgId}"')
        connection.commit()
        cursor.execute('INSERT INTO Users VALUES (?, ?);', (tgId, adApi))
        connection.commit()
        connection.close()

    def getApi(self,tgId):
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT adToken FROM Users WHERE id={tgId}")
            row = ''.join(str(x) for x in cursor.fetchone())
            return row
        except Exception as ex:
            return ex
        finally:
            connection.close()

    def check_id(self,tgId):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT id FROM Users WHERE id={tgId}")
        row = cursor.fetchone()
        if row != None:
            return row
        else:
            return False



