from django import forms
from .models import *


class Search_form(forms.Form):
    search_product          = forms.CharField(label='', widget=forms.TextInput(
                                                attrs={
                                                    "placeholder": "Szukaj",
                                                    "class": "col form-control shadow-sm p-1 mx-1 rounded"
                                                }
                                            )
                                       )

class PaymentForms(forms.ModelForm):
    firstname  = forms.CharField(label='', required=True, widget=forms.TextInput(
                                                 attrs={
                                                     "placeholder": "Imię",
                                                     "class": "form-control"
                                                 }
                                             )
                                        )
    lastname =  forms.CharField(label='', required=True, widget=forms.TextInput(
                                                 attrs={
                                                     "placeholder": "Nazwisko",
                                                     "class": "form-control"
                                                 }
                                             )
                                        )
    email =  forms.EmailField(label='', required=True, widget=forms.EmailInput(
                                                 attrs={
                                                     "placeholder": "adres e-mail",
                                                     "class": "form-control"
                                                 }
                                             )
                                        )
    number =  forms.IntegerField(label='', required=True, widget=forms.NumberInput(
                                                 attrs={
                                                     "placeholder": "Telefon",
                                                     "class": "form-control"
                                                 }
                                             )
                                        )

    streetnumber = forms.CharField(label='', required=True, widget=forms.TextInput(
                                                attrs={
                                                    "placeholder": "Ulica, nr.Domu",
                                                    "class": "form-control"
                                                }
                                            )
                                                                    )
    city = forms.CharField(label='',required=True, widget=forms.TextInput(
                                                 attrs={
                                                     "placeholder": "Miasto",
                                                     "class": "form-control"
                                                 }
                                             )
                                        )
    zipcode =  forms.CharField(label='', required=True, widget=forms.TextInput(
                                                 attrs={
                                                     "size":6,
                                                     "placeholder": "Kod",
                                                     "class": "form-control"

                                                 }
                                             )
                                        )
    comment = forms.CharField(label='', required=False, widget=forms.Textarea(
        attrs={
            "rows": 4,
            "cols": 10,
            "placeholder": "Uwagi",
            "class": "form-control"

        }
    )
                              )

    class Meta:
        model = ShoppingAddress
        fields = (
            'firstname',
            'lastname',
            'email',
            'number',
            'streetnumber',
            'city',
            'zipcode',
            'comment'
        )

