from django import forms
from .models import *


class ContactForms(forms.ModelForm):
    name  = forms.CharField(label='', required=True, widget=forms.TextInput(
                                                 attrs={
                                                     "class": "input-field"
                                                 }
                                             )
                                        )
    surname =  forms.CharField(label='', required=False, widget=forms.TextInput(
                                                 attrs={
                                                     "class": "input-field"
                                                 }
                                             )
                                        )
    company = forms.CharField(label='', required=False, widget=forms.TextInput(
                                                attrs={
                                                    "class": "input-field"
                                                }
                                            )
                                        )
    email =  forms.EmailField(label='', required=True, widget=forms.EmailInput(
                                                 attrs={
                                                     "class": "input-field"
                                                 }
                                             )
                                        )
    question = forms.CharField(label='', required=True, widget=forms.Textarea(
                                                attrs={
                                                    "rows": 7,
                                                    "cols": 15,
                                                    "class": "input-field"

                                                }
                                            )
                                        )

    confirmation = forms.BooleanField(initial=True)

    class Meta:
        model = ContactModels
        fields = [
            'name',
            'surname',
            'company',
            'email',
            'question',
            'confirmation',
        ]