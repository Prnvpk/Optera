from django import forms
from django.core.exceptions import ValidationError
import re
from datetime import datetime


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

    # ✅ Validate Expiry Date (MM/YY and year >= 2026)
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')

        # Check format MM/YY
        if not re.fullmatch(r'(0[1-9]|1[0-2])\/\d{2}', expiry_date):
            raise ValidationError("Expiry date must be in MM/YY format (example: 12/28).")

        month, year = expiry_date.split('/')
        month = int(month)
        year = int("20" + year)   # convert YY -> YYYY

        now = datetime.now()

        # Must be 2026 or later
        if year < 2026:
            raise ValidationError("Expiry year must be 2026 or later.")

        # Check if expired
        if year < now.year or (year == now.year and month < now.month):
            raise ValidationError("Card has expired.")

        return expiry_date