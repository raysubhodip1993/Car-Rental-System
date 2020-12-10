from __future__ import unicode_literals

from django.db import models
import uuid


# Database files
class AdminStatus(models.Model):
    stat=models.CharField(max_length=1)

    def __str__(self):
        template = ' {0.stat} '
        return template.format(self)

class ActiveUsers(models.Model):
    empid=models.CharField(max_length=100)


    def __str__(self):
        template = ' {0.empid} '
        return template.format(self)

class ActiveCars(models.Model):
    carid=models.CharField(max_length=100)
    uname=models.CharField(max_length=100)
    locktime = models.BigIntegerField()
    lockDuration = models.BigIntegerField()

    def __str__(self):
        template = ' {0.carid} {0.uname} {0.locktime} {0.lockDuration}'
        return template.format(self)

class ActiveCustomer(models.Model):
    custid=models.CharField(max_length=100)
    uname = models.CharField(max_length=100)
    locktime = models.BigIntegerField()
    lockDuration = models.BigIntegerField()


    def __str__(self):
        template = ' {0.custid} {0.uname} {0.locktime} {0.lockDuration}'
        return template.format(self)

class ActiveBookings(models.Model):
    bookingId=models.CharField(max_length=100)
    uname = models.CharField(max_length=100)
    locktime = models.BigIntegerField()
    lockDuration = models.BigIntegerField()


    def __str__(self):
        template = ' {0.bookingId} {0.uname} {0.locktime} {0.lockDuration}'
        return template.format(self)

