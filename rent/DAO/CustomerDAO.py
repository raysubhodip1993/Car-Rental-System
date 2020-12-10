from rent.DAO import BaseDAO
from rent.DAO import sqlUtility
from rent import Utility

def getAllCustomers():
    baseDao = BaseDAO.DbConnection()
    results = baseDao.getAllRecords(sqlUtility.CUSTOMER_DB_NAME)

    print("All Customers")
    print(results)
    return results

def getCustomerByDLN(dln):
    baseDao = BaseDAO.DbConnection()
    customers = baseDao.getRecord(sqlUtility.CUSTOMER_DB_NAME,sqlUtility.CUSTOMER_DRIVING_LICENSE,dln)

    print("customer")
    print(customers)
    return customers

def updateCustomer(customer):
    baseDao = BaseDAO.DbConnection()
    data = customer.getData() + (customer.driving_license,)
    result = baseDao.updateRecord(sqlUtility.UPDATE_QUERY_CUSTOMER_DB,data)

    print("customer")
    print(customer)
    return result

def addCustomer(customer):
    baseDao = BaseDAO.DbConnection()
    item= "cust"
    customer = baseDao.addRecord(sqlUtility.INSERT_QUERY_CUSTOMER_DB,customer,sqlUtility.CUSTOMER_DB_NAME,item)
    print("customer")
    print(customer)
    return customer

def deleteCustomer(dln):
    baseDao = BaseDAO.DbConnection()
    customer = baseDao.deleteRecord(sqlUtility.DELETE_QUERY_CUSTOMER_DB,dln)

    print("customer")
    print(customer)
    return customer


