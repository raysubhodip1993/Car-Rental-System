from rent.DAO import employeeDAO
from rent.DAO import BaseDAO
from rent.DAO import sqlUtility
import random
from rent.Entity import Employee


def getAllEmployees():
    employeeObjects = employeeDAO.getAllEmployees()

    print("All Employees")
    print(employeeObjects)
    return employeeObjects


def getEmplyeeById(empId):
    employee = employeeDAO.getEmpById(empId)

    print("Employee Data")

    print(employee)

    return employee


def getEmployeeByUserName(username):
    baseDao = BaseDAO.DbConnection()
    employee = baseDao.getRecord(sqlUtility.EMPLOYEE_DB_NAME, sqlUtility.EMPLOYEE_USER_NAME, username)

    print("Employee Data")
    # print(results)

    # employee = Utility.json2obj(result)
    print("Employee")
    # print(type(employee['password']))

    return employee

def getEmployeeByID(uid):
    baseDao = BaseDAO.DbConnection()
    employee = baseDao.getRecord(sqlUtility.EMPLOYEE_DB_NAME, sqlUtility.EMPLOYEE_ID, uid)

    print("Employee Data")
    # print(results)

    # employee = Utility.json2obj(result)
    print("Employee")
    # print(type(employee['password']))

    return employee



def saveEmployeeDetails(request):
    baseDao = BaseDAO.DbConnection()
    emp_id = random.randint(1, 999)
    employee = Employee.Clerk(emp_id,
                              request.POST.get(sqlUtility.CUSTOMER_FIRST_NAME),
                              request.POST.get(sqlUtility.EMPLOYEE_LAST_NAME),
                              request.POST.get(sqlUtility.EMPLOYEE_USER_NAME),
                              request.POST.get(sqlUtility.EMPLOYEE_PASSWORD), request.POST.get(sqlUtility.EMPLOYEE_TYPE)
                              )
    employeeDAO.saveEmpDetails(employee)
    return employee


def deletEmployee(empId):
    baseDao = BaseDAO.DbConnection()
    employeeDAO.deletEmployee(empId)


def updateEmpDetails(request):
    employee = Employee.Clerk(request.POST.get(sqlUtility.EMPLOYEE_ID),
                              request.POST.get(sqlUtility.CUSTOMER_FIRST_NAME),
                              request.POST.get(sqlUtility.EMPLOYEE_LAST_NAME),
                              request.POST.get(sqlUtility.EMPLOYEE_USER_NAME),
                              request.POST.get(sqlUtility.EMPLOYEE_PASSWORD), request.POST.get(sqlUtility.EMPLOYEE_TYPE)
                              )
    oldObj = employeeDAO.getEmpById(employee.emp_id)
    result= {}
    if oldObj[sqlUtility.TIME_STAMP] > employee.time_stamp:
        alert('Employee already modified by other admin')
        result['updated'] = False
        return result
    else:
        employeeDAO.updateEmpDetails(employee)
        result['updated'] = True
        return result

