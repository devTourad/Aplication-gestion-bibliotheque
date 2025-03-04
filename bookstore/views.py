from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.


from .models import *

from .forms import OrderForm,createNewuser,customerForm

from .filters import orderFilter
from django.forms import inlineformset_factory
from django.contrib import  messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as Mylogin
from django.contrib.auth.decorators import login_required
from .decorators import notLoggedUsers,allowedUsers,forAdmins
from django.contrib.auth.models import Group

import requests
from django.conf import settings

@login_required(login_url='login')
# @allowedUsers( allowedGroups=['ADMIN'])
@forAdmins
def home(request):
     customers = Customer.objects.all()
     orders = order.objects.all()
     t_orders = orders.count()
     p_orders = orders.filter(status='Pending').count()
     d_orders = orders.filter(status='Delivered').count()
     in_orders = orders.filter(status='in progress').count()
     out_orders = orders.filter(status='out of order').count()
     context = {'customers':customers,
                'orders': orders,
                't_orders': t_orders,
                'p_orders': p_orders,
                'd_orders': d_orders,
                'in_orders': in_orders,
                'out_orders': out_orders}
     return render(request,'bookstore/dashbord.html',context)

@login_required(login_url='login')
@forAdmins
def books(request):
    books = Book.objects.all()
    return render(request,'bookstore/books.html',{'books':books})

@login_required(login_url='login')
def customer(request,pk) :
    customer = Customer.objects.get(id=pk)
    orders= customer.order_set.all()
    number_orders = orders.count()
    searchfilter=orderFilter(request.GET , queryset=orders)
    orders = searchfilter.qs
    context = {'customers':customer,
                'orders': orders,
                'number_orders': number_orders,
                'myfilter':searchfilter,}
    return render(request,'bookstore/customer.html',context )

@login_required(login_url='login')
def dashbord(request):
    return render(request,'bookstore/dashbord.html')

# def create(request):
#     form = OrderForm()
#     if request.method == "POST":
#         #print(request.Post)
#         form = OrderForm(request.POST)
#         if form.is_valid():
#              form.save()
#              return redirect('/')
#     context = {'form':form,}
#     return render(request,'bookstore/my_order_form.html',context)

@login_required(login_url='login')
@allowedUsers( allowedGroups=['ADMIN'])
def create(request,pk):
    orderformset =inlineformset_factory(Customer,order,fields=('book','status'),extra=1)
    customer = Customer.objects.get(id=pk)
    formset = orderformset(queryset =order.objects.none() , instance = customer)
    if request.method == "POST":
        formset = orderformset(request.POST,instance = customer)
        if formset.is_valid():
             formset.save()
             return redirect('/')
    context = {'formset':formset,}
    return render(request,'bookstore/my_order_form.html',context)

@login_required(login_url='login')
@allowedUsers( allowedGroups=['ADMIN'])
def update(request,pk):
    orders = order.objects.get(id=pk)
    form = OrderForm(instance = orders)
    if request.method == "POST":
        #print(request.POST)
        form = OrderForm(request.POST,instance = orders)
        if form.is_valid():
             form.save()
             return redirect('/')
    context = {'form':form}
    return render(request,'bookstore/my_order_form.html',context)

@login_required(login_url='login')
@allowedUsers( allowedGroups=['ADMIN'])
def delete(request,pk):
    orders = order.objects.get(id=pk)
    if request.method == "POST":
             orders.delete()
             return redirect('/')
    context = {'Order':orders}
    return render(request,'bookstore/delete_form.html',context)

@notLoggedUsers
def register(request):
        form = createNewuser()
        if request.method == "POST":
                form = createNewuser(request.POST)
                if form.is_valid():
                    # recaptcha_response = request.POST.get('g-recaptcha-response')
                    # data = {
                    #        'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    #        'response' : recaptcha_response
                    #    }
                    # r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                    # result = r.json()
                    # if result['success']:
                        user = form.save()
                        username = form.cleaned_data.get('username')
                        messages.success(request, username + '  Created successfuly !')
                        return redirect('login')
                    # else:
                    #   messages.error(request ,  ' invalid Recaptcha please try again!')
        context = {'form':form}
        return render(request,'bookstore/register.html',context)

@notLoggedUsers

def login(request):
            username = request.POST.get('username' )
            password = request.POST.get('password' )
            user = authenticate(request, username=username ,password=password)
            if user is not None:
                    Mylogin(request,user)
                    return redirect('home')
            else:
                messages.info(request,' ')
            context = {}
            return render(request,'bookstore/login.html',context)

def UserLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowedUsers( allowedGroups=['CUSTOMER'])
def Userprofile(request):
    orders= request.user.customer.order_set.all()
    t_orders = orders.count()
    p_orders = orders.filter(status='Pending').count()
    d_orders = orders.filter(status='Delivered').count()
    in_orders = orders.filter(status='in progress').count()
    out_orders = orders.filter(status='out of order').count()
    context = {
                'orders': orders,
                't_orders': t_orders,
                'p_orders': p_orders,
                'd_orders': d_orders,
                'in_orders': in_orders,
                'out_orders': out_orders}
    return render(request,'bookstore/profile.html',context)



@login_required(login_url='login')
def profileInfo(request):
    customer = request.user.customer
    form = customerForm(instance=customer)
    if request.method == "POST":
         form = customerForm(request.POST , request.FILES, instance=customer)
         if form.is_valid():
             form.save()
    context = {'form': form,
                }
    return render(request,'bookstore/profile_info.html',context)