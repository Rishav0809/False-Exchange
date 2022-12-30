from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Order
from .orders_utility import fetch_all_orders,executable_orders,save_order,execute_order,fetch_user_portfolio,orders_summary,fetch_all_user_orders



def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('loginuser')

#Authentication

def signupuser(request):
    if not request.user.is_authenticated:
        if request.method=='GET':
            return render(request,'user_register.html',{'form':UserCreationForm()})
        else:
            if request.POST['password1']==request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('index')
                except IntegrityError:
                    return render(request, 'user_register.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
            else:
                return render(request, 'user_register.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})
    else:
        return redirect('index')


def loginuser(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'user_login.html', {'form':AuthenticationForm()})
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'user_login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
            else:
                login(request, user)
                return redirect('home')
    else:
        return redirect('index')

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('index')

@login_required
def home(request):
    context=dict()
    context['user_portfolio'],context['total_investment']=fetch_user_portfolio(request.user)
    context['created_orders']=fetch_all_user_orders(request.user)
    context['pending_orders'],context['executed_orders']=orders_summary(request.user)
    return render(request,'home.html',context)






#Placing orders

def placeorder(request):
    if request.method=="POST":
        security_type=request.POST.get('security_type')
        order_type=request.POST.get('order_type')
        price=request.POST.get('price')
        quantity=request.POST.get('quantity')
        status="Pending"
        user=request.user
        order_id=save_order(security_type,order_type,price,quantity,status,user)
        execute_order(order_id,security_type,order_type,price,quantity,status,user)
        return redirect(home)

def flush_database(request):
    Order.objects.all().delete()
    return redirect(createdorders)

def createdorders(request):
    context=dict()
    context['created_orders']=fetch_all_orders(request.user)
    return render(request,'all_orders.html',context)

def viewportfolio(request):
    context=dict()
    context['user_portfolio'],context['']=fetch_user_portfolio(request.user)
    return render(request,'user_portfolio.html',context)

def deleteorder(request):
    if request.method=="POST":
        record=Order.objects.get(pk=request.POST['order_id'])
        record.delete()
        return redirect(home)

def amendorder(request):
    if request.method=="POST":
        record=Order.objects.get(pk=request.POST['order_id'])
        record.quantity=request.POST['quantity']
        record.save()
        return redirect(home)
   




