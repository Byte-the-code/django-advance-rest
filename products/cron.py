from datetime import datetime, timedelta

from django.core.mail import send_mail

from products.models import Order

def order_reminder_sender():
    today = datetime.now()
    orders = Order.objects.filter(
        is_paid = False,
        remainder_sended = False,
        creation_date__gte = today - timedelta(hours=24),
        creation_date__lte = today - timedelta(hours=2)
    ).exclude(mercado_link = None)

    subject = 'Reminder! Complete your order'
    for order in orders:
        message = f'Hi {order.buyer.get_full_name()}\nYou have and order in pending state with the folowwing products:\n'
        for product in order.products.all():
            message += f'Name: {product.name}\n'
        
        message += f"You can make the payment with this link!!\n{order.mercado_link}\n\nThank you, ByteTheOrder"
        
        send_mail(
            subject,
            message,
            None,
            [order.buyer.email],
            fail_silently=False
        )
        
        order.remainder_sended = True
        order.save()

def delete_orders_unpaid_24_hours():
    today = datetime.now()
    Order.objects.filter(
        is_paid = False,
        creation_date__lte = today - timedelta(hours=24),
    ).delete()