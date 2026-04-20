from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.username} {self.password} {self.email} {self.address} {self.mobile}"
    
class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    cuisines = models.CharField(max_length=200)
    rating = models.FloatField()
    picture = models.URLField(max_length=200, default="https://scarborough.originalshawarma.ca/wp-content/uploads/2024/07/placeholder-restaurant.png")

    def __str__(self):
        return f"{self.name} {self.cuisines} {self.rating}"

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')

    name = models.CharField(max_length=20)
    picture = models.URLField(max_length=200, default="https://cdn-icons-png.flaticon.com/512/1147/1147856.png")
    description = models.CharField(max_length=200)
    price = models.FloatField()
    is_veg = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.description} {self.price}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField("MenuItem", related_name='carts')

    def total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"{self.customer.username} {self.total_price}"