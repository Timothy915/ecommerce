from .models import Order  # Import your Order model or relevant models

def cart_total(request):
    cart_total = 0

    if request.user.is_authenticated:
        user_order = Order.objects.filter(customer=request.user, complete=False).first()
        if user_order:
            cart_total = user_order.get_cart_total()

    return {'cart_total': cart_total}
