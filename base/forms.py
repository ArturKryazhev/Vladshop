from django.forms import ModelForm
from .models import Order
from django.forms import TextInput

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'buying_type',  'comment')