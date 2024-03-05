from django.contrib import admin

# Register your models here.
from charity_app.models import (Category, Institution, Donation, User)
admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
admin.site.register(User)

