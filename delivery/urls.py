from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication paths
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('index/', views.index, name='index'),
    path('signin/index/', views.index, name='signin_index'),
    path('signup/index/', views.index, name='signup_index'),
    path('signup/index/signin/', views.signin, name='signup_signin'),
    path('signin/index/signup/', views.signup, name='signin_signup'),
    path('handle_login/', views.handle_login, name='handle_login'),
    path('handle_register/', views.handle_register, name='handle_register'),
    
    # Restaurant management paths
    path('handle_login/restaurant_page/', views.restaurant_page, name='restaurant_page'),
    path('handle_login/add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('handle_login/show_restaurant_page/',views.show_restaurant_page, name='show_restaurant_page'),
    
    path('restaurants/', views.show_restaurant_page, name='show_restaurant_page'),
    path('restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_page, name='restaurant_page'),
    path('restaurants/<int:restaurant_id>/menu/', views.restaurant_menu, name='restaurant_menu'),
    path('restaurants/<int:restaurant_id>/update/', views.update_restaurant, name='update_restaurant'),
    path('restaurants/<int:restaurant_id>/update/page', views.update_restaurant_page, name='update_restaurant_page'),
    path('restaurants/<int:restaurant_id>/delete/', views.delete_restaurant, name='delete_restaurant'),

    # Menu Item management paths
    path('menu/<int:menuItem_id>/update/', views.update_menuItem, name='update_menuItem'),
    path('menu/<int:menuItem_id>/update/page/', views.update_menuItem_page, name='update_menuItem_page'),
    path('menu/<int:menuItem_id>/delete/', views.delete_menuItem, name='delete_menuItem'),

    # Customer management paths
    path('restaurants/<int:restaurant_id>/menu/customer/<str:username>/', views.customer_menu, name='customer_menu'),

    # --- CLEANED CUSTOMER CART PATHS ---
    # This is the ONLY path for viewing the cart
    path('cart/<str:username>/', views.show_cart_page, name='show_cart_page'),
    
    # This is the ONLY path for adding items to the cart
    path('cart/add/<int:menuItem_id>/<str:username>/', views.add_to_cart, name='add_to_cart'),

    # This is the path for checkout
    path('checkout/<str:username>/', views.checkout, name='checkout'),

    path('orders/<str:username>/', views.orders, name='view_orders'),
    
    path('cart/remove/<int:menuItem_id>/<str:username>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('cart/clear/<str:username>/', views.clear_cart, name='clear_cart'), 
]