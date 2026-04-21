from pyexpat.errors import messages
from urllib import request
import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from delivery.models import Cart, Customer, MenuItem, Restaurant

# Create your views here.
def index(request):
    return render(request, 'delivery/index.html')

def signin(request):
    return render(request, 'delivery/signin.html')

def signup(request):
    return render(request, 'delivery/signup.html')

# Handle Login
def handle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            Customer.objects.get(username=username, password=password)
            
            # Admin User
            if username == 'admin':
                return render(request, 'delivery/home.html', {'username': username})
            
            # Normal Customer User
            else:
                restaurants = Restaurant.objects.all()
                return render(request, 'delivery/customer_home.html', {
                    'restaurants': restaurants,
                    'username': username
                })
                
        except Customer.DoesNotExist:
            return render(request, 'delivery/signin.html', 
                         {'error': 'Invalid username or password.'})

    # If someone opens the login page directly (GET request)
    return render(request, 'delivery/signin.html')

# Handle Registration
def handle_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        
        #preventing duplicate username
        try:
            #username already exists
            cust = Customer.objects.get(username=username, password=password)
            return render(request, 'delivery/signin.html', {'error': 'Username already exists.'})
        except:
            #username is available, create new user
            c = Customer(username=username, password=password, email=email, address=address, mobile=mobile)
            c.save()
            
        return render(request,'delivery/signin.html')
        
        # return HttpResponse(f"Registered Username: {username}, Password: {password}, Email: {email}, Address: {address}, Mobile: {mobile}")
    else:
        return HttpResponse("Invalid request method.")

# Restaurant Management Views
def restaurant_page(request):
    return render(request, 'delivery/add_restaurant.html')

# Add New Restaurant
def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cuisines = request.POST.get('cuisines')
        rating = request.POST.get('rating')
        picture = request.POST.get('picture')
        
        #preventing duplicate restaurant name
        try:
            #restaurant already exists
            rest = Restaurant.objects.get(name=name)
            return render(request, 'delivery/add_restaurant.html', {'error': 'Restaurant already exists.'})
        except:
            #restaurant is available, add new restaurant
            rest = Restaurant(name=name, cuisines=cuisines, rating=rating, picture=picture)
            rest.save()
        
        restaurants = Restaurant.objects.all()
    
        return render(request,'delivery/show_restaurants.html', {"restaurants": restaurants})
        
        # return HttpResponse(f"Registered Username: {username}, Password: {password}, Email: {email}, Address: {address}, Mobile: {mobile}")
    else:
        return HttpResponse("Invalid request method.")

# Show all Restaurants
def show_restaurant_page(request):
    restaurants = Restaurant.objects.all()
    username = request.GET.get('username', 'Guest')
    
    # If the person is admin, show the management list
    if username == 'admin':
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants, "username": username})
    
    # Otherwise, show the customer browsing list (customer_home.html)
    else:
        return render(request, 'delivery/customer_home.html', {"restaurants": restaurants, "username": username})

# Restaurant Menu Management Views
def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if request.method == 'POST':
        #Handle adding new menu item
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        picture = request.POST.get('picture')
        
        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            is_veg=is_veg,
            picture=picture
        )
        
        return redirect('restaurant_menu', restaurant_id=restaurant.id)
    
    #Fetch all menu items for the restaurant
    menu_items = restaurant.menu_items.all()

    return render(request, 'delivery/menu.html', {
        'restaurant': restaurant, 
        'menu_items': menu_items,
    })
    
# Update Restaurant Page
def update_restaurant_page(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'delivery/update_restaurant_page.html', {"restaurant": restaurant})

# Update Restaurant
def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.cuisines = request.POST.get('cuisines')
        restaurant.rating = request.POST.get('rating')
        restaurant.picture = request.POST.get('picture')
        restaurant.save()
        
        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

# Delete Restaurant
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()
    
    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})


# Update Menu Item Page
def update_menuItem_page(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)
    return render(request, 'delivery/update_menuItem_page.html', {"item": menuItem})

# Update Menu Item
def update_menuItem(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)

    if request.method == 'POST':
        menuItem.name = request.POST.get('name')
        menuItem.description = request.POST.get('description')
        menuItem.price = request.POST.get('price')
        menuItem.is_veg = request.POST.get('is_veg') == 'on'
        menuItem.picture = request.POST.get('picture')
        
        menuItem.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

# Delete Menu Item
def delete_menuItem(request, menuItem_id):
        menuItem = get_object_or_404(MenuItem, id=menuItem_id)
        menuItem.delete()
    
        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})
    




# Customer Menu Management Views
def customer_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()

    return render(request, 'delivery/customer_menu.html', {
        'restaurant': restaurant, 
        'menu_items': menu_items,
        'username': username,
    })
  
  
# Add items to Cart
def add_to_cart(request, menuItem_id, username):
    customer = get_object_or_404(Customer, username=username)
    item = get_object_or_404(MenuItem, id=menuItem_id)

    # Get or create a cart for the customer
    cart, created = Cart.objects.get_or_create(customer=customer)
    
    # Add the item to the cart
    cart.items.add(item)
    cart.save()
    
    return redirect('customer_menu', restaurant_id=item.restaurant.id, username=username)

# Customer Cart View
def show_cart_page(request, username):
    #Fetch the customer
    customer = get_object_or_404(Customer, username=username)
    
    #Fetch the customer's cart
    #We use .filter().first() so it returns None if no cart exists yet
    cart = Cart.objects.filter(customer=customer).first()

    #Handle the "No Cart" scenario gracefully
    #This prevents the page from crashing if the cart is empty
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'delivery/customer_cart.html', {
        'items': items,             # Note: change your HTML loop to {% for item in items %}
        'total_price': total_price,
        'username': username,
    })
    
# Remove item from Cart
def remove_from_cart(request, menuItem_id, username):
    #Get the customer
    customer = get_object_or_404(Customer, username=username)
    
    #Get the item to be removed
    item = get_object_or_404(MenuItem, id=menuItem_id)
    
    #Get the customer's cart
    cart = Cart.objects.filter(customer=customer).first()
    
    if cart:
        #Remove the specific item from the ManyToMany relationship
        cart.items.remove(item)
    
    #Redirect back to the cart page to show updated list/total
    return redirect('show_cart_page', username=username)

# Clear Cart
def clear_cart(request, username):
    #Get the customer
    customer = get_object_or_404(Customer, username=username)
    
    #Get the customer's cart
    cart = Cart.objects.filter(customer=customer).first()
    
    if cart:
        #Wipe all items from this cart at once
        cart.items.clear()
    
    #Redirect back to the cart page (which will now show the "Empty Cart" message)
    return redirect('show_cart_page', username=username)

# Checkout Page
def checkout(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0
    
    if total_price == 0:
        return render(request, 'delivery/customer_cart.html', {
            'username': username,
            'items': items,
            'error': 'Your cart is empty!'
        })
        
    # Razorpay Integration
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        amount_paise = int(total_price * 100) # Razorpay works in Paise
        
        order_data = {
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': '1'
        }
        order = client.order.create(data=order_data)
        
        return render(request, 'delivery/checkout.html', {
            'username': username,
            'total_price': total_price,
            'amount_paise': amount_paise,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
        })
    except Exception as e:
        # If Razorpay fails (e.g. invalid keys), show a readable error
        return HttpResponse(f"Payment Gateway Error: {e}. Please check your RAZORPAY settings.")
    
# View Orders
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    
    # Capture items for the receipt BEFORE clearing the cart
    cart_items = list(cart.items.all()) if cart else []
    total_price = cart.total_price() if cart else 0
    
    if cart:
        cart.items.clear()  # Empty the cart after successful payment simulation
        
    return render(request, 'delivery/orders.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
    })