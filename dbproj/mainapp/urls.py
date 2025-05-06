from django.urls import path

from . import views
from .views import shopkeep

urlpatterns = [
    path('shopkeep/<int:shop_id>/', shopkeep, name='shopkeep'),
    path('shopkeep/<int:shop_id>/report/', views.shopkeep_report, name='shopkeep_report'),
    path('item/edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('item/delete/<int:item_id>/', views.delete_item, name='delete_item'),       
    path('item/add/<int:shop_id>/', views.add_item, name='add_item'), 
    path('item/details/shop<int:shop_id>/<int:item_id>/', views.item_detail, name='item_detail'),
    path('shop/<int:shop_id>/', views.customer_shop_view, name='customer_shop_view'),
    path('shop/<int:shop_id>/buy/<int:item_id>/', views.purchase_item, name='purchase_item'),
    path('mainapp/order/<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('', views.home, name='home')

]