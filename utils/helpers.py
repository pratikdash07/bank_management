# utils/helpers.py

import random
import string
from datetime import datetime

# ---------- ID Generators ----------

def generate_customer_id():
    """
    Generates a unique customer ID.
    Example: C1045
    """
    return "C" + str(random.randint(1000, 9999))


def generate_account_number():
    """
    Generates a unique account number.
    Example: A203456
    """
    return "A" + str(random.randint(100000, 999999))


def generate_pin():
    """
    Generates a 4-digit PIN.
    """
    return str(random.randint(1000, 9999))


# ---------- Date Utility ----------

def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
