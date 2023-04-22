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
PORT = 55555        # The port used by the server
address = (HOST, PORT)


commodities = [
    ('apple', 20),
    ('book', 20),
    ('cat', 15),
    ('dog', 10),
    ('banana', 30),
    ('cloth', 30),
    ('shoes', 50),
    ('kimchi', 100),
    ('TV', 40),
    ('coach', 30),
    ('ball', 25),
    ('beef noodle', 10),
]

for description, count in commodities:
    obj, created = Commodity.objects.get_or_create(description=description, defaults={'count': count})
    
products = [
    ('apple'),
    ('book'),
    ('cat'),
    ('dog'),
    ('banana'),
    ('cloth'),
    ('shoes'),
    ('kimchi'),
    ('TV'),
    ('coach'),
    ('ball'),
    ('beef noodle'),
]

for description in products:
    obj, created = Product.objects.get_or_create(description=description)



def home(request):
    products = Commodity.objects.all().order_by("id")
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

def clear_cart(request):
    request.session['cart'] = {}
    return render(request, 'frontend/clear_cart.html')

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
            product = Commodity.objects.get(pk=product_id)
            # Check if the requested quantity is valid
            if int(quantity) <= 0 or int(quantity) > product.count:
                messages.error(request, 'Invalid quantity.')
                products = Commodity.objects.all()
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
        #print("key: " + key)
        #print("products: ")
        #print(products)
        orders[key].append({'destination_x': destination_x})
        orders[key].append({'destination_y': destination_y})
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
    request.session['cart'] = {}
    return redirect('home')

def add_to_cart(request):
    description = request.POST.get('description')
    quantity = int(request.POST.get('quantity'))
    destination_x = request.POST.get('destination_x')
    destination_y = request.POST.get('destination_y')
    product = Commodity.objects.get(description=description)
    
    # Get the product from the database
    available_quantity = int(product.count)
    
    # Check if the requested quantity is available
    if quantity < 0 or quantity > available_quantity:
        # Show an error message to the user
        error_message = request.session.get('error_message', None)
        error_message = f"Only {available_quantity} units of {description} are available"
        print("ERROR MESSAGE1: ", error_message)
        return render(request, 'frontend/buy.html', {'error_message': error_message})
    # Add product to cart
    product_id = product.id
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
'''
'''
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
'''