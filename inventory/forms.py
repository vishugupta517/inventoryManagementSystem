from django import forms

from .models import Inventory


class SellItemForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["quantity"]

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be a positive number.")
        return quantity


class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["name", "iin", "cost", "quantity", "selling_price"]


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["name", "iin", "cost", "quantity", "selling_price"]
        widgets = {"quantity": forms.TextInput(attrs={"readonly": "readonly"})}


class PlaceOrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
