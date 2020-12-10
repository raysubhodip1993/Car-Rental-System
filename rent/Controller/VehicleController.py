from rent.Controller.AppController import *
from rent.Service import BookingService
from django.http import HttpResponse
from rent.models import *
from rent.DAO import BaseDAO
from rent.DAO import sqlUtility
from rent.Service import VehicleService
from django.contrib.sessions.models import Session
from rent.models import ActiveCars, ActiveUsers, ActiveCustomer
import json


def view_catalog(request):
    if 'user' not in request.session:
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
    cars = VehicleService.fetchCars()
    print('cars in catalog')
    page = 'clerk/view-catalog.html'
    template = loader.get_template(page)
    request.session['currentPage'] = page
    return HttpResponse(template.render({'cars': cars}, request))


def view_vehicle(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET' or request.method == 'POST':
        cars = VehicleService.fetchCars()
        currentCar = dict()
        nextCar = dict()
        previousCar = dict()
        print("carsssssssssssssssss ")
        print(cars)
        print(request.GET)
        print(request.POST)
        for index, car in enumerate(cars):
            if (car['license_plate'] == request.GET.get('license_plate') or car['license_plate'] == request.POST.get(
                    'license_plate') or car['license_plate'] == request.GET.get('license')):
                currentCar = car
                if (index > 0):
                    previousCar = cars[index - 1]
                else:
                    previousCar = cars[len(cars) - 1]
                if (index < (len(cars) - 1)):
                    nextCar = cars[index + 1]
                else:
                    nextCar = cars[0]
        data = dict()
        if (currentCar['booked'] == 1):
            currentCar['status'] = 'booked'
        else:
            currentCar['status'] = 'available'
        data['currentCar'] = currentCar
        data['nextCar'] = nextCar['license_plate']
        data['previousCar'] = previousCar['license_plate']

    template = loader.get_template('clerk/view-vehicle.html')
    return HttpResponse(template.render({'data': data}, request))


def add_vehicle(request):
    if 'user' not in request.session:
        template = loader.get_template('auth/login.html')
        return HttpResponse(template.render({}, request))
    template = loader.get_template('admin/new-vehicle.html')
    return HttpResponse(template.render({}, request))


def edit_vehicle(request):
    vehicle = VehicleService.getCarByLicense(str(request.GET.get('license_plate')))
    if vehicle['booked']:
        alert("Vehicle is in booked state can not update")
        return view_vehicle(request)
    else:
        if (ActiveCars.objects.filter(carid=request.GET['license_plate']).count() >= 1):
            activeCar = ActiveCars.objects.get(carid=request.GET['license_plate'])
            print("activeeeeeeeeeeeeeeee ")
            print(activeCar)
            if activeCar and (int(time.time()) - activeCar.locktime) > activeCar.lockDuration:
                activeCar.delete()
                activeCar = ActiveCars(carid=request.GET.get('license_plate'),
                                       uname=request.session['userid'],
                                       locktime=int(time.time()), lockDuration=60)
                activeCar.save()
                vehicle = VehicleService.getCarByLicense(str(request.GET.get('license_plate')))
                template = loader.get_template('admin/edit-vehicle.html')
                return HttpResponse(template.render({'vehicle': vehicle}, request))
            else:
                alert("Vehicle is active in the system")
                return view_vehicle(request)
        else:
            activeCar = ActiveCars(carid=request.GET.get('license_plate'),
                                   uname=request.session['userid'],
                                   locktime=int(time.time()), lockDuration=60)
            activeCar.save()
            vehicle = VehicleService.getCarByLicense(str(request.GET.get('license_plate')))
            template = loader.get_template('admin/edit-vehicle.html')
            return HttpResponse(template.render({'vehicle': vehicle}, request))


########################################################################################################################
def addVehicle(request):
    print('edit vehicle')
    print(request.POST)
    if request.POST.get('type') and request.POST.get('brand') and request.POST.get(
            'model') and request.POST.get('prod_year') and request.POST.get('license_plate') and request.POST.get(
        'color'):

        VehicleService.addVehicle(request)
    else:
        alert(text='Vehicle Creation Failed!', title='Failure', button='OK')
    return view_catalog(request)


def editVehicle(request):
    print('edit vehicle')
    print(request.POST)
    if request.POST.get('license_plate'):
        print('here thvvjk')
        print(request.POST.get(sqlUtility.VEHICLE_PROD_YEAR))
        result = VehicleService.modifyVehicle(request)
        if not result["updated"]:
            return VehicleController.view_catalog(request)
        return view_vehicle(request)
    else:
        alert(text='Customer Creation Failed!', title='Failure', button='OK')
        return VehicleController.view_catalog(request)


def deleteVehicle(request):
    print('edit vehicle')
    print(request.POST)
    if request.POST.get('license_plate'):
        vehicle = VehicleService.getCarByLicense(str(request.POST.get('license_plate')))
        if vehicle['booked']:
            alert("Vehicle is in booked state can not delete")
            return view_vehicle(request)

        if vehicle[sqlUtility.VEHICLE_BOOKED]:
            alert(text='vehicle in booked state')
            return view_vehicle(request)
        if (ActiveCars.objects.filter(carid=request.POST['license_plate']).count() >= 1):
            activeCar = ActiveCars.objects.get(carid=request.POST['license_plate'], uname=request.session['userid'])
            print("activeeeeeeeeeeeeeeee ")
            print(activeCar)
            if activeCar:
                activeCar.delete()
                VehicleService.deleteVehicle(request)
                return view_catalog(request)
            else:
                alert(text='Car is active in the system')
                activeCar.delete()
                return view_vehicle(request)
        if (len(VehicleService.fetchCars()) < 2):
            alert(text='There should be atleast one car in the catalog')
            # request.GET['license_plate'] = request.POST['license_plate']
            return view_vehicle(request)

        print(vehicle["license_plate"])
        if (ActiveCars.objects.filter(carid=vehicle["license_plate"]).count() >= 1):
            alert("Car Operations in Process, Cannot Delete.")
            # template = loader.get_template('clerk/view-catalog.html')
            return redirect('dashboard')
        VehicleService.deleteVehicle(request)
        return view_catalog(request)
    else:
        alert(text='Customer Creation Failed!', title='Failure', button='OK')
    return view_catalog(request)


def lockVehicle(request):
    data = {}
    catalog = []
    if request.GET.get('license_plate'):
        if (ActiveCars.objects.filter(carid=request.GET['license_plate']).count() >= 1):
            if (ActiveCars.objects.filter(carid=request.GET['license_plate'],
                                          uname=request.session['userid']).count() >= 1):
                cars = ActiveCars.objects.filter(carid=request.GET['license_plate'],
                                                 uname=request.session['userid'])

                for car in cars:
                    print('###################33 car')
                    print(car)
                    car.lockDuration = 120
                    car.save()
                data['status'] = "available"

            else:
                data['status'] = "unavailable"

            catalog = VehicleService.getAvailableCars()
            data['catalog'] = catalog
            return JsonResponse({'data': data})

        else:
            data['status'] = "available"
            catalog = VehicleService.getAvailableCars()
            data['catalog'] = catalog
            ActiveCars.objects.filter(uname=request.session['userid']).delete()

            car = ActiveCars(carid=request.GET.get('license_plate'), uname=request.session['userid'],
                             locktime=int(time.time()),
                             lockDuration=120)
            car.save()
            return JsonResponse({'data': data})
