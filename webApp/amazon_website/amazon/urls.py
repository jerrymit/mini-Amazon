from django.urls import path
from . import views


urlpatterns = [
    # home page
    path('', views.register, name='register'),
    path('home', views.home, name='home'),
    # search page
    path('search_result', views.search_products, name='search_result'),
    path('buy', views.Buy, name='buy'),
    path('add_product', views.add_product, name='add_product'),
    path('add_warehouse', views.add_warehouse, name='add_warehouse'),
    path('cart', views.cart_items, name='cart'),
<<<<<<< HEAD
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    #path('buy_confirmed', views.buy_confirm, name='buy_confirmed'),
    path('Cartbuy', views.Cartbuy, name='Cartbuy'),
    path('Search_product', views.status_search, name='Search_product'),
    #path('Order_Status', views.package_detail, name='Order_Status'),
    path('order_status', views.order_status, name='order_status'),
    #path('Product_status', views.package_status, name='Product_status'),
    
=======
    path('buy_confirmed/<int:order_id>', views.buy_confirm, name='buy_confirmed'),
    path('Cartbuy', views.Cartbuy, name='Cartbuy'),
>>>>>>> master
    #path('home/search_results/order', views.assign_order, name='order'),
]
