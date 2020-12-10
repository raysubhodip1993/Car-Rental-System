from rent.Controller.AppController import *
from rent.Service import BookingService
from rent.DAO import BaseDAO
from rent.DAO import sqlUtility
from django.shortcuts import redirect
from django.template import loader
import multiprocessing
import threading
import time
from rent.models import *
from django.http import *

bookingFilepath = 'TestData/BookingDetails.txt'
carFilepath = 'TestData/CarDetails.txt'


def homePage(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    else:
        # print(request.session['user'])
        template = loader.get_template('clerk/view-catalog.html')
        return HttpResponse(template.render({}, request))


def logout(request):
    try:
        if 'user' not in request.session:
            print('Already Logged Out Of Session!!! Please Login')
            template = loader.get_template('auth/login.html')
            return HttpResponse(template.render({}, request))
        activeCars = ActiveCars.objects.filter(uname=request.session['userid'])
        for activeCar in activeCars:
            activeCar.delete()
        activeCustomers = ActiveCustomer.objects.filter(uname=request.session['userid'])
        for activeCust in activeCustomers:
            activeCust.delete()
        activeBookings = ActiveBookings.objects.filter(uname=request.session['userid'])
        for activeBooking in activeBookings:
            activeBooking.delete()
        print(request.session['id'])
        # p1 = ActiveUsers.objects.get()
        p1 = ActiveUsers.objects.get(empid=request.session['id']).delete()
        del request.session['user']
        baseDao = BaseDAO.DbConnection()
        baseDao.executeQuery(sqlUtility.LOGIN_DELETE_QUERY)
        baseDao.conn.close()
        p = AdminStatus.objects.all().delete()
        # p.delete()
        p = AdminStatus(stat="1")
        p.save()
        ActiveCars.objects.filter(uname=request.session['userid']).delete()
        ActiveCustomer.objects.filter(uname=request.session['userid']).delete()
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))

    except KeyError:
        pass
        print("Error Logging Out")




# Your foo function
def clearResources(n):
    for i in range(10000 * n):
        print("Tick")
        time.sleep(1)

if __name__ == '__main__':
    print("###################")
    # Start foo as a process
    p = multiprocessing.Process(target=clearResources, name="clearResources", args=(10,))
    p.start()

    # Wait 10 seconds for foo
    time.sleep(10)

    if p.is_alive():
        print("foo is running... let's kill it...")

        # Terminate foo
        p.terminate()
        p.join()


class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)


# Example usage



