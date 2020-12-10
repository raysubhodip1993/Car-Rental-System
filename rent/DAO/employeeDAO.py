from rent.DAO import BaseDAO
from rent.DAO import sqlUtility
from rent import Utility

def getAllEmployees():
    baseDao = BaseDAO.DbConnection()
    results = baseDao.getAllRecords(sqlUtility.EMPLOYEE_DB_NAME)
    employeeObjects = []
    for row in results:
        print(row)
        employeeObjects.append(row)

    print("All Employees")
    print(employeeObjects)
    return employeeObjects


def getEmpById(empId):
    baseDao = BaseDAO.DbConnection()
    result = baseDao.getRecord(sqlUtility.EMPLOYEE_DB_NAME, sqlUtility.EMPLOYEE_ID, empId)

    print("Employee Data")
    print(result)

    employee = result
    print("Employee")
    print(employee)

    return employee


def saveEmpDetails(employee):
    baseDao = BaseDAO.DbConnection()
    item="emp"
    baseDao.addRecord(sqlUtility.INSERT_QUERY_EMPLOYEE_DB,employee,sqlUtility.EMPLOYEE_DB_NAME,item)


def deletEmployee(empId):
    baseDao = BaseDAO.DbConnection()
    baseDao.deleteRecord(sqlUtility.DELETE_QUERY_EMPLOYEE_DB, empId)


def updateEmpDetails(employee):
    baseDao = BaseDAO.DbConnection()
    data = employee.getData()
    data = data + (employee.emp_id,)
    return baseDao.updateRecord(sqlUtility.UPDATE_QUERY_EMPLOYEE_DB, data)
