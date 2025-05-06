from django.contrib import admin
from .models import Shop, Seller, Item, Customer, Order, ShoppingCart, Inventory, ShopManager, Inventory

admin.site.register(Shop)
admin.site.register(Seller)
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(ShoppingCart)
admin.site.register(Inventory)
admin.site.register(ShopManager)
