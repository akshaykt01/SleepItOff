from django.contrib import admin
from .models import *


admin.site.register(user)
admin.site.register(warden)
admin.site.register(hostel)
admin.site.register(Room)
admin.site.register(Bed)
admin.site.register(Contact)
admin.site.register(Booking)
admin.site.register(PasswordReset)
admin.site.register(Booking_Archive)
