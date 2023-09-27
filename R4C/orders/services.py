from customers.models import Customer


def get_customer(email: str):
    customer = Customer.objects.get_or_create(email=email)

    return customer[0]