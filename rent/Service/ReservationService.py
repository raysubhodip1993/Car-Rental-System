from rent.Entity import Reservation
from rent.Entity import Vehicle
from rent.DAO import VehicleDAO
from rent.DAO import CustomerDAO
from rent.DAO import bookingDAO, reservationDAO
from rent.Entity import Reservation, Booking
from rent.DAO import sqlUtility


# ALL RESERVATION HISTORY
def fetchReservations():
    bookings = reservationDAO.getReservationsByStatus("reserved")
    bookingData = []
    for booking in bookings:
        customer = CustomerDAO.getCustomerByDLN(booking['driving_license'])
        bookingData.append({**booking, **customer})
    return bookingData


# MODIFY EXISTING BOOKING DATA
def modifyReservationData(request):
    # request.POST.get(sqlUtility.BOOKING_STATUS),
    bookingObj = Reservation.ReservationObject(request.POST.get(sqlUtility.BOOKING_START_DATE),
                                               request.POST.get(sqlUtility.BOOKING_END_DATE),
                                               request.POST.get(sqlUtility.BOOKING_DRIVING_LICENSE),
                                               request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE),
                                               "reserved",
                                               )

    print('bookingObj bookingObj bookingObj bookingObj')
    print(bookingObj.getData())
    oldReservationObj = reservationDAO.getReservationObject(request.POST.get('booking_id'))
    if oldReservationObj[sqlUtility.TIME_STAMP] > bookingObj.time_stamp:
        alert('Reservation already modified by other clerk')
        result["updated"] = False
        return result
    if not oldReservationObj[sqlUtility.BOOKING_LICENSE_PLATE] == request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE):
        VehicleDAO.updateStatus('reserved', request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE))
        VehicleDAO.updateStatus('available', oldReservationObj[sqlUtility.BOOKING_LICENSE_PLATE])

    result = reservationDAO.updateReservation(bookingObj, request.POST.get(sqlUtility.BOOKING_ID))
    if not result["error"]:
        result["updated"] = True
        return result


# FETCH EXISTING RESERVATION BY ID
def fetchReservation(bookingId):
    booking = reservationDAO.getReservationObject(bookingId)
    if booking:
        customer = CustomerDAO.getCustomerByDLN(booking['driving_license'])
        bookingData = {**booking, **customer}
        return bookingData
    else:
        return []


# ADD RESERVATION OBJECT INTO DB
def addReservation(request):
    booking = Reservation.ReservationObject(request.POST.get(sqlUtility.BOOKING_START_DATE),
                                            request.POST.get(sqlUtility.BOOKING_END_DATE),
                                            request.POST.get(sqlUtility.BOOKING_DRIVING_LICENSE),
                                            request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE),
                                            'reserved')
    booking = reservationDAO.addReservation(booking)
    VehicleDAO.updateStatus('reserved', request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE))
    return booking['booking_id']


# def completeReservation(request):
#     booking = Reservation.ReservationObject(request.POST.get(sqlUtility.BOOKING_START_DATE),
#                                     request.POST.get(sqlUtility.BOOKING_END_DATE),
#                                     request.POST.get(sqlUtility.BOOKING_DRIVING_LICENSE), request.POST.get(
#             sqlUtility.BOOKING_LICENSE_PLATE),'booked')
#     booking =  bookingDAO.deleteReservation(request.POST.get('booking_id'))
#     VehicleDAO.updateStatus('available', request.POST.get(sqlUtility.BOOKING_LICENSE_PLATE))
#     #return booking['booking_id']


# DELETE EXISTING BOOKING
def cancelReservation(request, bookingID):
    print('request 321354')
    print(request.GET)
    print(bookingID)
    if bookingID is None or bookingID == '':
        bookingID = request.GET.get(sqlUtility.BOOKING_ID)
    print('request')
    print(request)
    print(bookingID)
    if not (bookingID is None or bookingID == ''):
        reservation = reservationDAO.getReservationObject(bookingID)
        reservationObj = Reservation.ReservationObject(reservation[sqlUtility.BOOKING_START_DATE],
                                                       reservation[sqlUtility.BOOKING_END_DATE],
                                                       reservation[sqlUtility.BOOKING_DRIVING_LICENSE],
                                                       reservation[sqlUtility.BOOKING_LICENSE_PLATE],
                                                       'cancelled')
        print('reservation object')
        print(reservationObj.getData())
        reservationDAO.updateReservation(reservationObj, bookingID)
        VehicleDAO.updateStatus('available', reservation[sqlUtility.BOOKING_LICENSE_PLATE])
    else:

        VehicleDAO.updateStatus('available', request.GET.get(sqlUtility.BOOKING_LICENSE_PLATE))

        # Return Booked vehicle


def returnRental(request, bookingID):
    print('request')
    request.POST = request.GET
    print(request.GET.get(sqlUtility.BOOKING_LICENSE_PLATE))
    allReservations = reservationDAO.getTransactions()
    for booking in allReservations:
        print(booking)
        if booking[sqlUtility.BOOKING_LICENSE_PLATE] == request.GET.get(sqlUtility.BOOKING_LICENSE_PLATE):
            bookingID = booking[sqlUtility.BOOKING_ID]

    print(request.POST)
    print(request.GET)
    deleteReservation(request, str(bookingID))


def modifyToBooking(request):
    booking = fetchReservation(request.GET.get(sqlUtility.BOOKING_ID))
    bookingObj = Booking.BookingObject(booking[sqlUtility.BOOKING_START_DATE],
                                       booking[sqlUtility.BOOKING_END_DATE],
                                       booking[sqlUtility.BOOKING_DRIVING_LICENSE],
                                       booking[sqlUtility.BOOKING_LICENSE_PLATE],
                                       'booked'
                                       )
    bookingDAO.updateBooking(bookingObj, request.GET.get(sqlUtility.BOOKING_ID))
    return bookingDAO.getBookingObject(request.GET.get(sqlUtility.BOOKING_ID))
