from rent.Controller.AppController import *
from rent.Service import BookingService
from django.http import HttpResponse
import json
from rent.models import ActiveCustomer, ActiveUsers, ActiveCars
import time

filepath = 'TestData/ClientDetails.txt'

custHeader = ['first_name', 'last_name', 'driving_licence', 'expiry_date', 'phone_no']

bookingFilepath = 'TestData/BookingDetails.txt'
carFilepath = 'TestData/CarDetails.txt'


def create_customer(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        template = loader.get_template('clerk/create-customer.html')
        return HttpResponse(template.render({}, request))


def view_customers(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    customers = CustomerService.getAllCustomers()
    activeCars = ActiveCars.objects.filter(uname=request.session['userid'])
    for activeCar in activeCars:
        activeCar.delete()
    activeCustomers = ActiveCustomer.objects.filter(uname=request.session['userid'])
    for activeCust in activeCustomers:
        activeCust.delete()
    activeBookings = ActiveBookings.objects.filter(uname=request.session['userid'])
    for activeBooking in activeBookings:
        activeBooking.delete()
    template = loader.get_template('clerk/view-customers.html')
    return HttpResponse(template.render({'customers': customers}, request))


def view_customer(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        customerData = CustomerService.fetchCustomer(request.GET.get('driving_license'))
        # customerData = CustomerService.getCustomer(request.GET.get('driving_license'))
        print(customerData)
        template = loader.get_template('clerk/view-customer.html')
        return HttpResponse(template.render({'data': customerData}, request))


def edit_customer(request):
    print('###################################')
    print()
    print("sesion")
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    print()
    print('###################################')
    customerData = CustomerService.fetchCustomer(request.GET.get('driving_license'))
    transactions = BookingService.fetchTransactionHistory()
    print('transactions')
    print(transactions)
    print('customerData')
    print(customerData)
    if customerData['currentCustomer']:
        for tran in transactions:
            if (tran[sqlUtility.CUSTOMER_DRIVING_LICENSE] == customerData['currentCustomer'][
                sqlUtility.CUSTOMER_DRIVING_LICENSE]):
                alert("Customer has an active booking can not modify")
                return view_customer(request)
        if (ActiveCustomer.objects.filter(custid=request.GET['driving_license']).count() >= 1):
            if (ActiveCustomer.objects.filter(custid=request.GET['driving_license'],
                                              uname=request.session['userid']).count() >= 1):
                activeCust = ActiveCustomer.objects.get(custid=request.GET['driving_license'],
                                                        uname=request.session['userid'])
                # if int(time.time()) - activeCust.locktime > activeCust.lockDuration:
                #     activeCust.delete()
                #     activeCust = ActiveCustomer(custid=customerData['currentCustomer']['driving_license'],
                #                                 uname=request.session['userid'],
                #                                 locktime=int(time.time()), lockDuration=60)
                #     activeCust.save()
                #     template = loader.get_template('clerk/edit-customer.html')
                #     return HttpResponse(template.render({'customer': customerData['currentCustomer']}, request))
                # else:
                activeCust.lockDuration = 60
                activeCust.save()
                template = loader.get_template('clerk/edit-customer.html')
                return HttpResponse(template.render({'customer': customerData['currentCustomer']}, request))
            else:
                activeCust = ActiveCustomer.objects.get(custid=request.GET['driving_license'])
                if int(time.time()) - activeCust.locktime > activeCust.lockDuration:
                    activeCust.delete()
                    activeCust = ActiveCustomer(custid=customerData['currentCustomer']['driving_license'],
                                                uname=request.session['userid'],
                                                locktime=int(time.time()), lockDuration=60)
                    activeCust.save()
                    template = loader.get_template('clerk/edit-customer.html')
                    return HttpResponse(template.render({'customer': customerData['currentCustomer']}, request))
                else:
                    alert("Customer is active in the system")
                    return view_customer(request)
        else:
            activeCust = ActiveCustomer(custid=customerData['currentCustomer']['driving_license'],
                                        uname=request.session['userid'],
                                        locktime=int(time.time()), lockDuration=60)
            activeCust.save()
            template = loader.get_template('clerk/edit-customer.html')
            return HttpResponse(template.render({'customer': customerData['currentCustomer']}, request))

    else:
        alert("No Customer with these details")
        return view_customers(request)


########################################################################################################################


def fetchCustomerDetails():
    custObjects = CustomerDB.objects.all()
    customers = []
    for customer in custObjects:
        print('customer')
        print(customer.asDict())
        i = 0
        customerDict = customer.asDict()
        customers.append(customerDict)
    if not customers:
        print('no customers')
        return {}
    else:
        return customers


def createCust(request):
    if request.method == 'POST':
        if request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get(
                'driving_license') and request.POST.get('phone_no') and request.POST.get('expiry_date'):
            CustomerService.addCustDetails(request)
            alert(text='Customer Creation Success!', title='Success', button='OK')
            return redirect('/view-customer/?driving_license=' + request.POST.get('driving_license'))
        else:
            alert(text='Customer Creation Failed!', title='Failure', button='OK')
            template = loader.get_template('clerk/create-customer.html')
            return HttpResponse(template.render({}, request))


def createCustForBooking(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get(
                'driving_license') and request.POST.get('phone_no') and request.POST.get('expiry_date'):
            CustomerService.addCustDetails(request)
            activeCust = ActiveCustomer(custid=request.POST.get(
                'driving_license'), uname=request.session['userid'],
                locktime=int(time.time()), lockDuration=120)
            activeCust.save()
            alert(text='Customer Creation Success!', title='Success', button='OK')
            return redirect('/view-customer/?driving_license=' + request.POST.get('driving_license'))
        else:
            alert(text='Customer Creation Failed!', title='Failure', button='OK')
            template = loader.get_template('clerk/create-customer.html')
            return HttpResponse(template.render({}, request))


def modifyCust(request):
    if request.method == 'POST':
        if (ActiveCustomer.objects.filter(custid=request.POST['driving_license']).count() >= 1):
            if (ActiveCustomer.objects.filter(custid=request.POST['driving_license'],
                                              uname=request.session['userid']).count() >= 1):
                activeCust = ActiveCustomer.objects.get(custid=request.POST['driving_license'],
                                                        uname=request.session['userid'])
                if int(time.time()) - activeCust.locktime > activeCust.lockDuration:
                    activeCust.delete()
                    alert(text='Customer Modify Failed! Session Expired', title='Failure', button='OK')
                    return redirect('/edit-customer/?driving_license=' + request.POST.get('driving_license'))
            else:
                activeCust = ActiveCustomer.objects.get(custid=request.POST['driving_license'])
                if not int(time.time()) - activeCust.locktime > activeCust.lockDuration:
                    alert(text='Customer account is active in another session', title='Failure', button='OK')
                    return redirect('/edit-customer/?driving_license=' + request.POST.get('driving_license'))

        print('test test')
        print(request.POST)
        if request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get(
                'driving_license') and request.POST.get('phone_no') and request.POST.get('expiry_date'):
            customer = CustomerService.getCustomer(request.POST.get('driving_license'))
            if customer:
                result = CustomerService.updateCustDetails(request)
                if not result["updated"]:
                    request.method = 'GET'
                    return view_customers(request)
                alert(text='Customer Modify Success!', title='Success', button='OK')
                return redirect('/view-customer/?driving_license=' + request.POST.get('driving_license'))
            else:
                alert("No Customer with these details")
                return view_customers(request)
        else:
            alert(text='Customer Modify Failed!', title='Failure', button='OK')
            return redirect('/edit-customer/?driving_license=' + request.POST.get('driving_license'))


def deleteCust(request):
    if request.POST.get('driving_license'):

        customerData = CustomerService.fetchCustomer(request.POST.get('driving_license'))
        transactions = BookingService.fetchTransactionHistory()
        if customerData['currentCustomer']:
            for tran in transactions:
                if (tran[sqlUtility.CUSTOMER_DRIVING_LICENSE] == customerData['currentCustomer'][
                    sqlUtility.CUSTOMER_DRIVING_LICENSE]):
                    alert("Customer has an active booking can not delete")
                    return view_customers(request)

            if (ActiveCustomer.objects.filter(custid=request.POST['driving_license']).count() >= 1):
                if (ActiveCustomer.objects.filter(custid=request.POST['driving_license'],
                                                  uname=request.session['userid']).count() >= 1):
                    activeCust = ActiveCustomer.objects.get(custid=request.POST['driving_license'],
                                                            uname=request.session['userid'])
                    # if int(time.time()) - activeCust.locktime > activeCust.lockDuration:
                    activeCust.delete()
                    CustomerService.deletCustomer(request.POST.get('driving_license'))
                    alert(text='Customer Delete Success!', title='Success', button='OK')
                    return redirect('/view-customers/')
                    # else:
                    #     alert("Customer is active in the system")
                    #     customerData = CustomerService.fetchCustomer(request.POST.get('driving_license'))
                    #     template = loader.get_template('clerk/view-customer.html')
                    #     return HttpResponse(template.render({'data': customerData}, request))
                else:
                    activeCust = ActiveCustomer.objects.get(custid=request.POST['driving_license'])
                    if int(time.time()) - activeCust.locktime > activeCust.lockDuration:
                        activeCust.delete()
                        CustomerService.deletCustomer(request.POST.get('driving_license'))
                        alert(text='Customer Delete Success!', title='Success', button='OK')
                        return redirect('/view-customers/')
                    else:
                        alert("Customer is active in the system")
                        customerData = CustomerService.fetchCustomer(request.POST.get('driving_license'))
                        template = loader.get_template('clerk/view-customer.html')
                        return HttpResponse(template.render({'data': customerData}, request))
            else:
                CustomerService.deletCustomer(request.POST.get('driving_license'))
                alert(text='Customer Delete Success!', title='Success', button='OK')
                return redirect('/view-customers/')
        else:
            alert("No Customer with these details")
            return view_customers(request)
    else:
        alert(text='Customer Delete Failed!', title='Failure', button='OK')
        return redirect('/view-customer/?driving_license=' + request.POST.get('driving_license'))


# SEARCH CUSTOMER USING DRIVING LICENSE
def findCust(request):
    # print(request.GET)
    data = {}
    data['found'] = False
    data['customer'] = {}
    data['status'] = "unavailable"
    print("request.GET.get('driving_license')")
    print(request.GET.get('driving_license'))
    if request.method == 'GET':
        if request.GET.get('driving_license'):

            if (ActiveCustomer.objects.filter(custid=request.GET['driving_license']).count() >= 1):
                if (ActiveCustomer.objects.filter(custid=request.GET['driving_license'],
                                                  uname=request.session['userid']).count() >= 1):
                    activeCust = ActiveCustomer.objects.get(custid=request.GET['driving_license'],
                                                            uname=request.session['userid'])
                    if int(time.time()) - activeCust.locktime > activeCust.lockDuration:
                        alert("Session Expired")
                        return view_customer(request)
                    else:
                        activeCust(lockDuration=120)
                        activeCust.save()
                    custObj = CustomerService.getCustomer(request.GET.get('driving_license'))
                    data['found'] = True
                    data['customer'] = custObj
                    data['status'] = "inactive"
                    return JsonResponse(data)
                else:
                    alert("Customer is active in the system")
                    data['status'] = "active"
                    return view_customer(request)

            else:
                custObj = CustomerService.getCustomer(request.GET.get('driving_license'))
                ActiveCustomer.objects.filter(uname=request.session['userid']).delete()
                if custObj:
                    data['found'] = True
                    data['customer'] = custObj
                    data['status'] = "inactive"

                    activeCust = ActiveCustomer(custid=custObj['driving_license'], uname=request.session['userid'],
                                                locktime=int(time.time()), lockDuration=120)
                    activeCust.save()

    return JsonResponse(data)
