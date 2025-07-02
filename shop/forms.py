from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'transaction_id']
        widgets = {
            'payment_method': forms.RadioSelect
        }
