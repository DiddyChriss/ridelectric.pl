from django import forms
from shop.models import shop_products


class Search_form(forms.Form):
    search_product          = forms.CharField(label='', widget=forms.TextInput(
                                                attrs={
                                                    "size": 20,
                                                    "placeholder": "Szukaj",
                                                    "class": "col form-control shadow-sm p-1 mx-1 rounded"
                                                }
                                            )
                                       )

class Quantity_form(forms.Form):
    quantity = forms.IntegerField(label='',
                                  required=True,
                                  initial=1,
                                  max_value=99,
                                  min_value=0,
                                  widget=forms.NumberInput(
                                      attrs={
                                          "size": 5
                                      }
                                  )
                                  )

# class ProductShop(forms.ModelForm):
#     title_product  = forms.CharField(label='Name', widget=forms.TextInput(
#                                                  attrs={
#                                                      "size": 30,
#                                                      "placeholder": "Your Name"
#                                                  }
#                                              )
#                                         )
#     description_product = forms.CharField(required=False, label='Comment', widget=forms.Textarea(
#                                                  attrs={
#                                                      "placeholder": "Coment",
#                                                      "rows": 10,
#                                                      "cols": 30
#                                                  }
#                                              )
#                                         )
#     price_product = forms.DecimalField(widget=forms.TextInput(
#                                                  attrs={
#                                                      "placeholder": "19.99"
#                                                  }
#                                              )
#                                          )
#     image_product = forms.FileField(label='Image', required=False)
#     confirmation_buy = forms.BooleanField(required=False)
#     class Meta:
#         model = Shop_models
#         fields = (
#             'title_product',
#             'description_product',
#             'price_product',
#             'image_product',
#             'confirmation_buy'
#         )

    # def clean_name_shop(self,*args, **kwargs):
    #     name_shop = self.cleaned_data.get('name_shop')
    #     if "fuck" in name_shop:
    #         raise forms.ValidationError('It\'s a bad word! Stop use!')
    #     return name_shop




# class ProductFormShop(forms.Form):
#     title_product            = forms.CharField(label='Name', widget=forms.TextInput(
#                                                 attrs={
#                                                     "size": 30,
#                                                     "placeholder": "Your Name"}
#                                             )
#                                        )
#     description_product      = forms.CharField(required=False, label='Comment', widget=forms.Textarea(
#                                                 attrs={
#                                                     "placeholder": "Coment",
#                                                     "rows": 10,
#                                                     "cols": 30
#                                                 }
#                                             )
#                                        )
#     price_product            = forms.DecimalField(widget=forms.TextInput(
#                                                 attrs={
#                                                     "placeholder": "19.99"
#                                                 }
#                                             )
#                                         )
#     image_product             = forms.FileField(label='Photo',required=False)
#     confirmation_buy = forms.BooleanField(required=False)