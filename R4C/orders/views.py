from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from robots.models import Robot

from .forms import OrderForm
from .models import Order
from .services import get_customer


def make_order(request: HttpRequest):
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            customer = get_customer(email=data['email'])
            
            if Robot.objects.filter(serial=data['serial_robot']).count() == 0:

                Order.objects.create(customer=customer,
                                     robot_serial=data['serial_robot'],
                                     is_wait=True)
                return HttpResponse('К сожалению, выбранного робота нет в наличии, мы сообщим Вам на почту, когда он появится')
            
            else:
                Order.objects.create(customer=customer,
                                     robot_serial=data['serial_robot'])
                return HttpResponse('Заказ оформлен')
            
        else:
            return render(request,
                          'orders/index.html',
                          context={'form': form})
            
    form = OrderForm()
    return render(request,
                  'orders/index.html',
                  context={'form': form})