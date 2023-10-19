from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name or self.email or "Unnamed Customer"

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)  # Add the description field
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
   

    def __str__(self):
        return self.name 

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)  # Set a default product ID
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    def get_cart_total(self):
        # Implement logic to calculate and return the cart total as a float
        total = 0
        for item in self.orderitem_set.all():
            total += item.get_total()  # Example: Calculate the total based on order items
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total_items = sum([item.quantity for item in orderitems])
        return total_items

    @property
    def get_cart_total(self):
        Orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in Orderitems])
        return total

    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if not item.product.digital:
                shipping = True
        return shipping

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order_ref = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, default='No Address Provided')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.address


class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivered = models.BooleanField(default=False)
    
    # New fields for tracking information
    carrier = models.CharField(max_length=100, null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Delivery for Order {self.order.id}"

        return self.name


class Promotion(models.Model):
    name = models.CharField(max_length=200, default="No Name")
    discount_percentage = models.PositiveIntegerField()
    products = models.ManyToManyField(Product, related_name='promotions')
    start_date = models.DateField()
    end_date = models.DateField()

    def promotion_image(self):
        # Get the image of the first associated product
        if self.products.exists():
            return self.products.first().image.url
        return None

    def __str__(self):
        return self.name

class MensClothing(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name or "Unnamed Men's Clothing"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class WomensClothig(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class KidsClothing(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name
  
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url