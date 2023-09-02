from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress, Delivery
from .models import Promotion
from django.utils import timezone

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# Define a custom admin class for CompletedOrder
class CompletedOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'customer_email', 'order_date', 'item_details', 'total_items', 'total_price', 'shipping_required', 'shipping_address', 'order_status')
    list_filter = ('date_ordered', 'complete')  # Removed 'delivery__delivered' from list_filter
    search_fields = ('customer__name', 'customer__email', 'id')

    def order_id(self, obj):
        return obj.id
    order_id.short_description = 'Order ID'

    def customer_name(self, obj):
        return obj.customer.name or "Unnamed Customer"
    customer_name.short_description = 'Customer Name'

    def customer_email(self, obj):
        return obj.customer.email or "No Email"
    customer_email.short_description = 'Customer Email'

    def order_date(self, obj):
        return obj.date_ordered
    order_date.short_description = 'Order Date'

    def item_details(self, obj):
        item_details = [f"{item.product.name} ({item.quantity} x {item.product.price})" for item in obj.orderitem_set.all()]
        return ', '.join(item_details)
    item_details.short_description = 'Item Details'

    def total_items(self, obj):
        return obj.get_cart_items
    total_items.short_description = 'Total Items'

    def total_price(self, obj):
        return obj.get_cart_total
    total_price.short_description = 'Total Price'

    def shipping_required(self, obj):
        return obj.shipping()
    shipping_required.short_description = 'Shipping Required'

    def shipping_address(self, obj):
        address = ShippingAddress.objects.filter(order=obj).first()
        if address:
            return f"{address.address}, {address.city}, {address.state}, {address.zipcode}"
        return "No Shipping Address"
    shipping_address.short_description = 'Shipping Address'

    def order_status(self, obj):
        if obj.complete:
            if obj.delivery and obj.delivery.delivered:  # Check if there is a related Delivery and if it's marked as delivered
                return 'Delivered'
            else:
                return 'In Transit'
        else:
            return 'Not Completed'
    order_status.short_description = 'Order Status'

    def get_queryset(self, request):
        # Filter completed orders
        return super().get_queryset(request).filter(complete=True)

# Register the custom CompletedOrderAdmin class for the Order model
admin.site.register(Order, CompletedOrderAdmin)

# Define a custom admin class for Delivery
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'delivery_date', 'delivered', 'carrier', 'tracking_number')
    list_filter = ('delivered',)
    search_fields = ('order__id',)

    def order_id(self, obj):
        return obj.order.id
    order_id.short_description = 'Order ID'

    def get_order_status(self, obj):
        if obj.delivered:
            return 'Delivered'
        else:
            return 'In Transit'
    get_order_status.short_description = 'Order Status'

# Register the custom DeliveryAdmin class for the Delivery model
admin.site.register(Delivery, DeliveryAdmin)

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percentage', 'start_date', 'end_date')

admin.site.register(Promotion, PromotionAdmin)

