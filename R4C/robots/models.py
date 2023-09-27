from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from .tasks import background_send_email


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)


#Signal to send emails
@receiver(post_save, sender=Robot)
def send_email_to_customers(sender, instance, created, **kwargs):
    if created:
        #Get orders waiting for the added robot
        list_orders = Order.objects.filter(robot_serial=instance.serial,
                                           is_wait=True).select_related('customer')
        
        if list_orders:
            list_email_for_sending = tuple(map(lambda order: order.customer.email, list_orders))
            model, version = instance.serial.split('-')
            
            #Run celery task
            background_send_email.delay(list_email_for_sending,
                                        model,
                                        version)
            
            #Switch 'is_wait' attribute on False for each order
            for order in list_orders:
                order.is_wait = False
                order.save()