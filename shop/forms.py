from django import forms
from shop.models import Shop_models

class ProductShop(forms.ModelForm):
    name_shop = forms.CharField(label='Name', widget=forms.TextInput(attrs={"size": 10, "placeholder": "Your Name"}))
    coment_shop = forms.CharField(required=False, label='Comment', widget=forms.Textarea(
                                                    attrs={
                                                        "placeholder": "Coment",
                                                        "rows": 10,
                                                        "cols": 30
                                                    }
                                                )
                                                                              )
    price = forms.DecimalField(widget=forms.TextInput(attrs={"placeholder": "19.99"}))
    confirmation_buy = forms.BooleanField(required=False)
    class Meta:
        model = Shop_models
        fields = [
            'name_shop',
            'coment_shop',
            'price',
            'confirmation_buy'
        ]

    def clean_name_shop(self,*args, **kwargs):
        name_shop = self.cleaned_data.get('name_shop')
        if "fuck" in name_shop:
            raise forms.ValidationError('It\'s a bad word! Stop use!')
        return name_shop




class ProductFormShop(forms.Form):
    name_shop        = forms.CharField(label='Name', widget=forms.TextInput(attrs={"size": 10, "placeholder": "Your Name"}))
    coment_shop      = forms.CharField(required=False, label='Comment', widget=forms.Textarea(
                                                attrs={
                                                    "placeholder": "Coment",
                                                    "rows": 10,
                                                    "cols": 30
                                                }
                                            )
                                       )
    price            = forms.DecimalField(widget=forms.TextInput(attrs={"placeholder": "19.99"}))
    confirmation_buy = forms.BooleanField(required=False)