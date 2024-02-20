from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, ContactInfo, Address, Appointment, Invoice

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(ContactInfo)
admin.site.register(Address)
admin.site.register(Appointment)
admin.site.register(Invoice)
