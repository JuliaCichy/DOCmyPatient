import random
import string
from users.models import Patient


def get_profile_reference():
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars) for i in range(30)))


def check_user_exists(ppsn):
    if Patient.objects.filter(ppsn=ppsn).exists():
        return False
    else:
        return True