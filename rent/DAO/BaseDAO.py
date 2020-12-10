import sqlite3
from rent.DAO import sqlUtility
import json
from collections import namedtuple
import os
#import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   passwd="yourpassword"
# )

class DbConnection:

    def __init__(self):
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            print('BASE_DIR')
            print(BASE_DIR)
            db_path = os.path.join(BASE_DIR, "sqlDB")
            print('db_path')
            print(db_path)
            self.conn = sqlite3.connect(db_path)
            self.curr = self.conn.cursor()
        except Exception as dbException:
            print("Error during conection: ", str(dbException))

    def createConnection(self):
        try:
            return self.curr

        except Exception as dbException:
            print("Error during conection: ", str(dbException))

    def getAllRecords(self, dbName):
        results = self.executeQuery("SELECT * FROM " + str(dbName))
        self.conn.commit()
        self.conn.close()
        print("DataBase Connection Closed Successfully")
        return results

    def getRecord(self, dbName, filterName, filterValue):
        result = self.executeQuery("SELECT * FROM " + dbName + " WHERE " + filterName + " = '" + filterValue + "'")
        self.conn.commit()
        self.conn.close()
        print("DataBase zConnection Closed Successfully")
        print('result')
        print(result)
        if result:
            return result[0]
        else:
            return {}

    def getRecords(self, dbName, filterName, filterValue):
        results = self.executeQuery("SELECT * FROM " + dbName + " WHERE " + filterName + " = '" + filterValue + "'")
        self.conn.commit()
        self.conn.close()
        print("DataBase zConnection Closed Successfully")
        print('result')
        return results

    def addRecord(self, sqlQuery, object, dbName, item):
        print('Add record Query')
        print(item)
        print(sqlQuery + str(object.getData()))
        self.curr.execute(sqlQuery, object.getData())
        self.conn.commit()
        self.conn.commit()
        if(item=="cust"):
            obj = self.getLastInsertedRecord(self.curr.lastrowid, dbName, item)
        else:
            obj = self.getLastInsertedRecord(self.curr.lastrowid, dbName, item)

        print("DataBase Connection Closed Successfully")
        return obj

    def updateRecord(self, sqlQuery, data):
        print('Update Record Query')
        result = {}
        result["error"] = None
        try:
            print(sqlQuery + str(data))
            self.curr.execute(sqlQuery, data)
            self.conn.commit()
            # self.conn.close()
        except Exception as error:
            print("DB Error "+ str(error))
            result["Error"] = str(error)

        finally:
            self.conn.close()
        return result

    def getLastInsertedRecord(self,id,dbName, item):
        if(item=="car"):
            i="carID"
            result = self.executeQuery("SELECT * FROM " + dbName + " WHERE " + i + " = " + str(id))
        if (item == "emp"):
            i = "_ROWID_"
            result = self.executeQuery("SELECT * FROM " + dbName + " WHERE " + i + " = " + str(id))
        if (item == "cust"):
            i = "_ROWID_"
            result = self.executeQuery("SELECT * FROM " + dbName + " WHERE " + i + " = " + str(id))
        if (item == "book"):
            i = "booking_id"
            result = self.executeQuery("SELECT * FROM " + dbName + " WHERE " + i + " = " + str(id))

        self.conn.commit()
        self.conn.close()
        print("DataBase zConnection Closed Successfully")
        print('result')
        return result[0]

    def deleteRecord(self, sqlQuery, data):
        print('delete query')
        print(sqlQuery)
        filterValue = ()
        filterValue = filterValue + (data,)
        self.curr.execute(sqlQuery, filterValue)
        self.conn.commit()
        self.conn.close()
        print("DataBase Connection Closed Successfully")

    def clearDb(self,dbName):
        results = self.curr.execute("DELETE FROM " + dbName)
        print(results)
        for row in results:
            print(row)
        self.curr.commit()
        self.conn.close()
        print("DataBase Connection Closed Successfully")
        return results

    def closeConnection(self):
        self.conn.close()

    def executeQuery(self, query):
        dbCursor = self.curr
        print('query')
        print(query)
        return [dict((dbCursor.description[i][0], value) for i, value in enumerate(row)) for row in
                dbCursor.execute(query)]

    def getAtt(self):
        return self.conn + " " + self.curr



    # results = conn.execute("SELECT * FROM " + 'rent_cardb' + " WHERE " + 'license_plate' + " =  '123 456'")
    #
    # r = [dict((cur.description[i][0], value) \
    #           for i, value in enumerate(row)) for row in
    #      cur.execute("SELECT * FROM " + 'rent_cardb' + " WHERE " + 'license_plate' + " =  '123 456'")]
    #
    # print(str(r[0]))
    # x = json.loads(json.dumps(r[0]), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    #
    # print(x.type)
    # for row in results:
    #     print(row)
    # conn.close()
    # result = cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
# BaseDAO.createConnection()
