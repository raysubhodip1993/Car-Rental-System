from django.contrib import admin
from .models import ActiveCustomer,ActiveCars,ActiveUsers,AdminStatus

# Register your models here.
admin.site.register(AdminStatus)
admin.site.register(ActiveUsers)
admin.site.register(ActiveCars)
admin.site.register(ActiveCustomer)

# admin.site.re
