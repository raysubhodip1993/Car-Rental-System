from rent.DAO import CustomerDAO
from rent.DAO import BaseDAO
from rent.DAO import sqlUtility
from rent.Entity import Customer
from rent import Utility
import random


def getAllCustomers():
    baseDao = BaseDAO.DbConnection()
    customers = CustomerDAO.getAllCustomers()
    print("All Customers")
    print(customers)
    return customers


# FETCH CUSTOMER WITH NEXT AND PREVIOUS CUSTOMER DLN
def fetchCustomer(drivingLicense):
    custObjects = getAllCustomers()
    currentCust = {}
    nextCustomerDln = ""
    previousCustomerDln = ""
    customerData = {}
    test = False
    for index, customer in enumerate(custObjects):
        if (drivingLicense == customer['driving_license']):
            print('customer')
            print(customer)
            currentCust = customer
            if (index > 0):
                previousCustomerDln = custObjects[index - 1]['driving_license']
            else:
                previousCustomerDln = custObjects[len(custObjects) - 1]['driving_license']
            if (index < (len(custObjects) - 1)):
                nextCustomerDln = custObjects[index + 1]['driving_license']
            else:
                nextCustomerDln = custObjects[0]['driving_license']
    if not currentCust:
        print('no customer with license No ' + str(drivingLicense))
        customerData['currentCustomer'] = {}
        customerData['nextCustomer'] = {}
        customerData['previousCustomer'] = {}
    else:
        customerData['currentCustomer'] = currentCust
        customerData['nextCustomer'] = nextCustomerDln
        customerData['previousCustomer'] = previousCustomerDln
    return customerData


# GET SINGLE CUSTOMER OBJECT
def getCustomer(dln):
    customer = CustomerDAO.getCustomerByDLN(dln)
    print("customer Data")
    print(customer)
    return customer


def addCustDetails(request):
    customer = Customer.Customer(
        request.POST.get(sqlUtility.CUSTOMER_FIRST_NAME),
        request.POST.get(sqlUtility.CUSTOMER_LAST_NAME),
        request.POST.get(sqlUtility.CUSTOMER_DRIVING_LICENSE),
        request.POST.get(sqlUtility.CUSTOMER_LICENSE_EXPIRY), request.POST.get(sqlUtility.CUSTOMER_PHONE_NO)
    )
    CustomerDAO.addCustomer(customer)
    return customer


def deletCustomer(dln):
    CustomerDAO.deleteCustomer(dln)


def updateCustDetails(request):
    #request.POST.get(sqlUtility.EMPLOYEE_ID),
    customer = Customer.Customer(request.POST.get(sqlUtility.CUSTOMER_FIRST_NAME),
                                 request.POST.get(sqlUtility.CUSTOMER_LAST_NAME),
                                 request.POST.get(sqlUtility.CUSTOMER_DRIVING_LICENSE),
                                 request.POST.get(sqlUtility.CUSTOMER_LICENSE_EXPIRY),
                                 request.POST.get(sqlUtility.CUSTOMER_PHONE_NO))
    oldObj = CustomerDAO.getCustomerByDLN(customer.driving_license)
    if oldObj[sqlUtility.TIME_STAMP] > customer.time_stamp:
        alert('Customer already modified by other clerk')
        result['updated'] = False
        return result
    else:
        result = CustomerDAO.updateCustomer(customer)
        result['updated'] = True
        return result
