from django.urls import path
from . import views


urlpatterns = [
    # home page
    path('', views.home, name='home'),
    # search page
    path('search_result', views.search_products, name='search_result'),
    path('buy', views.Buy, name='buy'),
    path('add_product', views.add_product, name='add_product'),
    path('add_warehouse', views.add_warehouse, name='add_warehouse'),
    path('cart', views.cart_items, name='cart'),
    path('buy_confirmed/<int:order_id>', views.buy_confirm, name='buy_confirmed'),
    #path('home/search_results/order', views.assign_order, name='order'),
]
