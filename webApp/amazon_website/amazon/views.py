from django.shortcuts import render, redirect, get_object_or_404
#from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from random import choice
from .models import *
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import socket, json, time
#import protobuf_pb2

# Create your views here.

print("Trying to connect to amazon server")
# Try to connect to amazon server until success
amazon_socket = None

HOST = '152.3.53.130'  # The server's hostname or IP address
PORT = 55555        # The port used by the server
address = (HOST, PORT)


def home(request):
    products = Product.objects.all().order_by("id")
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
<<<<<<< HEAD
        products = Commodity.objects.filter(description=query)
=======
        products = Product.objects.filter(description__icontains=query)
>>>>>>> master
    else:
        products = Product.objects.all()
    return render(request, "frontend/search.html", {'products': products, 'query': query})


def add_product(request):
    if request.method == 'POST':
        # Create a new Product object with the form data
        product = Product(
            description=request.POST['description'],
            count=request.POST['count']
        )
        # Save the new Product object to the database
        product.save()
        # Redirect to the home page
        return redirect('home')
    else:
        # Render the form template
        return render(request, 'frontend/add_product.html')
    
def add_warehouse(request):
    if request.method == 'POST':
        warehouse = Warehouse(
            location_x=request.POST['location_x'],
            location_y=request.POST['location_y']
        )
        # Save the new Product object to the database
        warehouse.save()
        # Redirect to the home page
        return redirect('add_warehouse')
    else:
        warehouses = Warehouse.objects.all()
        return render(request, 'frontend/add_warehouse.html', {'warehouses': warehouses})

def view_cart(request):
    cart_items = Cart.objects.all()
    return render(request, 'frontend/cart.html', {'cart_items': cart_items})

def Buy(request):
    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            add_to_cart(request)
            return redirect('buy')
        else:
            user_id = request.session.get('user_id', None)
            # Get the form data from the POST request
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity')
            destination_x = request.POST.get('destination_x')
            destination_y = request.POST.get('destination_y')
            
            # Create a new shipment for the order
            '''
            warehouses = Warehouse.objects.all()
            warehouse = random.choice(warehouses)
            shipment = Shipment.objects.create(
                status = "ordered",
                destination_x=des_x,
                destination_y=des_y,
                warehouse=warehouse,
                #truck=truck  # assign the selected truck to the shipment
            )
            '''
            # Create a new order for the shipment
            product = Product.objects.get(pk=product_id)
            # Check if the requested quantity is valid
            if int(quantity) <= 0 or int(quantity) > product.count:
                messages.error(request, 'Invalid quantity.')
                products = Product.objects.all()
                warehouses = Warehouse.objects.all()
                return render(request, 'frontend/buy.html', {'products': products, 'warehouses': warehouses})
            
            #order = Order.objects.create(product=product, quantity=quantity, shipment=shipment)
            
            # Send data over socket
            data = {
                'destination_x': destination_x,
                'destination_y': destination_y,
                'user_id': user_id,
                'product_id': product_id,
                'description': product.description,
<<<<<<< HEAD
                'quantity': quantity,
            })
            
            orders_data = json.dumps(orders[key])
            product.count -= int(quantity)
            product.save()
            
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
=======
                'count': quantity,
            }
            frontend_request = [data]
            while True:
            # Send the frontend_request to the socket
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect(address)
                    client_socket.sendall(json.dumps(frontend_request).encode())
                    break
                except socket.error:
                    time.sleep(0.5)
                    print('Error: Could not connect to Amazon Server')
                    continue
            client_socket.close()
>>>>>>> master
            # Redirect to a confirmation page
            return render(request, 'frontend/buy_confirmed.html')
            #return redirect('home')
    else:
        # Render the buy form with a list of available products
        products = Product.objects.all()
        warehouses = Warehouse.objects.all()
        return render(request, 'frontend/buy.html', {'products': products, 'warehouses': warehouses})
    
def Cartbuy(request):
    user_id = request.session.get('user_id', None)
    cart = request.session.get('cart', {})
    request.session['purchase_fail'] = {}
    purchase_fail = {}
    orders = {}
    # manipulate the data with user_id
    filtered_cart = {}
    for key, items in cart.items():
        filtered_items = [item for item in items if item['user_id'] == user_id]
        if filtered_items:
            filtered_cart[key] = filtered_items
    
    for key, products in filtered_cart.items():
        destination_x, destination_y = key.split(',')
        orders[key] = []
        #print("key: " + key)
        #print("products: ")
        #print(products)
        orders[key].append({'destination_x': destination_x})
        orders[key].append({'destination_y': destination_y})
<<<<<<< HEAD
        orders[key].append({'user_id': user_id})
        purchase_fail[key] = []
        for product in products:
            flag = 0
            commodity = Commodity.objects.get(description=product['description'])
            if product['quantity'] > commodity.count:
                purchase_fail[key].append({'destination_x': destination_x})
                purchase_fail[key].append({'destination_y': destination_y})
                purchase_fail[key].append({'user_id': user_id})
                purchase_fail[key].append({
                    'product_id': product['product_id'],
                    'description': product['description'],
                    'quantity': product['quantity'],
                })
                print("Quantity exceed the maximum value of the product. Try again!")
                continue
            else:
                commodity.count -= product['quantity']
                commodity.save()
                
                orders[key].append({ # add the order to the list of orders for this key
                'product_id': product['product_id'],
                'description': product['description'],
                'quantity': product['quantity'],
                })
                
        if len(orders[key]) == 3:
            continue
        request.session['purchase_fail'] = purchase_fail
=======
        #orders[key].append({'user_id': user_id})
        '''
        if key not in orders:
            warehouses = Warehouse.objects.all()
            warehouse = random.choice(warehouses)
            shipment = Shipment.objects.create(
                status="ordered",
                destination_x=destination_x,
                destination_y=destination_y,
                warehouse=warehouse,
            )
        '''    
        for product in products:
            orders[key].append({ # add the order to the list of orders for this key
                'product_id': product['product_id'],
                'description': product['description'],
                'quantity': product['quantity'],
            })
        
>>>>>>> master
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
                
        '''
        # create the orders for this package
        shipment = Shipment.objects.get(destination_x=key.split(',')[0], destination_y=key.split(',')[1], status="ordered")
        for order_data in products:
            Order.objects.create(
                user_id=request.user,
                product=Product.objects.get(description=order_data['description']),
                quantity=order_data['quantity'],
                shipment=shipment,
            )
        '''
    '''    
    for key, orders_for_key in orders.items(): # send each package as JSON
        data = {
            'orders': orders_for_key,
            'destination_x': key.split(',')[0],
            'destination_y': key.split(',')[1],
        }
        data_str = json.dumps(data)
        
        # Create a socket and send the JSON string
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(address)
        client_socket.sendall(json.dumps(frontend_request).encode())
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
        s.send(data_str.encode())
        s.close()
        
        # create the orders for this package
        shipment = Shipment.objects.get(destination_x=key.split(',')[0], destination_y=key.split(',')[1], status="ordered")
        for order_data in orders_for_key:
            Order.objects.create(
                user_id=request.user,
                product=Product.objects.get(description=order_data['description']),
                quantity=order_data['quantity'],
                shipment=shipment,
            )
    '''
    # clear the cart and redirect to the confirmation page
    for key, items in cart.items():
        cart[key] = [item for item in items if item['user_id'] != user_id]
    #request.session['cart'] = {}
    return redirect('home')

def add_to_cart(request):
    description = request.POST.get('description')
    quantity = int(request.POST.get('quantity'))
    destination_x = request.POST.get('destination_x')
    destination_y = request.POST.get('destination_y')
<<<<<<< HEAD
    product = Commodity.objects.get(description=description)
    user_id = request.session.get('user_id', None)
    # Get the product from the database
    available_quantity = product.count
    
    # Check if the requested quantity is available
    if quantity < 0 or quantity > available_quantity:
        # Show an error message to the user
        error_message = f"Only {available_quantity} units of {description} are available. Try again!"
        return error_message
=======
    product = Product.objects.get(description=description)
    product_id = product.id
>>>>>>> master
    # Add product to cart
    cart = request.session.get('cart', {})
    
    key = f"{destination_x},{destination_y}"
    if key in cart:
        flag = 0
        for item in cart[key]:
            print("item: ", item)
<<<<<<< HEAD
            if item['description'] == description and item['user_id'] == user_id:
                total = item['quantity'] + quantity
                if total > available_quantity:
                    # Show an error message to the user
                    error_message = f"Exceed the maximum number of {description}."
                    print("ERROR MESSAGE2: ", error_message)
                    return error_message
=======
            if item['description'] == description:
>>>>>>> master
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
            'user_id':user_id,
        })
    else:
        cart[key] = [{
            'product_id': product_id,
            'description': description,
            'quantity': quantity,
            'destination_x':destination_x,
            'destination_y':destination_y,
            'user_id':user_id,
        }]
    
    request.session['cart'] = cart
    #request.session.clear()

def cart_items(request):
    user_id = request.session.get('user_id', None)
    cart = request.session.get('cart', {})
    filtered_cart = {}
    
    for key, items in cart.items():
        filtered_items = [item for item in items if item['user_id'] == user_id]
        if filtered_items:
            filtered_cart[key] = filtered_items

    print(filtered_cart)
    items = []
    for key, product_items in filtered_cart.items():
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

<<<<<<< HEAD
# not use
def status_search(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        package = Package.objects.filter(package_id)
        print("into status_search")
        if package is not None:
            status = package.status
            print("search success")
            return render(request, 'frontend/package_status.html', {'package': package})
=======
def buy_confirm(request, order_id):
    # Get the order details from the database
    order = Order.objects.get(pk=order_id)

    # Render the confirmation page
    return render(request, 'frontend/buy_confirmed.html', {'order': order})

'''
def Buy(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        description = request.POST['product_name']
        quantity = int(request.POST['quantity'])
        warehouse_id = int(request.POST['warehouse_id'])

        # Check if the product exists
        product, created = Product.objects.get_or_create(
            product_id=product_id,
            defaults={'description': description},
        )

        if not created and product.description != description:
            return JsonResponse({'error': 'Product description does not match existing product.'})

        # Find the warehouse
        try:
            warehouse = Warehouse.objects.get(warehouse_id=warehouse_id)
        except Warehouse.DoesNotExist:
            return JsonResponse({'error': 'Warehouse not found.'})

        # Update the inventory
        package, _ = Order.objects.get_or_create(
            shipment=None,
            product=product,
            warehouse=warehouse,
            defaults={'quantity': quantity},
        )

        if not created:
            package.quantity += quantity
            package.save()

        return JsonResponse({'success': 'Products purchased and added to warehouse inventory.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})
'''    
def pack_shipment(request):
    if request.method == 'POST':
        warehouse_id = int(request.POST['warehouse_id'])
        product_id = int(request.POST['product_id'])
        quantity = int(request.POST['quantity'])
        destination_x = int(request.POST['destination_x'])
        destination_y = int(request.POST['destination_y'])

        # Find the warehouse
        try:
            warehouse = Warehouse.objects.get(warehouse_id=warehouse_id)
        except Warehouse.DoesNotExist:
            return JsonResponse({'error': 'Warehouse not found.'})

        # Find the product
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'})

        # Check if there's enough inventory
        package = Order.objects.filter(shipment=None, product=product, warehouse=warehouse).first()

        if not package or package.quantity < quantity:
            return JsonResponse({'error': 'Not enough inventory in the warehouse.'})

        # Create a new shipment
        shipment = Shipment.objects.create(
            warehouse=warehouse,
            destination_x=destination_x,
            destination_y=destination_y,
            status='packing',
        )

        # Update the warehouse package
        package.quantity -= quantity
        if package.quantity == 0:
            package.delete()
>>>>>>> master
        else:
            package.save()

        # Create a new package for the shipment
        Order.objects.create(
            shipment=shipment,
            product=product,
            quantity=quantity,
        )

        # Simulate packing process (use background tasks like Celery in real application)
        import time
        time.sleep(5)
        shipment.status = 'packed'
        shipment.save()

        return JsonResponse({'success': 'Shipment packed.', 'shipment_id': shipment.shipment_id})
    else:
<<<<<<< HEAD
        return render(request, 'frontend/status_search.html')

# not use
def package_detail(request):
    # Get the package_id parameter from the request.GET dictionary
    package_id = request.GET.get('package_id')

    # Get the user ID from the session
    user = request.session.get('user_id')
    # Get the order that matches the given package_id
    orders = Order.objects.filter(package_id=package_id, package__user_id=user)

    if not orders.exists():
        # If no order is found, render a message indicating so
        error_message = f"No order found for package ID {package_id}."
        return render(request, 'frontend/package_status.html', {'error_message':error_message})

    # If an order is found, render the package status information
    return render(request, 'frontend/package_status.html', {'orders': orders})

def order_status(request):
    user_id = request.session.get('user_id', None)
    packages = Package.objects.filter(user_id=user_id)
    orders = []
    for package in packages:
        package_orders = Order.objects.filter(package=package)
        orders += list(package_orders)
    return render(request, 'frontend/order_status.html', {'orders': orders})
    
=======
        return JsonResponse({'error': 'Invalid request method.'})
    
def load_shipment(request):
    if request.method == 'POST':
        shipment_id = int(request.POST['shipment_id'])
        truck_id = int(request.POST['truck_id'])

        # Find the shipment
        try:
            shipment = Shipment.objects.get(shipment_id=shipment_id)
        except Shipment.DoesNotExist:
            return JsonResponse({'error': 'Shipment not found.'})

        # Check if the shipment is packed
        if shipment.status != 'packed':
            return JsonResponse({'error': 'Shipment must be packed before loading.'})

        # Check if the truck is at the warehouse and ready to receive the shipment
        #truck_ready = check_truck_ready(truck_id, shipment.warehouse_id)

        #if not truck_ready:
            #return JsonResponse({'error': 'Truck is not at the warehouse or not ready to receive the shipment.'})

        # Simulate loading process (use background tasks like Celery in real application)
        import time
        time.sleep(5)

        # Update the shipment status
        shipment.status = 'loaded'
        shipment.save()

        return JsonResponse({'success': 'Shipment loaded onto the truck.', 'shipment_id': shipment.shipment_id})
    else:
        return JsonResponse({'error': 'Invalid request method.'})

def query_package_status(request):
    if request.method == 'GET':
        package_id = int(request.GET['package_id'])

        # Find the package
        try:
            package = Order.objects.get(package_id=package_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Package not found.'})

        # Get the shipment status
        status = package.shipment.status

        return JsonResponse({'package_id': package.package_id, 'status': status})
    else:
        return JsonResponse({'error': 'Invalid request method.'})
>>>>>>> master
