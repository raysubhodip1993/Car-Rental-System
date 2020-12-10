from rent.Controller.AppController import *
from rent.Controller.VehicleController import lockVehicle
from rent.Service import BookingService
from rent.models import *
import random
from rent.Service import BookingService
from rent.DAO import sqlUtility


def validate(request):
    print("Hello")
    try:
        availableCars = VehicleService.getAvailableCars()
        print(availableCars)
    except:
        template = loader.get_template('clerk/create-booking.html')
        return HttpResponse(template.render({'cars': availableCars}, request))
    template = loader.get_template('clerk/create-booking.html')
    return HttpResponse(template.render({'cars': availableCars}, request))


# VIEW BOOKINGS
def view_bookings(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        bookings = BookingService.fetchBookings()
        activeCars = ActiveCars.objects.filter(uname=request.session['userid'])
        for activeCar in activeCars:
            activeCar.delete()
        activeCustomers = ActiveCustomer.objects.filter(uname=request.session['userid'])
        for activeCust in activeCustomers:
            activeCust.delete()
        activeBookings = ActiveBookings.objects.filter(uname=request.session['userid'])
        for activeBooking in activeBookings:
            activeBooking.delete()
        print('bookings ')
        print(bookings)
        template = loader.get_template('clerk/view-bookings.html')
        return HttpResponse(template.render({'bookings': bookings}, request))


# VIEW TRANSACTIONS
def view_transactions(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        bookings = BookingService.fetchTransactionHistory()
        activeCars = ActiveCars.objects.filter(uname=request.session['userid'])
        for activeCar in activeCars:
            activeCar.delete()
        activeCustomers = ActiveCustomer.objects.filter(uname=request.session['userid'])
        for activeCust in activeCustomers:
            activeCust.delete()
        template = loader.get_template('admin/view-transactions.html')
        return HttpResponse(template.render({'bookings': bookings}, request))


# LOAD CREATE BOOKING PAGE WITH AVAILABLE CARS
def create_booking(request):
    print("test teste jsfjkbsdjkvbkb")
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))

    try:
        activeCars = ActiveCars.objects.filter(uname=request.session['userid'])
        for car in activeCars:
            car.delete()
        activeCustomers = ActiveCustomer.objects.filter(uname=request.session['userid'])
        for cust in activeCustomers:
            cust.delete()
        availableCars = VehicleService.getAvailableCars()
        print('avaialble cars')
        if not availableCars:
            alert('no cars available for booking')
            return view_bookings(request)
        print(availableCars)
    except:
        template = loader.get_template('clerk/create-booking.html')
        return HttpResponse(template.render({'cars': availableCars}, request))

    template = loader.get_template('clerk/create-booking.html')
    return HttpResponse(template.render({'cars': availableCars}, request))


# SHOW BOOKING DETAILS
def view_booking_details(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        # booking = Bookings.fetchBooking(request.GET.get("booking_id"))
        print('request.GET.get("id")')
        print(request.GET.get("id"))
        if request.GET.get("id"):
            booking = BookingService.fetchBooking(request.GET.get("id"))
        else:
            booking = BookingService.fetchBooking(request.GET.get(sqlUtility.BOOKING_ID))
    if request.method == 'POST':
        if request.POST.get("booking_id"):
            booking = BookingService.fetchBooking(request.POST.get("booking_id"))
        else:
            bookings = BookingService.fetchBookings()
            booking = {}
            for bookingObj in bookings:
                if (bookingObj[sqlUtility.BOOKING_LICENSE_PLATE] == request.GET[sqlUtility.BOOKING_LICENSE_PLATE]):
                    booking = bookingObj
    print('BOOKING DATA')
    print(booking)
    template = loader.get_template('clerk/view-booking-details.html')
    return HttpResponse(template.render({'booking': booking}, request))


# BOOKING COMPLETE AFTER VEHICLE RETURNED
def complete_booking(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    print(request.GET)
    booking = {}

    if sqlUtility.BOOKING_LICENSE_PLATE in request.GET:
        bookings = BookingService.fetchBookings()
        print("bookings")
        print(bookings)
        for bookingObj in bookings:
            if bookingObj[sqlUtility.BOOKING_LICENSE_PLATE] == request.GET[sqlUtility.BOOKING_LICENSE_PLATE]:
                booking = bookingObj
    elif sqlUtility.BOOKING_ID in request.GET:
        booking = BookingService.fetchBooking(request.GET.get(sqlUtility.BOOKING_ID))

    if booking:
        if (ActiveBookings.objects.filter(bookingId=booking[sqlUtility.BOOKING_ID]).count() >= 1):
            if not (ActiveBookings.objects.filter(bookingId=booking[sqlUtility.BOOKING_ID],
                                                  uname=request.session['userid']).count() >= 1):

                activeBooking = ActiveBookings.objects.get(bookingId=booking[sqlUtility.BOOKING_ID])
                if int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:
                    activeBooking.delete()
                else:
                    alert("Booking Screen is active in the system")
                    return view_booking_details(request)

    else:
        alert("No Booking in the system with this ID")
        return view_bookings(request)

    if request.method == 'GET':
        BookingService.returnRental(request, '')

        bookings = BookingService.fetchBookings()

        template = loader.get_template('clerk/view-bookings.html')
        return HttpResponse(template.render({'bookings': bookings}, request))


# LOAD EXISTING BOOKING TO MODIFY
def modify_booking(request):
    if (ActiveBookings.objects.filter(bookingId=request.GET[sqlUtility.BOOKING_ID]).count() >= 1):
        if (ActiveBookings.objects.filter(bookingId=request.GET[sqlUtility.BOOKING_ID],
                                          uname=request.session['userid']).count() >= 1):
            activeBooking = ActiveBookings.objects.get(bookingId=request.GET[sqlUtility.BOOKING_ID],
                                                       uname=request.session['userid'])
            # if int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:
            #     alert("Session Expired")
            #     activeBooking.delete()
            #     return view_booking_details(request)
            # else:
            activeBooking.lockDuration = 60
            activeBooking.save()
            availableCars = VehicleService.getAvailableCars()
            booking = BookingService.fetchBooking(request.GET.get(sqlUtility.BOOKING_ID))
            data = {}
            data['booking'] = booking
            data['cars'] = availableCars
            template = loader.get_template('clerk/modify-booking.html')
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
                    template = loader.get_template('clerk/modify-booking.html')
                    return HttpResponse(template.render({'data': data}, request))
            else:
                alert("Booking is active in the system")
                return view_booking_details(request)

    else:
        print(request.GET)
        print("bnnnnnnnnnnnnnnnnnnnnnnb")
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
            alert("Booking is not avilable in the system")
            bookings = BookingService.fetchBookings()
            ActiveCars.objects.filter(uname=request.session['userid']).delete()
            ActiveCustomer.objects.filter(uname=request.session['userid']).delete()
            print('bookings ')
            print(bookings)
            template = loader.get_template('clerk/view-bookings.html')
            return HttpResponse(template.render({'bookings': bookings}, request))


########################################################################################################################
# HANDLE DATA
########################################################################################################################

# CREATE BOOKING
def createBooking(request):
    print('create booking')
    print(request.POST)
    if request.POST.get('first_name') and request.POST.get(
            'last_name') and request.POST.get('driving_license') and request.POST.get(
        'start_date') and request.POST.get('license_plate') and request.POST.get('end_date'):

        bookingId = BookingService.addBooking(request)
        # p = ActiveCars(carid=request.POST.get('license_plate'))
        # p.save()

        return redirect('/view-booking-details/?id=' + str(bookingId))
    else:
        alert(text='Car Booking Failed!', title='Failure', button='OK')
        template = loader.get_template('create-booking.html')
        return HttpResponse(template.render({}, request))


# MODIFY EXISTING BOOKING DATA
def modifyBooking(request):
    print('MODIFY MODIFY MODIFY')
    print(request.POST)
    if request.method == 'POST':
        result = BookingService.modifyBookingData(request)
        if not result["updated"]:
            request.method = 'GET'
            return view_bookings(request)
        booking = BookingService.fetchBooking(request.POST.get(sqlUtility.BOOKING_ID))
        template = loader.get_template('clerk/view-booking-details.html')
        return HttpResponse(template.render({'booking': booking}, request))
    else:
        print('test')


# DELETE EXISTING BOOKING
def deleteBooking(request):
    if request.POST.get('booking_id'):
        if (ActiveBookings.objects.filter(bookingId=request.POST[sqlUtility.BOOKING_ID]).count() >= 1):
            if (ActiveBookings.objects.filter(bookingId=request.POST[sqlUtility.BOOKING_ID],
                                              uname=request.session['userid']).count() >= 1):
                activeBooking = ActiveBookings.objects.get(bookingId=request.POST[sqlUtility.BOOKING_ID],
                                                           uname=request.session['userid'])
                # if not int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:
                #     alert(text='Booking Delete Failed!', title='Failure', button='OK')
                #     return redirect('/view-booking-details/?id=' + request.POST.get('booking_id'))
            else:
                activeBooking = ActiveBookings.objects.get(bookingId=request.POST[sqlUtility.BOOKING_ID])
                activeBooking.delete()
                if int(time.time()) - activeBooking.locktime > activeBooking.lockDuration:
                    BookingService.deleteBooking(request, request.POST.get(sqlUtility.BOOKING_ID))
                    alert(text='Booking Delete Success!', title='Success', button='OK')
                    return redirect('/view-bookings/')
                else:
                    alert("Booking Screen is active in the system")
                    return view_booking_details(request)

        else:
            BookingService.deleteBooking(request, request.POST.get(sqlUtility.BOOKING_ID))
            alert(text='Booking Delete Success!', title='Success', button='OK')
            return redirect('/view-bookings/')


    else:
        alert(text='Booking Delete Failed!', title='Failure', button='OK')
        return redirect('/view-booking-details/?id=' + request.POST.get('booking_id'))
