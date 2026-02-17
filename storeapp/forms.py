from django import forms
from django.core.exceptions import ValidationError
import re

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    expiry_date = forms.CharField(max_length=5)
    cvv = forms.CharField(max_length=3)

    # ✅ Validate Card Number (exactly 16 digits)
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')

        if not re.fullmatch(r'\d{16}', card_number):
            raise ValidationError("Card number must contain exactly 16 digits.")

        return card_number

    # ✅ Validate CVV (exactly 3 digits)
    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')

        if not re.fullmatch(r'\d{3}', cvv):
            raise ValidationError("CVV must contain exactly 3 digits.")

        return cvv
