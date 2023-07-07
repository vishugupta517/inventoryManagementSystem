"""
URL configuration for ims project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from inventory.views import (
    confirm_order_canceled,
    confirm_order_received,
    create_item,
    delete_item,
    edit_item,
    home,
    item_details,
    item_list,
    item_orders,
    item_transactions,
    orders_failed,
    orders_successed,
    place_order,
    sell_item,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("items/", item_list, name="item_list"),
    path("items/create/", create_item, name="create_item"),
    path("items/<int:item_id>/sell/", sell_item, name="sell_item"),
    path("items/<int:item_id>/edit/", edit_item, name="edit_item"),
    path("items/<int:item_id>/delete/", delete_item, name="delete_item"),
    path("items/<int:item_id>/", item_details, name="item_details"),
    path("items/<int:item_id>/place-order/", place_order, name="place_order"),
    path("items/<int:item_id>/orders/", item_orders, name="item_orders"),
    path(
        "items/<int:item_id>/orders/accepted/",
        orders_successed,
        name="orders_successed",
    ),
    path(
        "items/<int:item_id>/orders/declined/",
        orders_failed,
        name="orders_failed",
    ),
    path(
        "items/orders/<int:order_id>/confirm-order?",
        confirm_order_received,
        name="confirm_order_received",
    ),
    path(
        "items/orders/<int:order_id>/cancel-order?/",
        confirm_order_canceled,
        name="confirm_order_canceled",
    ),
    path(
        "items/<int:item_id>/transactions/",
        item_transactions,
        name="item_transactions",
    ),
]

# from django.urls import path

# from inventory.views import (
#     create_item,
#     item_details,
#     item_list,
#     items_sold,
#     orders_canceled,
#     orders_placed,
#     orders_received,
#     sell_item,
# )

# app_name = "inventory"

# urlpatterns = [
#     path("", item_list, name="item_list"),
#     path("item/<int:item_id>/", item_details, name="item_details"),
#     path("item/create/", create_item, name="create_item"),
#     path("item/<int:item_id>/sell/", sell_item, name="sell_item"),
#     path("item/<int:item_id>/orders/placed/", orders_placed, name="orders_placed"),
#     path(
#         "item/<int:item_id>/orders/received/", orders_received, name="orders_received"
#     ),
#     path(
#         "item/<int:item_id>/orders/canceled/", orders_canceled, name="orders_canceled"
#     ),
#     path("item/<int:item_id>/transactions/", items_sold, name="items_sold"),
# ]
