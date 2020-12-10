import time

class Customer:

    def __init__(self,first_name,last_name,driving_license,expiry_date,phone_no):
        #self._employee_id = employee_id
        self._first_name = first_name
        self._last_name = last_name
        self._driving_license = driving_license
        self._expiry_date = expiry_date
        self._phone_no = phone_no
        self._time_stamp = int(time.time())

    def getData(self):
        data = (self._first_name,self._last_name,self._phone_no,self._driving_license,self._expiry_date,self._time_stamp)
        return data


    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def expiry_date(self):
        return self._expiry_date

    @expiry_date.setter
    def expiry_date(self, value):
        self._expiry_date = value

    @property
    def driving_license(self):
        return self._driving_license

    @driving_license.setter
    def driving_license(self, value):
        self._model = value


    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def phone_no(self):
        return self._phone_no

    @phone_no.setter
    def phone_no(self, value):
        self._phone_no = value

    @property
    def time_stamp(self):
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        self._time_stamp = value

