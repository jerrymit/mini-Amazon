from django.shortcuts import render, redirect
#from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from random import choice
from .models import *
# Create your views here.

def home(request):
    products = Product.objects.all().order_by("id")
    warehouses = Warehouse.objects.all().order_by("warehouse_id")
    context = {"products": products, "warehouses": warehouses}
    return render(request, "frontend/home.html",context)

def search_products(request):
    query = request.GET.get('search_input')
    if query:
        products = Product.objects.filter(description__icontains=query)
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

def Buy(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        des_x = request.POST.get('destination_x')
        des_y = request.POST.get('destination_y')
        
        # Create a new shipment for the order
        warehouses = Warehouse.objects.all()
        warehouse = random.choice(warehouses)
        shipment = Shipment.objects.create(
            status = "ordered",
            destination_x=des_x,
            destination_y=des_y,
            warehouse=warehouse,
            #truck=truck  # assign the selected truck to the shipment
        )
        # Create a new order for the shipment
        product = Product.objects.get(pk=product_id)
        # Check if the requested quantity is valid
        if int(quantity) <= 0 or int(quantity) > product.count:
            messages.error(request, 'Invalid quantity.')
            products = Product.objects.all()
            warehouses = Warehouse.objects.all()
            return render(request, 'frontend/buy.html', {'products': products, 'warehouses': warehouses})
        
        order = Order.objects.create(product=product, quantity=quantity, shipment=shipment)

            # Redirect to a confirmation page
        return redirect('buy_confirmed', order_id=order.pk)

    else:
        # Render the buy form with a list of available products
        products = Product.objects.all()
        warehouses = Warehouse.objects.all()
        return render(request, 'frontend/buy.html', {'products': products, 'warehouses': warehouses})

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