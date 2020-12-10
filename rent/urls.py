"""rentacar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from rent.Controller import AppController
from rent.Controller import SessionController
from rent.Controller import BookingController
from rent.Controller import CustomerController
from rent.Controller import VehicleController
from rent.Controller import EmployeeController, ReservationController

urlpatterns = [
    ############################################################################################
    path('', VehicleController.view_catalog, name='homePage'),
    ############################################################################################
    path(r'view-catalog/', VehicleController.view_catalog, name='dashboard'),
    path(r'view-vehicle', VehicleController.view_vehicle, name='view-vehicle'),
    path(r'add-vehicle/', VehicleController.add_vehicle, name='add-vehicle'),
    path(r'edit-vehicle/', VehicleController.edit_vehicle, name='edit-vehicle'),

    path(r'create-customer/', CustomerController.create_customer, name='create-customer'),
    path(r'view-customers/', CustomerController.view_customers, name='view-customers'),
    path(r'view-customer/', CustomerController.view_customer, name='view-customer'),
    path(r'edit-customer/', CustomerController.edit_customer, name='edit-customer'),

    path(r'create-booking/', BookingController.create_booking, name='create-booking'),
    path(r'validate/', BookingController.validate, name='validate'),
    path(r'create-reservation/', ReservationController.create_reservation, name='create-reservation'),
    path(r'modify-booking/', BookingController.modify_booking, name='modify-booking'),
    path(r'modify-reservation/', ReservationController.modify_reservation, name='modify-reservation'),

    path(r'view-bookings/', BookingController.view_bookings, name='view-bookings'),
    path(r'view-transactions/', BookingController.view_transactions, name='view-transactions'),
    path(r'view-reservations/', ReservationController.view_reservations, name='view-reservations'),
    path(r'view-booking-details/', BookingController.view_booking_details, name='view-booking-details'),
    path(r'complete-booking/', BookingController.complete_booking, name='complete-booking'),
    path(r'cancel-reservation/', ReservationController.cancel_reservation, name='cancel-reservation'),
    path(r'view-transactions/', BookingController.view_transactions, name='view-transactions'),
    path(r'view-reservation/', ReservationController.view_reservations, name='view-reservation'),
    path(r'view-reservation-details/', ReservationController.view_reservation_details, name='view-reservation-details'),
    path(r'reservation-booking/', ReservationController.update_to_booking, name='view-booking-details'),

    path(r'create-employee/', EmployeeController.create_employee, name='create-employee'),
    path(r'edit-employee/', EmployeeController.edit_employee, name='edit-employee'),
    path(r'view-employees/', EmployeeController.view_employees, name='view-employees'),
    path(r'view-employee-details/', EmployeeController.view_employee_details, name='view-employee-details'),

    ############################################################################################
    path(r'login/', AppController.login, name='login'),
    path(r'logout/', SessionController.logout, name='logout'),

    path(r'createCust/', CustomerController.createCust, name='createCust'),
    path(r'createCustForBooking/', CustomerController.createCustForBooking, name='createCustForBooking'),
    path(r'editCust/', CustomerController.modifyCust, name='editCust'),
    path(r'deleteCust/', CustomerController.deleteCust, name='deleteCust'),
    path(r'findCust/', CustomerController.findCust, name='findCust'),
    path(r'modifyCust/', CustomerController.modifyCust, name='modifyCust'),
    path(r'deleteBooking/', BookingController.deleteBooking, name='deleteBooking'),
    # path(r'deleteReservation/', BookingController.deleteReservation, name='deleteReservation'),
    path(r'addBooking/', BookingController.createBooking, name='addBooking'),
    path(r'addReservation/', ReservationController.createReservation, name='addReservation'),

    path(r'modifyBooking/', BookingController.modifyBooking, name='modifyBooking'),
    path(r'modifyReservation/', ReservationController.modifyReservation, name='modifyReservation'),

    path(r'createEmployee/', EmployeeController.AddClerkDetails, name='AddClerkDetails'),
    path(r'modifyEmployee/', EmployeeController.modifyEmployee, name='modifyEmployee'),
    path(r'deleteEmployee/', EmployeeController.deleteEmployee, name='deleteEmployee'),
    path(r'newVehicle/', VehicleController.addVehicle, name='newVehicle'),
    path(r'deleteVehicle/', VehicleController.deleteVehicle, name='deleteVehicle'),
    path(r'editVehicle/', VehicleController.editVehicle, name='editVehicle'),
    path(r'selectCar/', VehicleController.lockVehicle, name='editVehicle'),

    ############################################################################################

]
