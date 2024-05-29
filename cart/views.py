from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Part
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_parts = cart.get_pars
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_parts":cart_parts, "quantities":quantities, "totals":totals})


def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # Test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        part_id = int(request.POST.get('part_id'))
        part_qty = int(request.POST.get('part_qty'))

        # lookup part in DB
        part = get_object_or_404(Part, id=part_id)

        # Save to session
        cart.add(part=part, quantity=part_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return response
        # response = JsonResponse({'Part Name: ': part.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Part Added to Cart"))
        return response
    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        part_id = int(request.POST.get('part_id'))
        # Call delete function in Cart
        cart.delete(part=part_id)

        response = JsonResponse({'part':part_id})
        messages.success(request, ("Item Deleted From Cart!"))
        # return redirect('cart_summary')
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        part_id = int(request.POST.get('part_id'))
        part_qty = int(request.POST.get('part_qty'))

        cart.update(part=part_id, quantity=part_qty)

        response = JsonResponse({'qty':part_qty})
        messages.success(request, ("Your Cart Has Been Updated!"))
        return response
        #return redirect('cart_summary')
