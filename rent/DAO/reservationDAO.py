from . import sqlUtility
from rent.DAO import BaseDAO

# Transaction History
def getTransactions():
    baseDao = BaseDAO.DbConnection()
    bookings = baseDao.executeQuery(sqlUtility.BOOKING_DATA_QUERY)
    return bookings

# GET BOOKING OBJECT FROM DB USNIG STATUS
def getReservationsByStatus(status):
    baseDao = BaseDAO.DbConnection()
    bookings = baseDao.getRecords(sqlUtility.BOOKING_DB_NAME, sqlUtility.BOOKING_STATUS, status)
    return bookings

# GET BOOKING OBJECT FROM DB USING BOOKING ID
def getReservationObject(id):
    baseDao = BaseDAO.DbConnection()
    booking = baseDao.getRecord(sqlUtility.BOOKING_DB_NAME, sqlUtility.BOOKING_ID, id)
    return booking


# UPDATE EXISTING BOOKING OBJECT IN DB
def updateReservation(bookingObj,id):
    baseDao = BaseDAO.DbConnection()
    data = bookingObj.getData() + (id,)
    return baseDao.updateRecord(sqlUtility.UPDATE_QUERY_BOOKING_DB, data)



# ADD BOOKING OBJECT TO DB
def addReservation(reservation):
    baseDao = BaseDAO.DbConnection()
    print('ADD BOOKING OBJECT TO DB')
    print(reservation)
    item="book"
    reservation = baseDao.addRecord(sqlUtility.INSERT_QUERY_BOOKING_DB, reservation, sqlUtility.BOOKING_DB_NAME, item)
    print('ADD BOOKING OBJECT TO DB')
    print(reservation)
    return reservation

# DELETE BOOKING OBJECT FROM DB
def deleteReservation(bookingId):
    baseDao = BaseDAO.DbConnection()
    booking = baseDao.deleteRecord(sqlUtility.DELETE_QUERY_BOOKING_DB,bookingId)
    return booking
