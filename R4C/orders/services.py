from customers.models import Customer


def get_customer(email: str):
    customer, _ = Customer.objects.get_or_create(email=email)

    return customer