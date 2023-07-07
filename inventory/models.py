# from django.db import models


# class Inventory(models.Model):
#     name = models.CharField(max_length=100)
#     iin = models.CharField(max_length=100, unique=True)
#     cost = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField()
#     quantity_sold = models.PositiveIntegerField(default=0)
#     selling_price = models.DecimalField(max_digits=10, decimal_places=2)
#     profit_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     class Meta:
#         app_label = "inventory"


# class Orders(models.Model):
#     name = models.CharField(max_length=100)
#     item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     cost = models.DecimalField(max_digits=10, decimal_places=2)
#     orderdttm = models.DateTimeField(auto_now_add=True)
#     is_received = models.BooleanField(default=False)
#     is_cancel = models.BooleanField(default=False)


# class Transaction(models.Model):
#     name = models.CharField(max_length=100)
#     item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     selling_price = models.DecimalField(max_digits=10, decimal_places=2)
#     transactiondttm = models.DateTimeField(auto_now_add=True)
#     transactiondttm = models.DateTimeField(auto_now_add=True)

from django.db import models


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    iin = models.CharField(max_length=100, unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        app_label = "inventory"

    def __str__(self):
        return self.name


class Order(models.Model):
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    orderdttm = models.DateTimeField(auto_now_add=True)
    is_received = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    class Meta:
        app_label = "inventory"

    def __str__(self):
        return f"Order {self.id} - {self.item.name}"


class Transaction(models.Model):
    item = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="transactions"
    )
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    transactiondttm = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "inventory"

    def __str__(self):
        return f"Transaction {self.id} - {self.item.name}"
