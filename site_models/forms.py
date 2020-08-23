from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



PAYMENT_OPTION = (
    ('S', 'Stripe'),
    ('P', 'Cash')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "123 Mount St", "class": "form-control checkout__input__add"
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            "class": "form-control col-12"
        })
    )
    phone = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_OPTION)
