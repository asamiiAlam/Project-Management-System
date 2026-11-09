#create a 6 digit OTP

def generate_otp():
    import random
    return str(random.randint(100000, 999999))
