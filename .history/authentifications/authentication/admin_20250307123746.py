from django.contrib import admin

from .models import CustomUser, UserType, Ville

# Register your models here.
admin.site.register(UserType)
admin.site.register(CustomUser)
admin.site.register(Ville)
admin.site.register(maiso)



