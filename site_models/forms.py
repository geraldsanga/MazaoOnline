from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django import forms



PAYMENT_OPTION = (
    ('S', 'Stripe'),
    ('P', 'Cash')
)

# PAYMENT_CHOICES = (
#     ('S', 'Stripe'),
#     ('P', 'PayPal')
# )


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


# class CheckoutForm(forms.Form):
#     shipping_address = forms.CharField(required=False)
#     shipping_address2 = forms.CharField(required=False)
#     shipping_country = CountryField(blank_label='(select country)').formfield(
#         required=False,
#         widget=CountrySelectWidget(attrs={
#             'class': 'custom-select d-block w-100',
#         }))
#     shipping_zip = forms.CharField(required=False)

#     billing_address = forms.CharField(required=False)
#     billing_address2 = forms.CharField(required=False)
#     billing_country = CountryField(blank_label='(select country)').formfield(
#         required=False,
#         widget=CountrySelectWidget(attrs={
#             'class': 'custom-select d-block w-100',
#         }))
#     billing_zip = forms.CharField(required=False)

#     same_billing_address = forms.BooleanField(required=False)
#     set_default_shipping = forms.BooleanField(required=False)
#     use_default_shipping = forms.BooleanField(required=False)
#     set_default_billing = forms.BooleanField(required=False)
#     use_default_billing = forms.BooleanField(required=False)

#     payment_option = forms.ChoiceField(
#         widget=forms.RadioSelect, choices=PAYMENT_CHOICES)