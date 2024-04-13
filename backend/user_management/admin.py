from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BaseUser)
admin.site.register(EmployerUser)
admin.site.register(ApplicantUser)