import time


class ReservationObject:

    def __init__(self,startDate,endDate,drivingLicense,licensePlate,booking_status):
        self._startDate = startDate
        self._endDate = endDate
        self._drivingLicense = drivingLicense
        self._licensePlate = licensePlate
        self._booking_status = booking_status
        self._time_stamp = int(time.time())

    def getData(self):
        data = (self._drivingLicense,self._endDate,self._startDate,self._licensePlate,self._booking_status,self._time_stamp)
        return data


    @property
    def startDate(self):
        return self._startDate

    @startDate.setter
    def startDate(self, value):
        self._startDate = value

    @property
    def licensePlate(self):
        return self._licensePlate

    @licensePlate.setter
    def licensePlate(self, value):
        self._licensePlate = value

    @property
    def drivingLicense(self):
        return self._model

    @drivingLicense.setter
    def drivingLicense(self, value):
        self._drivingLicense = value


    @property
    def endDate(self):
        return self._endDate

    @endDate.setter
    def endDate(self, value):
        self._endDate = value

    @property
    def booking_status(self):
        return self._booking_status

    @booking_status.setter
    def booking_status(self, value):
        self._booking_status = value

    @property
    def time_stamp(self):
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        self._time_stamp = value

