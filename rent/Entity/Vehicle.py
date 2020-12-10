import time
from rent.DAO import sqlUtility
class car:

    def __init__(self,type,prod_year,booked,license_plate,brand,model,color):
        self._type = type
        self._prodYear = prod_year
        self._booked = booked
        self._brand = brand
        self._model = model
        self._color = color
        self._license_plate = license_plate
        self._booked = booked
        self._time_stamp = int(time.time())

    def getData(self):
        data = (self._type,int(self._prodYear),self._booked,self._license_plate,self._brand,self._model,self._color,self._time_stamp)
        return data

    def asDict(self):
        return {sqlUtility.VEHICLE_TYPE: self.type, sqlUtility.VEHICLE_BRAND: self.brand, sqlUtility.VEHICLE_MODEL: self.model,
                sqlUtility.VEHICLE_PROD_YEAR: self.prod_year, sqlUtility.VEHICLE_COLOR: self.color, sqlUtility.VEHICLE_BOOKED: str(self.booked).lower(),
                sqlUtility.VEHICLE_LICENSE_PLATE: self.license_plate}


    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value


    @property
    def prod_year(self):
        return self._prodYear

    @prod_year.setter
    def prod_year(self, value):
        self._prodYear = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def license_plate(self):
        return self._license_plate

    @license_plate.setter
    def license_plate(self, value):
        self._license_plate = value

    @property
    def booked(self):
        return self._booked

    @booked.setter
    def booked(self, value):
        self._booked = value

    @property
    def time_stamp(self):
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        self._time_stamp = value