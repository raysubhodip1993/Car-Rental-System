from django.contrib.sessions.models import Session

from rent.Service import EmployeeService
from rent.Controller.SessionController import FuncThread
from rent.models import *
from django.http import *
from django.shortcuts import redirect
from django.template import loader
from rent.Service import CustomerService
from rent.Service import VehicleService
from pymsgbox import *
import multiprocessing
import threading
import time
from rent.Service import BookingService
from rent.Service import EmployeeService
from rent.Controller import VehicleController
from rent.DAO import BaseDAO
from rent.DAO import sqlUtility
from rent.Entity import Employee

custHeader = ['first_name', 'last_name', 'driving_licence', 'expiry_date', 'phone_no']


# flag=1


def constant():
    print("CC")


def login(request):
    employee = Employee.Clerk(None, "", "", "", "", "")
    print("jfgDGJGsdkj")
    print(request.POST)
    # if request.method != 'POST':
    #     raise Http404('')
    print("here 1")
    # try:
    baseDao = BaseDAO.DbConnection()
    employee = EmployeeService.getEmployeeByUserName(request.POST['username'])
    print("empppppppp")
    print(employee)
    try:
        if employee['password'] == request.POST['password']:

            result = AdminStatus.objects.values('stat')
            list_result = [entry for entry in result]  # converts ValuesQuerySet into Python list
            print('result admin stat db')
            print(list_result)

            if employee['type'] == 'a':
                if {'stat': '0'} in list_result:
                    print("One admin instance already open, only one allowed at a time")
                    template = loader.get_template('Exception/oneAdminError.html')
                    return HttpResponse(template.render({}, request))
                else:
                    print('employee type')
                    print(employee['type'])
                    print('employee id')
                    print(employee['emp_id'])

                    request.session['user'] = employee
                    request.session['userid'] = employee['uname']
                    request.session['id'] = employee['emp_id']

                    activeCars = ActiveCars.objects.filter(uname=request.session['userid'])
                    for activeCar in activeCars:
                        activeCar.delete()
                    activeCustomers = ActiveCustomer.objects.filter(uname=request.session['userid'])
                    for activeCust in activeCustomers:
                        activeCust.delete()
                    AdminStatus.objects.all().delete()
                    adminStatus = AdminStatus(stat="0")
                    adminStatus.save()

                    activeUser = ActiveUsers(empid=employee['emp_id'])
                    activeUser.save()

                    userstat = {'stato': AdminStatus.objects.all()}
                    for i in userstat:
                        print(i, userstat[i])
                        flag = userstat[i]
                    # flag=0
                    print("Hello....:", flag)
                    # request.session['loggedInAs'] = user.type

                    return redirect('homePage')

            # p1 = ActiveUsers.objects.all()
            if employee['type'] == 'c':
                print(ActiveUsers.objects.filter(empid=employee['emp_id']).count())
                if (ActiveUsers.objects.filter(empid=employee['emp_id']).count() >= 1):
                    alert("You are already Logged in somewhere else in this beautiful world")
                    template = loader.get_template('auth/login.html')
                    return HttpResponse(template.render({}, request))
                else:
                    request.session['user'] = employee
                    request.session['userid'] = employee['uname']
                    request.session['id'] = employee['emp_id']
                    activeCars = ActiveCars.objects.filter(uname=request.session['userid'])
                    for activeCar in activeCars:
                        activeCar.delete()
                    activeCustomers = ActiveCustomer.objects.filter(uname=request.session['userid'])
                    for activeCust in activeCustomers:
                        activeCust.delete()
                    print("hasfjasjvcajsvcjascjavscjhasvjaytidagudua")
                    activeUser = ActiveUsers(empid=employee['emp_id'])
                    activeUser.save()
                    # t1 = FuncThread(someOtherFunc, [1, 2], 6)
                    # t1.start()
                    # t1.join()
                    return redirect("dashboard")
    except:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    else:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))


# except EmployeeDB.DoesNotExist:
#     template = loader.get_template('auth/login.html')
#     return HttpResponse(template.render({}, request))


def modifyBooking(request):
    if request.method == 'POST':
        print('modify booking')
        print(request.POST)
        # if request.POST.get('booking_id') and request.POST.get('first_name') and request.POST.get(
        #         'last_name') and request.POST.get('driving_license') and request.POST.get(
        #     'starDate') and request.POST.get('license_plate') and request.POST.get('endDate'):
        print('tes test teste')
        BookingService.modifyBooking(request)
        return redirect('/view-booking-details/?id=' + request.POST.get('booking_id'))


def createEmployee(request):
    if request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get(
            'uname') and request.POST.get(
        'password') and request.POST.get('type'):

        EmployeeService.AddClerkDetails(request)
        return redirect('/view-employee-details/?uname=' + request.POST.get('uname'))
    else:
        alert(text='Customer Creation Failed!', title='Failure', button='OK')
        template = loader.get_template('create-booking.html')
        return HttpResponse(template.render({}, request))


def addVehicle(request):
    print(request.POST)
    if request.POST.get('type') and request.POST.get('brand') and request.POST.get(
            'model') and request.POST.get('prod_year') and request.POST.get('license_plate') and request.POST.get(
        'color'):

        CarService.AddCarDetails(request)

        return redirect('/view-vehicle?license=' + request.POST.get('license_plate'))

    else:
        alert(text='Customer Creation Failed!', title='Failure', button='OK')
        template = loader.get_template('create-booking.html')
        return HttpResponse(template.render({}, request))


def deleteVehicle(request):
    print('delete vehicle')
    print(request.POST)
    if request.POST.get('license_plate'):
        print('here thvvjk')
        CarService.DeleteCarDetails(request.POST.get('license_plate'))
        template = loader.get_template('clerk/view-catalog.html')
        return VehicleController.view_catalog(request)
    else:
        alert(text='Customer Creation Failed!', title='Failure', button='OK')
        return VehicleController.view_catalog(request)


def login2(request):
    employee = EmployeeDB()

    if request.method != 'POST':
        raise Http404('')
    try:
        print(EmployeeDB.objects.all())
        user = EmployeeDB.objects.get(uname=request.POST['username'])
        print('request.session')
        print(request.session)
        if user.password == request.POST['password']:
            request.session['user'] = user.asDict()
            request.session['userid'] = user.uname
            return redirect('dashboard')
        else:
            # msg.Popup('Error Login in, Check User Name or Password.')
            template = loader.get_template('auth/login.html')
            return HttpResponse(template.render({}, request))

    except EmployeeDB.DoesNotExist:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))


