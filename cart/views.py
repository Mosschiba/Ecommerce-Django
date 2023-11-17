from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.


def cart_summary(request):
    return render(request, 'cart_summary.html', {})


def cart_add(request):
    # get the Cart
    cart = Cart(request)
    # check for POST
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))

        # lookup Product in DB
        product = get_object_or_404(Product, id=product_id)

        # save in session
        cart.add(product=product)

        # retund json
        response = JsonResponse({'Product Name: ': product.name})
        return response


def cart_delete(request):
    pass


def cart_update(request):
    pass
