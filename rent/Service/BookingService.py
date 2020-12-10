from rent.Entity import Booking
from rent.Entity import Vehicle
from rent.DAO import VehicleDAO
from rent.DAO import CustomerDAO
from rent.DAO import bookingDAO
from rent.Entity import Booking
from rent.DAO import sqlUtility
from rent.models import ActiveCustomer,ActiveCars,ActiveUsers

# TRANSACTION (Include both booking and reservations) HISTORY
def fetchTransactionHistory():
    bookings = bookingDAO.getTransactions()
    return bookings


# ALL BOOKING HISTORY
def fetchBookings():
    bookings = bookingDAO.getBookingsByStatus("booked")
    bookingData = []
    for booking in bookings:
        customer = CustomerDAO.getCustomerByDLN(booking['driving_license'])
        bookingData.append({**booking, **customer})

    return bookingData


# ALL RESERVATION HISTORY
def fetchReservations():
    bookings = bookingDAO.getBookingsByStatus("reserved")
    bookingData = []
    for booking in bookings:
        customer = CustomerDAO.getCustomerByDLN(booking['driving_license'])
        bookingData.append({**booking, **customer})
    return bookingData


# MODIFY EXISTING BOOKING DATA
def modifyBookingData(request):
    # request.POST.get(sqlUtility.BOOKING_STATUS),
    result = {}
    bookingObj = Booking.BookingObject(request.POST.get(sqlUtility.BOOKING_START_DATE),
                                       request.POST.get(sqlUtility.BOOKING_END_DATE),
                                       request.POST.get(sqlUtility.BOOKING_DRIVING_LICENSE),
                                       request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE),
                                       "booked",
                                       )
    print('bookingObj bookingObj bookingObj bookingObj')
    print(bookingObj.getData())
    oldBookingObj = bookingDAO.getBookingObject(request.POST.get('booking_id'))

    if oldBookingObj[sqlUtility.TIME_STAMP] > bookingObj.time_stamp:
        alert('booking already modified by other clerk')
        result["updated"] = False
        return result
    else:
        if not oldBookingObj[sqlUtility.BOOKING_LICENSE_PLATE] == request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE):
            VehicleDAO.updateStatus('booked', request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE))
            VehicleDAO.updateStatus('available', oldBookingObj[sqlUtility.BOOKING_LICENSE_PLATE])

        result = bookingDAO.updateBooking(bookingObj, request.POST.get(sqlUtility.BOOKING_ID))
        if not result["error"]:
            result["updated"] = True
            return result


# FETCH EXISTING BOOKING BY ID
def fetchBooking(bookingId):
    print("jhachvashjcvasjvchjv")
    booking = bookingDAO.getBookingObject(bookingId)
    print("jhachvashjcvasjvchjv")
    if booking:
        customer = CustomerDAO.getCustomerByDLN(booking['driving_license'])
        bookingData = {**booking, **customer}
        return bookingData
    print("jhachvashjcvasjvchjv")
    return []


# ADD BOOKING OBJECT INTO DB
def addBooking(request):
    booking = Booking.BookingObject(request.POST.get(sqlUtility.BOOKING_START_DATE),
                                    request.POST.get(sqlUtility.BOOKING_END_DATE),
                                    request.POST.get(sqlUtility.BOOKING_DRIVING_LICENSE),
                                    request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE),
                                    'booked')
    booking = bookingDAO.addBooking(booking)
    VehicleDAO.updateStatus('booked', request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE))

    return booking['booking_id']




# DELETE EXISTING BOOKING
def deleteBooking(request, bookingID):
    print('request 321354')
    print(request.GET)
    print(bookingID)
    if bookingID is None or bookingID == '':
        bookingID = request.GET.get(sqlUtility.BOOKING_ID)
    print('request')
    print(request)
    print(bookingID)
    if not (bookingID is None and bookingID == ''):
        booking = bookingDAO.getBookingObject(bookingID)
        ActiveCustomer.objects.filter(custid=booking['driving_license']).delete()

        bookingDAO.deleteBooking(bookingID)
        VehicleDAO.updateStatus('available', str(booking[sqlUtility.BOOKING_LICENSE_PLATE]))
    else:

        VehicleDAO.updateStatus('available', request.GET.get(sqlUtility.BOOKING_LICENSE_PLATE))


# Return Booked vehicle

def returnRental(request, bookingID):
    print('request')
    request.POST = request.GET
    print(request.GET.get(sqlUtility.BOOKING_LICENSE_PLATE))
    allBookings = bookingDAO.getTransactions()
    for booking in allBookings:
        print(booking)
        if booking[sqlUtility.BOOKING_LICENSE_PLATE] == request.GET.get(sqlUtility.BOOKING_LICENSE_PLATE):
            bookingID = booking[sqlUtility.BOOKING_ID]

    print(request.POST)
    print(request.GET)
    deleteBooking(request, str(bookingID))
