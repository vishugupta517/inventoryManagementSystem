from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CreateItemForm, EditItemForm, PlaceOrderForm, SellItemForm
from .models import Inventory, Order, Transaction


def home(request):
    total_profit = Inventory.objects.aggregate(Sum("profit_earned"))[
        "profit_earned__sum"
    ]
    revenue = Inventory.objects.aggregate(Sum("revenue"))["revenue__sum"]
    total_items = Inventory.objects.aggregate(Sum("quantity"))["quantity__sum"]
    highest_cost_item = Inventory.objects.order_by("-cost").first()
    highest_profit_item = Inventory.objects.order_by("-profit_earned").first()
    most_sold_item = Inventory.objects.order_by("-quantity_sold").first()
    out_of_stock_items = Inventory.objects.filter(quantity=0)
    low_stock_items = Inventory.objects.filter(quantity__lte=30)[:3]
    most_sold_items = Inventory.objects.order_by("-quantity_sold")
    total_sold_items = Inventory.objects.aggregate(Sum("quantity_sold"))[
        "quantity_sold__sum"
    ]
    total_sold_cost = Transaction.objects.filter(item__quantity_sold__gt=0).aggregate(
        Sum("cost")
    )
    total_sold_amount = total_sold_cost["cost__sum"] or 0
    total_ordered_items = Order.objects.aggregate(Sum("quantity"))["quantity__sum"]
    total_orders_amount = Order.objects.aggregate(Sum("cost"))["cost__sum"]
    total_canceled_orders = Order.objects.filter(is_canceled=True).count()
    total_accepted_orders = Order.objects.filter(is_received=True).count()
    total_pending_orders = Order.objects.filter(
        is_received=False, is_canceled=False
    ).count()
    context = {
        "total_profit": total_profit,
        "revenue": revenue,
        "total_items": total_items,
        "highest_cost_item": highest_cost_item.name,
        "highest_profit_item": highest_profit_item.name,
        "most_sold_item": most_sold_item,
        "out_of_stock_items": out_of_stock_items,
        "low_stock_items": low_stock_items,
        "most_sold_items": most_sold_items,
        "total_sold_items": total_sold_items,
        "total_sold_amount": total_sold_amount,
        "total_orders_amount": total_orders_amount,
        "total_ordered_items": total_ordered_items,
        "total_canceled_orders": total_canceled_orders,
        "total_accepted_orders": total_accepted_orders,
        "total_pending_orders": total_pending_orders,
    }

    return render(request, "inventory/home.html", context)


# Display all items
def item_list(request):
    items = Inventory.objects.all()
    context = {"items": items}
    return render(request, "inventory/item_list.html", context)


# Display an Item
def item_details(request, item_id):
    item = Inventory.objects.get(pk=item_id)
    orders = Order.objects.filter(item=item).order_by("-orderdttm")
    context = {"item": item, "orders": orders}

    return render(request, "inventory/item_details.html", context)


# Create an item
def create_item(request):
    if request.method == "POST":
        form = CreateItemForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data["name"]
            messages.success(request, f" '{name}' stock added successfully!")
            return redirect("item_list")
    else:
        form = CreateItemForm()

    context = {
        "form": form,
    }

    return render(request, "inventory/create_item.html", context)


# Update an item
def edit_item(request, item_id):
    item = Inventory.objects.get(pk=item_id)
    # form = CreateItemForm(instance=item)

    if request.method == "POST":
        form = EditItemForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, f"{item.name} stock updated successfully!")
            return redirect("item_list")
    else:
        form = EditItemForm(instance=item)

    return render(request, "inventory/edit_item.html", {"form": form, "item": item})


# Delete an item
def delete_item(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    if request.method == "POST":
        item.delete()
        messages.success(request, f"{item.name} stock deleted successfully")
        return redirect("item_list")

    return render(
        request, "inventory/delete_item.html", {"item": item, "item_id": item_id}
    )


# Sell an item
def sell_item(request, item_id):
    item = Inventory.objects.get(pk=item_id)
    message = None

    if request.method == "POST":
        form = SellItemForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            if quantity <= item.quantity:
                item.quantity -= quantity
                item.quantity_sold += quantity
                item.revenue += quantity * item.selling_price
                item.profit_earned += quantity * (item.selling_price - item.cost)
                item.save()

                cost = item.cost * quantity

                Transaction.objects.create(
                    item=item,
                    quantity=quantity,
                    selling_price=item.selling_price,
                    cost=cost,
                )

                message = "Item sold successfully."
                form = SellItemForm()  # Clear the form data
            else:
                message = "Insufficient quantity available."
    else:
        form = SellItemForm()

    context = {
        "item": item,
        "form": form,
        "message": message,
    }
    return render(request, "inventory/sell_item.html", context)


def place_order(request, item_id):
    item = Inventory.objects.get(id=item_id)

    if request.method == "POST":
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            cost = item.cost * quantity

            Order.objects.create(
                item=item,
                quantity=quantity,
                cost=cost,
                is_received=False,
                is_canceled=False,
            )

            return redirect("item_orders", item_id=item_id)
    else:
        form = PlaceOrderForm()

    context = {"item": item, "form": form}
    return render(request, "inventory/place_order.html", context)


def confirm_order_received(request, order_id):
    order = Order.objects.get(id=order_id)
    order.is_received = True
    order.item.quantity += order.quantity
    order.item.save()
    order.save()
    return redirect("item_orders", item_id=order.item.id)


def orders_successed(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    confirmed_orders = Order.objects.filter(item=item, is_received=True).order_by(
        "-orderdttm"
    )
    return render(
        request,
        "inventory/orders_successed.html",
        {"item": item, "confirmed_orders": confirmed_orders},
    )


def confirm_order_canceled(request, order_id):
    order = Order.objects.get(id=order_id)
    order.is_canceled = True
    order.save()
    return redirect("item_orders", item_id=order.item.id)


def orders_failed(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    failed_orders = Order.objects.filter(item=item, is_canceled=True).order_by(
        "-orderdttm"
    )
    return render(
        request,
        "inventory/orders_canceled.html",
        {"item": item, "failed_orders": failed_orders},
    )


def item_orders(request, item_id):
    item = Inventory.objects.get(id=item_id)
    orders = Order.objects.filter(item=item).order_by("-orderdttm")

    context = {"item": item, "orders": orders}
    return render(request, "inventory/item_orders.html", context)


def item_transactions(request, item_id):
    #  transactions(related name from model)
    item = Inventory.objects.get(id=item_id)
    all_transactions = item.transactions.all()
    total_cost = sum(
        transaction.quantity * transaction.selling_price
        for transaction in all_transactions
    )

    context = {
        "item": item,
        "all_transactions": all_transactions,
        "total_cost": total_cost,
    }

    return render(request, "inventory/item_transactions.html", context)
