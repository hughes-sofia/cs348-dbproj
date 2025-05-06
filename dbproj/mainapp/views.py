from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.db import models, transaction
from django.utils.timezone import now
from django.db.models import F, Sum, Count
from .models import Shop, ShopManager, Inventory, Item, Order
from .forms import ItemForm
from .utils import raw_today_revenue


# Create your views here.

def home(request):
    return HttpResponse("Hello, world. You're home.")

def shopkeep(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    shopkeepers = ShopManager.objects.filter(shop=shop).select_related('seller')
    inventory_items = Inventory.objects.filter(shop=shop)

    return render(request, 'mainapp/shopkeep.html', {
        'shop': shop,
        'shopkeepers': shopkeepers,
        'inventory_items': inventory_items,
    })

def shopkeep_report(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    orders = Order.objects.filter(shop_id=shop_id)
    total_revenue = orders.aggregate(total=models.Sum('total_price'))['total'] or 0
    today = now().date()
    today_revenue = orders.filter(order_date__date=today).aggregate(
        total=models.Sum('total_price')
    )['total'] or 0

    sort_order = request.GET.get('sort', 'desc')  # defaults to 'desc'
    ordering = 'total_earned' if sort_order == 'asc' else '-total_earned'

    top_items = Order.objects.filter(shop=shop) \
        .values('item__id', 'item__name') \
        .annotate(
            total_earned=Sum('total_price'),
            total_orders_with=Count('id'),
            times_bought=Sum('quantity')
        ) \
        .order_by(ordering)
    
    return render(request, 'mainapp/shopkeep_report.html', {
        'shop': shop,
        'total_revenue': total_revenue,
        'today': today,
        'today_revenue': today_revenue,
        'top_items': top_items
    })

def item_detail(request, item_id, shop_id):
    item = get_object_or_404(Item, id=item_id)
    shop = get_object_or_404(Shop, id=shop_id)
    orders = Order.objects.filter(shop_id=shop_id, item_id = item_id)

    sales_data = Order.objects.filter(item=item).aggregate(
        times_bought=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('item__price'), output_field=models.DecimalField()),
        total_orders=Count('id')
    )

    return render(request, 'mainapp/item_detail.html', {
        'item': item,
        'shop': shop,
        'shop_id': shop_id,
        'sales_data': sales_data,
        'orders': orders
    })


@transaction.atomic
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('shopkeep', shop_id=item.inventory_set.first().shop.id)
    else:
        form = ItemForm(instance=item)

    return render(request, 'mainapp/edit_item.html', {'form': form, 'item': item})

@transaction.atomic
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    shop_id = item.inventory_set.first().shop.id  
    item.delete()
    return redirect('shopkeep', shop_id=shop_id) 

def add_item(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            # Add item to inventory
            Inventory.objects.create(shop=shop, item=item)
            return redirect('shopkeep', shop_id=shop.id)
    else:
        form = ItemForm()
    
    return render(request, 'mainapp/add_item.html', {'form': form, 'shop': shop})

def customer_shop_view(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    inventory_items = Inventory.objects.filter(shop=shop)

    return render(request, 'mainapp/customer_shop.html', {
        'shop': shop,
        'inventory_items': inventory_items
    })

@transaction.atomic
def purchase_item(request, shop_id, item_id):

    item = get_object_or_404(Item, id=item_id)
    shop = get_object_or_404(Shop, id=shop_id)
    inventory = Inventory.objects.filter(shop_id=shop_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))

        if item.quantity < quantity:
            return render(request, 'mainapp/insufficient_stock.html', {'shop_id': shop_id})


        total_price = item.price * quantity
        order = Order.objects.create(
            item=item,
            shop=shop,
            quantity=quantity,
            total_price=total_price,
            order_date=request.POST.get('order_date')
        )
        item.quantity -= quantity
        item.save()
        return redirect('order_confirmation', order_id=order.id)
    else:
        return render(request, 'mainapp/insufficient_stock.html', {'item': item, 'shop_id': shop_id})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'mainapp/order_confirmation.html', {'order': order})

