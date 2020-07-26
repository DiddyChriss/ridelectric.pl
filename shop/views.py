from django.shortcuts import render, get_object_or_404, redirect
from shop.forms import ProductShop, ProductFormShop
from shop.models import Shop_models

# Create your views here.

def shop(request):

    return render(request, 'sklep.html', {})

# def shop_test(request):
#     my_form = ProductFormShop()
#     if request.method == 'POST':
#         my_form = ProductFormShop(request.POST)
#         if my_form.is_valid():
#             Shop_models.objects.create(**my_form.cleaned_data)
#         my_form = ProductFormShop()
#
#     context = {
#         'form' : my_form
#     }
#
#     return render(request, 'shop_test.html', context)



# def shop_test(request):
#     form = ProductShop(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = ProductShop()
#
#     context = {
#         'form' : form
#     }
#
#     return render(request, 'shop_test.html', context)

# def shop_test(request):
#     initail_data = {
#         'name_shop': "initial data"
#     }
#     # obj = Shop_models.objects.get(name_shop = 'new')
#     form = ProductShop(request.POST or None, initial=initail_data)        # instance = obj)
#     if form.is_valid():
#         form.save()
#         form = ProductShop()
#
#     context = {
#         'form' : form
#     }
#
#     return render(request, 'shop_test.html', context)

def shop_test_slug(request, slug):

    obj = get_object_or_404(Shop_models, name_shop=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('../../')

    context = {
        'objects': obj
    }

    return render(request, 'shop_test.html', context)

def shop_test(request):

    queryset = Shop_models.objects.all()

    context = {
        'object_list': queryset
    }

    return render(request, 'shop_test_II.html', context)