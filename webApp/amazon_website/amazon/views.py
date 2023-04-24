from django.shortcuts import render, redirect, get_object_or_404
#from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from random import choice
from .models import *
import socket, json, time
#import protobuf_pb2

# Create your views here.

print("Trying to connect to amazon server")
# Try to connect to amazon server until success
amazon_socket = None

HOST = '152.3.53.130'  # The server's hostname or IP address
#HOST = '152.3.53.130'  # The server's hostname or IP address james
PORT = 55555        # The port used by the server
address = (HOST, PORT)



def home(request):
    products = Commodity.objects.all().order_by("commodity_id")
    warehouses = Warehouse.objects.all().order_by("warehouse_id")
    context = {"products": products, "warehouses": warehouses}
    return render(request, "frontend/home.html",context)

def register(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id') # assuming 'user_id' is the name of the input field in the registration form
        request.session['user_id'] = user_id
        print("userID:", user_id)
        return redirect('home')
    else:
        #return redirect('home')
        return render(request, "frontend/register.html")

def search_products(request):
    query = request.GET.get('search_input')
    if query:
        products = Commodity.objects.filter(description__icontains=query)
    else:
        products = Commodity.objects.all()
    return render(request, "frontend/search.html", {'products': products, 'query': query})

def clear_cart(request):
    request.session['cart'] = {}
    return render(request, 'frontend/clear_cart.html')

def Buy(request):
    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            products = Commodity.objects.all()
            warehouses = Warehouse.objects.all()
            error_message = add_to_cart(request)
            return render(request, "frontend/buy.html", {'products':products,'warehouses':warehouses, 'error_message':error_message})
        else:
            user_id = request.session.get('user_id', None)
            # Get the form data from the POST request
            description = request.POST.get('description')
            quantity = request.POST.get('quantity')
            destination_x = request.POST.get('destination_x')
            destination_y = request.POST.get('destination_y')
            
            product = Commodity.objects.get(description=description)
            product_id = product.commodity_id
            # Check if the requested quantity is valid
            if int(quantity) <= 0 or int(quantity) > product.count:
                error_message = f"Only {product.count} units of {description} are available. Try again!"
                products = Commodity.objects.all()
                warehouses = Warehouse.objects.all()
                return render(request, 'frontend/buy.html', {'products': products, 'warehouses': warehouses})
            
            # Send data over socket
            orders = {}
            key = f"{destination_x},{destination_y}"
            orders[key] = []
            orders[key].append({'destination_x': destination_x})
            orders[key].append({'destination_y': destination_y})
            orders[key].append({'user_id': user_id})
            # add the product
            orders[key].append({ 
                'product_id': product_id,
                'description': product.description,
                'quantity': quantity,
            })
            orders_data = json.dumps(orders[key])
            connected = False
            while not connected:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect(address)
                    client_socket.sendall(orders_data.encode())
                    client_socket.close()
                    connected = True
                    product.count -= int(quantity)
                    product.save()
                except:
                    print("waiting for the world to be ready")
            # Redirect to a confirmation page
            #return redirect('buy_confirmed', order_id=order.pk)
            return redirect('home')
    else:
        # Render the buy form with a list of available products
        products = Commodity.objects.all()
        warehouses = Warehouse.objects.all()
        return render(request, 'frontend/buy.html', {'products': products, 'warehouses': warehouses})
    
def Cartbuy(request):
    user_id = request.session.get('user_id', None)
    cart = request.session.get('cart', {})
    orders = {}
    
    for key, products in cart.items():
        destination_x, destination_y = key.split(',')
        orders[key] = []
        orders[key].append({'destination_x': destination_x})
        orders[key].append({'destination_y': destination_y})
        orders[key].append({'user_id': user_id})
  
        for product in products:
            commodity = Commodity.objects.get(description=product['description'])
            if product['quantity'] > commodity.count:
                print("Quantity exceed the maximum value of the product.")
                continue
            orders[key].append({ # add the order to the list of orders for this key
                'product_id': product['product_id'],
                'description': product['description'],
                'quantity': product['quantity'],
            })
            
        print("orders[key] value: ")
        print(orders[key])
        # serialize the orders data to JSON format
        orders_data = json.dumps(orders[key])
        connected = False
        while not connected:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(address)
                client_socket.sendall(orders_data.encode())
                client_socket.close()
                connected = True
                
            except:
                print("waiting for the world to be ready")
    # clear the cart and redirect to the confirmation page
    request.session['cart'] = {}
    return redirect('home')

def add_to_cart(request):
    description = request.POST.get('description')
    quantity = int(request.POST.get('quantity'))
    destination_x = request.POST.get('destination_x')
    destination_y = request.POST.get('destination_y')
    product = Commodity.objects.get(description=description)
    
    # Get the product from the database
    available_quantity = product.count
    
    # Check if the requested quantity is available
    if quantity < 0 or quantity > available_quantity:
        # Show an error message to the user
        error_message = f"Only {available_quantity} units of {description} are available. Try again!"
        return error_message
    # Add product to cart
    product_id = product.commodity_id
    cart = request.session.get('cart', {})
    key = f"{destination_x},{destination_y}"
    if key in cart:
        flag = 0
        for item in cart[key]:
            print("item: ", item)
            if item['description'] == description:
                total = item['quantity'] + quantity
                if total > available_quantity:
                    # Show an error message to the user
                    error_message = f"Only {total - item['quantity']} units of {description} are available"
                    print("ERROR MESSAGE2: ", error_message)
                    return render(request, 'frontend/buy.html', {'error_message': error_message})
                item['quantity'] += quantity
                flag = 1
                break   
        if flag == 0:
            cart[key].append({
            'product_id': product_id,
            'description': description,
            'quantity': quantity,
            'destination_x':destination_x,
            'destination_y':destination_y,
        })
    else:
        cart[key] = [{
            'product_id': product_id,
            'description': description,
            'quantity': quantity,
            'destination_x':destination_x,
            'destination_y':destination_y,
        }]

    request.session['cart'] = cart
    #request.session.clear()

def cart_items(request):
    cart = request.session.get('cart', {})
    items = []
    for key, product_items in cart.items():
        destination_x, destination_y = key.split(',')
        print("item_key:", key)
        print("item_value:", product_items)
        for item in product_items:
            items.append({
                #'product': product,
                'description': item['description'],
                'quantity': item['quantity'],
                'destination_x': destination_x,
                'destination_y': destination_y,
            })
    context = {'items': items}
    return render(request, 'frontend/cart_items.html', context)

def buy_confirm(request, order_id):
    # Get the order details from the database
    order = Order.objects.get(pk=order_id)

    # Render the confirmation page
    return render(request, 'frontend/buy_confirmed.html', {'order': order})

def status_search(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        package = Package.objects.filter(package_id)
        if package is not None:
            status = package.status
            return render(request, 'frontend/package_status.html', {'package': package})
        else:
            status = f"No package found for package_id '{package_id}'"
            return render(request, 'frontend/package_status.html', {'status': status})
    else:
        return render(request, 'frontend/status_search.html')
    
def package_detail(request, package_id):
    order = Order.objects.filter(package_id)
    context = {'order': order}
    return render(request, 'package_status.html', context)
    