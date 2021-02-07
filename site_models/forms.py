from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django import forms



PAYMENT_OPTION = (
    ('S', 'Stripe'),
    ('P', 'Cash')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "123 Mount St", "class": "form-control checkout__input__add", "required": "true"
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            "class": "form-control col-12",
        })
    )
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "class": "form-control", "required": "true", "minlenghth": 13
    }))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "class": "form-control", "required": "true"
    }))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_OPTION)

    # def clean_street_address(self):
    #     data = self.cleaned_data['street_address']
    #     if 