from django.db.models.signals import post_save
from .models import Customer
# from django.contrib import admin
from django.contrib.auth.models import User,Group
# Register your models here.

def Customer_create_profile(sender, instance,created,**kwargs,):
    if created:
        group = Group.objects.get( name = "CUSTOMER")
        instance.groups.add(group)
        Customer.objects.create(
                user= instance,
                name=instance.username
    )
    print('Customer  profile created ')
post_save.connect(Customer_create_profile,sender=User)
# from .models import *

# admin.site.register(Customer)

# admin.site.register(Book)

# admin.site.register(Order)
# admin.site.register(Tag)