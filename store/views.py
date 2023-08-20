from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .form import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
import json
from .models import Customer

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance

            # Create a Customer instance and link it to the user
            customer = Customer.objects.create(user=user)
            customer.name = form.cleaned_data.get('username')  # Assuming username is used as the customer name

            customer.save()

            messages.success(request, 'Account was created for ' + user.username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'store/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Retrieve the 'username' value from POST data
        password = request.POST.get('password')  # Retrieve the 'password' value from POST data

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'username OR password is incorrect.....!')
        
    context = {}
    return render(request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items  # Use the get_cart_items property

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItem = order['get_cart_items']  # This line can be removed

    context = {'items': items, 'order': order}

    products = Product.objects.all()
    context['products'] = products  # Update the 'products' key in the context
    return render(request, 'store/Store.html', context)




def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
    context = {'items': items, 'order' : order}
    return render(request, 'store/Cart.html', context)

def Checkout(request):
 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
    context = {'items': items, 'order' : order}
    return render(request, 'store/Checkout.html', context)
    

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    # Assuming 'order_ref' is the correct ForeignKey field in your OrderItem model
    orderItem, created = OrderItem.objects.get_or_create(order_ref__customer=customer, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)