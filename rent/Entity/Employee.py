import time
class Clerk:

    def __init__(self,emp_id,first_name,last_name,uname,password,type):
        self._emp_id = emp_id
        self._first_name = first_name
        self._last_name = last_name
        self._uname = uname
        self._password = password
        self._type = type
        self._time_stamp = int(time.time())


    def getData(self):
        data = (self._emp_id,self._first_name,self._last_name,self._uname,self._password,self._type,self._time_stamp)
        return data

    @property
    def emp_id(self):
        return self._emp_id

    @emp_id.setter
    def emp_id(self, value):
        self._emp_id = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value


    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def time_stamp(self):
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        self._time_stamp = value

