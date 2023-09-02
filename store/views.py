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
import datetime
from .models import Product
from .models import Customer
from .models import Order, ShippingAddress
from django.contrib.auth.models import AnonymousUser
from .form import ProductSearchForm  
from .models import Product 
from django.template import TemplateDoesNotExist
import logging
from django.db import transaction 
from .models import Promotion
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Product, OrderItem, Customer, Order


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
@transaction.atomic  # Wrap the store view in a transaction
def store(request):
    customer, created = Customer.objects.get_or_create(user=request.user)

    # Check if an incomplete order exists for the customer
    try:
        order = Order.objects.get(customer=customer, complete=False)
    except Order.DoesNotExist:
        order = None

    if order and not order.complete:
        # An incomplete order exists; continue using it
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create a new order only if there's no incomplete order
        if order is None:
            order = Order.objects.create(customer=customer, complete=False)
        items = []
        cartItems = 0  # Initialize cartItems as 0

    # Retrieve promotions from the database
    promotions = Promotion.objects.all()

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'promotions': promotions}
    return render(request, 'store/Store.html', context)



def cart(request):
    order = None  # Initialize order with None when the user is not authenticated
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []

    cartItems = order.get_cart_items if order else 0  # Use the get_cart_items property
    cartTotal = order.get_cart_total if order else 0  # Use the get_cart_total property

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'cartTotal': cartTotal, 'shipping': False}
    return render(request, 'store/Cart.html', context)


def Checkout(request):
    context = {}  # Initialize the context dictionary

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items  # Use the get_cart_items property
        cartTotal = order.get_cart_total  # Use the get_cart_total property
    else:
        items = []
        cartItems = 0  # Initialize cartItems as 0 when the user is not authenticated
        cartTotal = 0  # Initialize cartTotal as 0 when the user is not authenticated
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}

    context.update({'items': items, 'order': order, 'cartItems': cartItems, 'cartTotal': cartTotal})

    return render(request, 'store/Checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer, created = Customer.objects.get_or_create(user=request.user)

    try:
        product = Product.objects.get(id=productId)
    except Product.DoesNotExist:
        # Handle the case where the product doesn't exist
        return JsonResponse({'message': 'Product does not exist'}, status=400)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # Use filter to get the OrderItem if it exists
    orderItem_qs = OrderItem.objects.filter(order_ref=order, product=product)

    if orderItem_qs.exists():
        orderItem = orderItem_qs.first()
    else:
        # If it doesn't exist, create a new one
        orderItem = OrderItem(order_ref=order, product=product, quantity=0)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    # Save the updated quantity
    orderItem.save()

    # If the quantity becomes zero or negative, delete the item
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({'message': 'Item was updated'}, safe=False)





def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        # For not-logged-in users, create a new customer instance
        customer, _ = Customer.objects.get_or_create(user=None)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    total_str = data['form']['total']
    
    # Check if the total_str is not empty before converting to float
    if total_str:
        total = float(total_str)
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):

            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
            print('Shipping details saved to the database.')
        else:
            print('No shipping details provided.')

    else:
        print('Total not provided in the data.')

    return JsonResponse('Payment complete!', safe=False)


def productSearch(request):
    form = ProductSearchForm(request.GET)
    results = None
    cartItems = 0  # Initialize cartItems as 0
    cartTotal = 0  # Initialize cartTotal as 0

    if request.method == 'GET':
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            results = Product.objects.filter(name__icontains=search_query)

    try:
        # Calculate the cart items and cart total
        if request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(user=request.user)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items  # Use the get_cart_items property
            cartTotal = order.get_cart_total  # Use the get_cart_total property
        else:
            items = []

        # Pass context to the template
        context = {
            'results': results,
            'form': form,
            'cartItems': cartItems,
            'cartTotal': cartTotal,
        }

        if results:
            return render(request, 'store/search_results.html', context)
        else:
            return render(request, 'store/search_no_results.html', context)

    except TemplateDoesNotExist as e:
        # Log the error and return a custom error response
        logger.error(f"TemplateDoesNotExist error: {e}")
        return HttpResponse("An error occurred while rendering the template.", status=500)

def promotion_view(request):
    current_date = timezone.now()
    promotions = Promotion.objects.all()
    
    # Include start_date and end_date in the context
    context = {
        'promotions': promotions,
        'start_date': current_date,  # Replace with the actual start date
        'end_date': current_date,    # Replace with the actual end date
    }



def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_total = 0
    cart_items = 0

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all()
        cart_total = order.get_cart_total
        cart_items = order.get_cart_items

    context = {'product': product, 'cart_total': cart_total, 'cart_items': cart_items}
    return render(request, 'store/product_detail.html', context)