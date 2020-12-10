from rent.DAO import VehicleDAO
from rent.Entity import Vehicle
from rent import Utility
from rent.DAO import sqlUtility


def fetchCars():
    carObjects = VehicleDAO.getAllCars()

    cars = []
    for row in carObjects:
        print('row')
        print(row)

        cars.append(row)

    print('cars')
    print(cars)
    if not cars:
        print('no cars')
        {}
    else:
        return cars


def getCarByLicense(licensePlate):
    car = VehicleDAO.getCar(licensePlate)
    return car

def addVehicle(request):
    print('adding car ')
    booked = 0
    if request.POST.get("status") == "booked":
        booked = 1
    car = Vehicle.car(request.POST.get(sqlUtility.VEHICLE_TYPE), request.POST.get(sqlUtility.VEHICLE_PROD_YEAR), booked,
                      request.POST.get(sqlUtility.VEHICLE_LICENSE_PLATE),
                      request.POST.get(sqlUtility.VEHICLE_BRAND),
                      request.POST.get(sqlUtility.VEHICLE_MODEL), request.POST.get(sqlUtility.VEHICLE_COLOR)
                      )
    print('adding car ',car)
    VehicleDAO.addCar(car)
    return car

def modifyVehicle(request):
    booked = 0
    if request.POST.get("status") == "booked":
        booked = 1

    car = Vehicle.car(request.POST.get(sqlUtility.VEHICLE_TYPE), request.POST.get(sqlUtility.VEHICLE_PROD_YEAR), booked,
                      request.POST.get(sqlUtility.VEHICLE_LICENSE_PLATE),
                      request.POST.get(sqlUtility.VEHICLE_BRAND),
                      request.POST.get(sqlUtility.VEHICLE_MODEL), request.POST.get(sqlUtility.VEHICLE_COLOR)
                      )

    oldObj = VehicleDAO.getCar(car.license_plate)
    if oldObj[sqlUtility.TIME_STAMP] > car.time_stamp:
        alert('Customer already modified by other clerk')
        result['updated'] = False
        return result
    else:
        result = VehicleDAO.modifyCar(car)
        result['updated'] = True
        return result

    return car

def deleteVehicle(request):
    VehicleDAO.deleteCar(request.POST.get(sqlUtility.VEHICLE_LICENSE_PLATE))

# GET CARS AVAILABLE FOR BOOKING
def getAvailableCars():
    cars = VehicleDAO.getAvailableCar()
    return cars
