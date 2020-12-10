from rent.Controller.AppController import *
from rent.Service import ReservationService, ReservationService
from rent.models import *
import random
from rent.Entity import Booking, Reservation
from rent.DAO import sqlUtility


# VIEW RESERVATIONS
def view_reservations(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        activeCars = ActiveCars.objects.filter(uname=request.session['userid'])
        for activeCar in activeCars:
            activeCar.delete()
        activeCustomers = ActiveCustomer.objects.filter(uname=request.session['userid'])
        for activeCust in activeCustomers:
            activeCust.delete()
        activeBookings = ActiveBookings.objects.filter(uname=request.session['userid'])
        for activeBooking in activeBookings:
            activeBooking.delete()
        bookings = ReservationService.fetchReservations()
        ActiveCars.objects.filter(uname=request.session['userid']).delete()
        ActiveCustomer.objects.filter(uname=request.session['userid']).delete()
        template = loader.get_template('clerk/view-reservations.html')
        return HttpResponse(template.render({'bookings': bookings}, request))


# LOAD CREATE BOOKING PAGE WITH AVAILABLE CARS
def create_reservation(request):
    print("test teste jsfjkbsdjkvbkb")
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))

    try:
        ActiveCars.objects.filter(uname=request.session['userid']).delete()
        ActiveCustomer.objects.filter(uname=request.session['userid']).delete()
        availableCars = VehicleService.getAvailableCars()
        print(availableCars)
    except:
        template = loader.get_template('clerk/create-reservation.html')
        return HttpResponse(template.render({'cars': availableCars}, request))

    template = loader.get_template('clerk/create-reservation.html')
    return HttpResponse(template.render({'cars': availableCars}, request))


# SHOW RESERVATION DETAILS
def view_reservation_details(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        # booking = Bookings.fetchReservation(request.GET.get("booking_id"))
        print('request.GET.get("sqlUtility.BOOKING_ID")')
        print(request.GET)
        booking = ReservationService.fetchReservation(request.GET.get(sqlUtility.BOOKING_ID))
        print('BOOKING DATA')
        print(booking)
        template = loader.get_template('clerk/view-reservation-details.html')
        return HttpResponse(template.render({'booking': booking}, request))


# BOOKING COMPLETE AFTER VEHICLE RETURNED
def cancel_reservation(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))

    if (ActiveBookings.objects.filter(bookingId=request.GET[sqlUtility.BOOKING_ID]).count() >= 1):
        alert("Reservation Screen is active in the system")
        return view_reservation_details(request)

    if request.method == 'GET':
        # booking = Bookings.fetchReservation(request.GET.get("booking_id"))
        print('request.GET.get("id")')
        print(request.GET)

        ReservationService.cancelReservation(request, '')

        bookings = ReservationService.fetchReservations()

        template = loader.get_template('clerk/view-reservations.html')
        return HttpResponse(template.render({'bookings': bookings}, request))


# LOAD EXISTING BOOKING TO MODIFY
def modify_reservation(request):
    if (ActiveBookings.objects.filter(bookingId=request.GET[sqlUtility.BOOKING_ID]).count() >= 1):
        if (ActiveBookings.objects.filter(bookingId=request.GET[sqlUtility.BOOKING_ID],
                                          uname=request.session['userid']).count() >= 1):
            activeBooking = ActiveBookings.objects.get(bookingId=request.GET[sqlUtility.BOOKING_ID],
                                                       uname=request.session['userid'])
            if int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:

                activeBooking.delete()
                return view_reservation_details(request)
            else:
                activeBooking.lockDuration = 60
                activeBooking.save()
                availableCars = VehicleService.getAvailableCars()
                booking = ReservationService.fetchReservation(request.GET.get(sqlUtility.BOOKING_ID))
                data = {}
                data['booking'] = booking
                data['cars'] = availableCars
                template = loader.get_template('clerk/modify-reservation.html')
                return HttpResponse(template.render({'data': data}, request))
        else:
            activeBooking = ActiveBookings.objects.get(bookingId=request.GET[sqlUtility.BOOKING_ID])
            if int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:
                availableCars = VehicleService.getAvailableCars()
                booking = BookingService.fetchBooking(request.GET.get(sqlUtility.BOOKING_ID))
                if booking:
                    activeBooking = ActiveBookings(bookingId=request.GET.get(sqlUtility.BOOKING_ID),
                                                   uname=request.session['userid'],
                                                   locktime=int(time.time()), lockDuration=60)
                    activeBooking.save()

                    data = {}
                    data['booking'] = booking
                    data['cars'] = availableCars
                    template = loader.get_template('clerk/modify-reservation.html')
                    return HttpResponse(template.render({'data': data}, request))
            else:
                alert("Reservation is active in the system")
                return view_reservation_details(request)

    else:

        availableCars = VehicleService.getAvailableCars()
        booking = BookingService.fetchBooking(request.GET.get(sqlUtility.BOOKING_ID))
        if booking:
            activeBooking = ActiveBookings(bookingId=request.GET.get(sqlUtility.BOOKING_ID),
                                           uname=request.session['userid'],
                                           locktime=int(time.time()), lockDuration=60)
            activeBooking.save()

            data = {}
            data['booking'] = booking
            data['cars'] = availableCars
            template = loader.get_template('clerk/modify-booking.html')
            return HttpResponse(template.render({'data': data}, request))
        else:
            alert("Reservation is not avilable in the system")
            bookings = BookingService.fetchBookings()
            ActiveCars.objects.filter(uname=request.session['userid']).delete()
            ActiveCustomer.objects.filter(uname=request.session['userid']).delete()
            print('bookings ')
            print(bookings)
            template = loader.get_template('clerk/view-reservations.html')
            return HttpResponse(template.render({'bookings': bookings}, request))


# LOAD EXISTING BOOKING TO MODIFY
def update_to_booking(request):
    print("testb bbbbbbbbbbbbb")

    if request.GET.get('booking_id'):
        print("testb 1")
        if (ActiveBookings.objects.filter(bookingId=request.GET[sqlUtility.BOOKING_ID]).count() >= 1):
            print("testb 2")
            if (ActiveBookings.objects.filter(bookingId=request.GET[sqlUtility.BOOKING_ID],
                                              uname=request.session['userid']).count() >= 1):
                activeBooking = ActiveBookings.objects.get(bookingId=request.GET[sqlUtility.BOOKING_ID],
                                                           uname=request.session['userid'])
                print("testb 3")
                if not int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:
                    print("testb 4")
                    alert("Booking Screen is active in the system")
                    return view_reservation_details(request)
            else:
                print("testb 5")
                activeBooking = ActiveBookings.objects.get(bookingId=request.GET[sqlUtility.BOOKING_ID])
                if int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:

                    activeBooking.delete()
                    print("testb 6")
                    booking = ReservationService.modifyToBooking(request)
                    template = loader.get_template('clerk/view-booking-details.html')
                    return HttpResponse(template.render({'booking': booking}, request))
                else:
                    alert("Reservation is active in the system")
                    return view_reservation_details(request)


        else:
            print("testb 7")
            booking = ReservationService.modifyToBooking(request)
            template = loader.get_template('clerk/view-booking-details.html')
            return HttpResponse(template.render({'booking': booking}, request))

    else:
        alert("Reservation is active in the system")
        return view_reservation_details(request)


########################################################################################################################
# HANDLE DATA
########################################################################################################################

# CREATE BOOKING
def createReservation(request):
    print('create booking')
    print(request.POST)
    if request.POST.get('first_name') and request.POST.get(
            'last_name') and request.POST.get('driving_license') and request.POST.get(
        'start_date') and request.POST.get('license_plate') and request.POST.get('end_date'):

        bookingId = ReservationService.addReservation(request)
        return redirect('/view-reservation-details/?booking_id=' + str(bookingId))
    else:
        alert(text='Customer Creation Failed!', title='Failure', button='OK')
        template = loader.get_template('create-booking.html')
        return HttpResponse(template.render({}, request))


# MODIFY EXISTING BOOKING DATA
def modifyReservation(request):
    print('MODIFY MODIFY MODIFY')
    print(request.POST)
    if request.method == 'POST':
        result = ReservationService.modifyReservationData(request)
        if not result["updated"]:
            request.method = 'GET'
            return view_reservations(request)
        booking = ReservationService.fetchReservation(request.POST.get(sqlUtility.BOOKING_ID))
        template = loader.get_template('clerk/view-reservation-details.html')
        return HttpResponse(template.render({'booking': booking}, request))
    else:
        print('test')


# DELETE EXISTING BOOKING
def deleteReservation(request):
    if request.POST.get('booking_id'):
        if (ActiveBookings.objects.filter(bookingId=request.POST[sqlUtility.BOOKING_ID]).count() >= 1):
            if (ActiveBookings.objects.filter(bookingId=request.POST[sqlUtility.BOOKING_ID],
                                              uname=request.session['userid']).count() >= 1):
                activeBooking = ActiveBookings.objects.get(bookingId=request.POST[sqlUtility.BOOKING_ID],
                                                           uname=request.session['userid'])
                if not int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:
                    alert("Booking Screen is active in the system")
                    return view_reservation_details(request)
            else:
                activeBooking = ActiveBookings.objects.get(bookingId=request.POST[sqlUtility.BOOKING_ID])
                activeBooking.delete()
                if int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:
                    ReservationService.deleteReservation(request, request.POST.get(sqlUtility.BOOKING_ID))
                    alert(text='Reservation Delete Success!', title='Success', button='OK')
                    return redirect('/view-reservation/')

        else:
            activeBooking = ActiveBookings.objects.get(bookingId=request.GET[sqlUtility.BOOKING_ID])
            if int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:
                ReservationService.deleteReservation(request, request.POST.get(sqlUtility.BOOKING_ID))
                alert(text='Reservation Delete Success!', title='Success', button='OK')
                return redirect('/view-reservation/')
            else:
                alert("Reservation is active in the system")
                return view_reservation_details(request)

    else:
        alert(text='Reservation Delete Failed!', title='Failure', button='OK')
        return redirect('/view-reservation-details/?id=' + request.POST.get('booking_id'))
