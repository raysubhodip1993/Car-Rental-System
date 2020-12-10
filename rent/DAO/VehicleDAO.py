from . import BaseDAO
from . import sqlUtility
from rent.Entity import Vehicle
from rent.DAO import BaseDAO
from rent.DAO import sqlUtility
from rent import Utility
from rent.models import  ActiveCars


def getAllCars():
    baseDao = BaseDAO.DbConnection()
    carObjs = baseDao.getAllRecords(sqlUtility.VEHICLE_DB_NAME)
    return carObjs


def updateStatus(status, licensePlate):
    baseDao = BaseDAO.DbConnection()
    carObj = baseDao.getRecord(sqlUtility.VEHICLE_DB_NAME, sqlUtility.VEHICLE_LICENSE_PLATE, str(licensePlate))
    if status == "booked" or status == "reserved":
        print('booked')
        BOOKED = 1
    else:
        print('Not Booked')
        BOOKED = 0
    car = Vehicle.car(carObj['type'], carObj['prod_year'], BOOKED, carObj['license_plate'], carObj['brand'],
                      carObj['model'], carObj['color'])

    # car = Vehicle.car(carObj['type'], carObj['prod_year'], carObj['booked'], carObj['license_plate'], carObj['brand'],
    #                   carObj['model'], carObj['color'])
    baseDao = BaseDAO.DbConnection()
    data = car.getData() + (car.license_plate,)
    baseDao.updateRecord(sqlUtility.UPDATE_QUERY_CAR_DB,data)


def getCar(licensePlate):
    baseDao = BaseDAO.DbConnection()
    car = baseDao.getRecord(sqlUtility.VEHICLE_DB_NAME, sqlUtility.VEHICLE_LICENSE_PLATE, licensePlate)
    return car

# GET CARS AVAILABLE FOR BOOKING
def getAvailableCar():
    baseDao = BaseDAO.DbConnection()
    availableCars = []
    cars = baseDao.executeQuery(sqlUtility.AVAILABLE_CARS_QUERY)
    activeCars = ActiveCars.objects.all()
    if(activeCars):
        for activeCar in activeCars:
            for car in cars:
                print('car')
                print(car)
                print('activeCar')
                print(activeCar)
                print('condition')
                print(car[sqlUtility.VEHICLE_LICENSE_PLATE] != activeCar.carid)
                if car[sqlUtility.VEHICLE_LICENSE_PLATE] != activeCar.carid:
                    if car not in availableCars:
                        availableCars.append(car)
                print('availble cars')
                print(availableCars)
    else:
        availableCars = cars
    return availableCars


def addCar(car):
    baseDao = BaseDAO.DbConnection()
    item="car"
    car = baseDao.addRecord(sqlUtility.INSERT_QUERY_CAR_DB, car,sqlUtility.VEHICLE_DB_NAME,item)
    return car


def modifyCar(car):
    baseDao = BaseDAO.DbConnection()
    data = car.getData() + (car.license_plate,)
    car = baseDao.updateRecord(sqlUtility.UPDATE_QUERY_CAR_DB, data)
    return car


def deleteCar(licensePlate):
    baseDao = BaseDAO.DbConnection()

    car = baseDao.deleteRecord(sqlUtility.DELETE_QUERY_CAR_DB, licensePlate)
    # return car


def executeQuery(dbCursor, query):
    return [dict((dbCursor.description[i][0], value) for i, value in enumerate(row)) for row in dbCursor.execute(query)]
