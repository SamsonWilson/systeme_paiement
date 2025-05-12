from django.contrib import admin

from .models import CustomUser, Maison, UserType, Ville

# Register your models here.
admin.site.register(UserType)
admin.site.register(CustomUser)
admin.site.register(Ville)
admin.site.register(Maison)



