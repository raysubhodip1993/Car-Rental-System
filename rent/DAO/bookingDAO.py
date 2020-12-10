from . import sqlUtility
from rent.DAO import BaseDAO

# Transaction History
def getTransactions():
    baseDao = BaseDAO.DbConnection()
    bookings = baseDao.executeQuery(sqlUtility.BOOKING_DATA_QUERY)
    return bookings

# GET BOOKING OBJECT FROM DB USNIG STATUS
def getBookingsByStatus(status):
    baseDao = BaseDAO.DbConnection()
    bookings = baseDao.getRecords(sqlUtility.BOOKING_DB_NAME, sqlUtility.BOOKING_STATUS, status)
    return bookings

# GET BOOKING OBJECT FROM DB USING BOOKING ID
def getBookingObject(bookingId):
    baseDao = BaseDAO.DbConnection()
    booking = baseDao.getRecord(sqlUtility.BOOKING_DB_NAME, sqlUtility.BOOKING_ID, bookingId)
    return booking


# UPDATE EXISTING BOOKING OBJECT IN DB
def updateBooking(bookingObj,id):
    baseDao = BaseDAO.DbConnection()
    data = bookingObj.getData() + (id,)
    print(data)
    return baseDao.updateRecord(sqlUtility.UPDATE_QUERY_BOOKING_DB, data)



# ADD BOOKING OBJECT TO DB
def addBooking(booking):
    baseDao = BaseDAO.DbConnection()
    print('ADD BOOKING OBJECT TO DB')
    print(booking)
    item="book"
    booking = baseDao.addRecord(sqlUtility.INSERT_QUERY_BOOKING_DB,booking,sqlUtility.BOOKING_DB_NAME,item)
    print('ADD BOOKING OBJECT TO DB')
    print(booking)
    return booking

# DELETE BOOKING OBJECT FROM DB
def deleteBooking(bookingId):
    baseDao = BaseDAO.DbConnection()
    booking = baseDao.deleteRecord(sqlUtility.DELETE_QUERY_BOOKING_DB,bookingId)
    return booking
