import random
def generate_otp():
    otp = ""
    for _ in range(8): # Use for loop
        otp += str(random.randint(0, 9)) # 
    return otp

def generate_rondom_password():
    password = ""
    for _ in range(8): # Use for loop
        password += str(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')) # 
    return password