#! ./.venv/bin/python3
import uuid
from datetime import date 
from billing.models import Bill 

def generate_billing_number():
    billing = Bill.objects.order_by("id").last()
    number = 1
    if billing:
        number = int(billing.number) + 1
        
    return f"{number}".zfill(8)