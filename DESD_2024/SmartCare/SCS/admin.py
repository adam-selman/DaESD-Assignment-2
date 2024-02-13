from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, ContactInfo, Addresse, Appointment, Invoice

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(ContactInfo)
admin.site.register(Addresse)
admin.site.register(Appointment)
admin.site.register(Invoice)
