import django_filters

from .models import *

class orderFilter(django_filters.FilterSet):
    class Meta:
        model = order
        # fields = '__all__'
        exclude = ['tags']


