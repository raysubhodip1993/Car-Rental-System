import sqlite3
from rent.DAO import sqlUtility, TestDAO
import json
from collections import namedtuple
import queue
import os
from threading import Thread
class BaseDAO:

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
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            print('BASE_DIR')
            print(BASE_DIR)
            db_path = os.path.join(BASE_DIR, "sqlDB")
            print('db_path')
            print(db_path)
            self.conn = sqlite3.connect(db_path)
            self.curr = self.conn.cursor()
            return self.curr

        except Exception as dbException:
            print("Error during conection: ", str(dbException))

    def getAllRecords(self, dbName):
        results = self.executeQuery("SELECT * FROM " + str(dbName))
        self.conn.close()
        print("DataBase Connection Closed Successfully")
        return results

    def getRecord(self, dbName, filterName, filterValue):
        result = self.executeQuery("SELECT * FROM " + dbName + " WHERE " + filterName + " = '" + filterValue + "'")
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
        self.conn.close()
        print("DataBase zConnection Closed Successfully")
        print('result')
        return results

    def addRecord(self, sqlQuery, object, dbName):
        print('Add record Query')
        print(sqlQuery + str(object.getData()))
        self.curr.execute(sqlQuery, object.getData())

        self.conn.commit()
        obj = self.getLastInsertedRecord(self.curr.lastrowid, dbName)
        print("DataBase Connection Closed Successfully")
        return obj

    def updateRecord(self, sqlQuery, data):
        print('Update Record Query')

        print(sqlQuery + str(data))
        self.curr.execute(sqlQuery, data)
        self.conn.commit()
        self.conn.close()
        print("DataBase Connection Closed Successfully")

    def getLastInsertedRecord(self, id, dbName):
        result = self.executeQuery("SELECT * FROM " + dbName + " WHERE booking_id = " + str(id))
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

    def clearDb(dbName):
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