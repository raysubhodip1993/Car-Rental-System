from rent.Controller.AppController import *
from rent.Service import BookingService
from django.http import HttpResponse
import json
from rent.models import *
from rent.DAO import sqlUtility
from rent.Service import EmployeeService
from rent import models

filepath = 'TestData/ClientDetails.txt'

employeeHeader = ['first_name', 'last_name', 'type', 'uname', 'password']

bookingFilepath = 'TestData/BookingDetails.txt'
carFilepath = 'TestData/CarDetails.txt'


def create_employee(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    template = loader.get_template('admin/create-employee.html')
    return HttpResponse(template.render({}, request))


def edit_employee(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))


    eid=request.GET.get('emp_id')
    print(eid)
    employee = EmployeeService.getEmployeeByID(eid)
    if (ActiveUsers.objects.filter(empid=employee['emp_id']).count() >= 1):
        alert("Active Employee, Cant'Update")
        template = loader.get_template('admin/view-employees.html')
        employees = EmployeeService.getAllEmployees()
        return HttpResponse(template.render({'employees': employees}, request))
    employee = EmployeeService.getEmplyeeById(request.GET.get('emp_id'))
    template = loader.get_template('admin/edit-employee.html')
    return HttpResponse(template.render({'data': employee}, request))


def view_employees(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        employees = EmployeeService.getAllEmployees()
        activeCars = ActiveCars.objects.filter(uname=request.session['userid'])
        for activeCar in activeCars:
            activeCar.delete()
        activeCustomers = ActiveCustomer.objects.filter(uname=request.session['userid'])
        for activeCust in activeCustomers:
            activeCust.delete()
        activeBookings = ActiveBookings.objects.filter(uname=request.session['userid'])
        for activeBooking in activeBookings:
            activeBooking.delete()
        print('employees')
        print(employees)
        template = loader.get_template('admin/view-employees.html')
        return HttpResponse(template.render({'employees': employees}, request))


def view_employee_details(request):
    print('view employee details')
    print(request.GET)
    print(request.GET.get('emp_id'))
    if request.method == 'GET':
        employees = EmployeeService.getAllEmployees()
        currentEmployee = dict()
        nextEmployee = dict()
        previousEmplyoee = dict()
        for index, employee in enumerate(employees):
            if ((request.method == 'GET' and (employee['emp_id'] == int(request.GET.get('emp_id')))) or (
                    (request.method == 'POST' and employee['emp_id'] == int(request.POST.get('emp_id'))))):
                currentEmployee = employee
                if (index > 0):
                    previousEmplyoee = employees[index - 1]
                else:
                    previousEmplyoee = employees[len(employees) - 1]
                if (index < (len(employees) - 1)):
                    nextEmployee = employees[index + 1]
                else:
                    nextEmployee = employees[0]
        data = dict()
        data['currentEmployee'] = currentEmployee
        data['nextEmployee'] = nextEmployee['emp_id']
        data['previousEmplyoee'] = previousEmplyoee['emp_id']

        template = loader.get_template('admin/view-employee-details.html')
        return HttpResponse(template.render({'data': data}, request))



########################################################################################################################

def fetchClerkDetails():
    clerkObjects = EmployeeService.getEmployees()

    list(EmployeeDB.objects.filter(type='c'))

    clerks = []
    for clerk in clerkObjects:
        print('clerk')
        print(clerk.asDict())
        clerks.append(clerk.asDict())
    if not clerks:
        print('no clerks')
        return {}
    else:
        return clerks


def fetchEmployee(uname):
    employees = EmployeeDB.objects.all()

    currentEmployee = dict()
    nextEmployee = ""
    previousEmployee = ""
    print('request.GET.get(uname)')
    print(employees.all())
    for index, employee in enumerate(employees):
        print('employee ')
        print(employee.asDict())
        if (employee.uname == uname):
            currentEmployee = employee.asDict()
            if (index > 0):
                previousEmployee = employees[index - 1].uname
            else:
                previousEmployee = employees[len(employees) - 1].uname
            if (index < (len(employees) - 1)):
                nextEmployee = employees[index + 1].uname
            else:
                nextEmployee = employees[0].uname
    data = dict()
    data['currentEmployee'] = currentEmployee
    data['previousEmployee'] = previousEmployee
    data['nextEmployee'] = nextEmployee
    return data


def AddClerkDetails(request):
    print(request.POST)
    if request.method == 'POST':
        print('here here here')
        if request.POST.get('first_name') and request.POST.get(
                'last_name') and request.POST.get(
            'uname') and request.POST.get('type'):

            employee = EmployeeService.saveEmployeeDetails(request)

        return redirect('/view-employee-details/?emp_id=' + str(employee.emp_id))
    else:
        employees = EmployeeService.fetchClerkDetails()
        template = loader.get_template('admin/view-employees.html')
        return HttpResponse(template.render({'employees': employees}, request))


def modifyEmployee(request):
    print(request.POST)
    if request.method == 'POST':
        print('here here here mnbjh')
        if request.POST.get('emp_id') and request.POST.get('first_name') and request.POST.get(
                'last_name') and request.POST.get(
            'uname') and request.POST.get('type'):
            print('here here here')
            result = EmployeeService.updateEmpDetails(request)
            if not result["updated"]:
                request.method = 'GET'
                template = loader.get_template('admin/view-employees.html')
                return HttpResponse(template.render({'employees': employees}, request))
        return redirect('/view-employee-details/?emp_id=' + request.POST.get('emp_id'))
    else:
        employees = EmployeeService.fetchClerkDetails()
        template = loader.get_template('admin/view-employees.html')
        return HttpResponse(template.render({'employees': employees}, request))


def deleteEmployee(request):
    if request.method == 'POST':
        print('delete employee')
        print(request.POST)
        if request.POST.get('emp_id'):
            eid = request.POST.get('emp_id')
            print(eid)
            employee = EmployeeService.getEmployeeByID(eid)
            if (ActiveUsers.objects.filter(empid=employee['emp_id']).count() >= 1):
                alert("Employee status = Active, Cant'Delete")
                template = loader.get_template('admin/view-employees.html')
                employees = EmployeeService.getAllEmployees()
                return HttpResponse(template.render({'employees': employees}, request))
            else:
                EmployeeService.deletEmployee(request.POST.get('emp_id'))
        else:
            alert(text='Customer Deletion Failed!', title='Failure', button='OK')
        employees = EmployeeService.getAllEmployees()
        template = loader.get_template('admin/view-employees.html')
        return HttpResponse(template.render({'employees': employees}, request))
