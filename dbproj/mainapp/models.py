from django.db import models

class Shop(models.Model):
    shop_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    shop_description = models.TextField(default="No Description Provided")


    def __str__(self):
        return self.shop_name
    
class Seller(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    #shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="sellers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ShopManager(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="managers")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="managed_shops")
    def __str__(self):
        return f"{self.seller} manages {self.shop}"


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="No Description Provided")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Inventory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.shop} contains {self.quantity} of {self.item}"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  

    def __str__(self):
        return self.name
    
class ShoppingCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.customer.name}'s Shopping Cart"

class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True, db_index=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # For total price

    def save(self, *args, **kwargs):
        # Automatically set the total_price before saving
        self.total_price = self.item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} from {self.shop.shop_name}"
