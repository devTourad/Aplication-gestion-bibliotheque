from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(order)
admin.site.register(Tag)