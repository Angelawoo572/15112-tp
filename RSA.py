import random
import math
import time

# RSA key generation
# primality testing - miller-rabin test
def miller_rabin(n,s):
    """
    Miller-Rabin primality test.
    n: The number to be tested for primality.
    s: The number of iterations to run the test.
    Returns: True if n is almost surely prime, False if composite.
    """
    for i in range(s):
        a = random.randint(1,n-1)
        if witness(a,n):
            return 'composite' # definitely composite
    return 'prime' # probably prime

def witness(a,n):
    """
    Witness function to check if 'a' is a witness to the compositeness of 'n'.
    a: Random base value between 1 and n-1.
    n: The number to be tested.
    Returns: True if 'a' is a witness that 'n' is composite, False otherwise.
    """
    # Write n - 1 as 2^t * u, where u is odd, t>=1
    u = n - 1
    t = 0
    while u % 2 == 0:
        t += 1
        u //=2

    # modular exponentiation
    x_0 = modular_exponentiation(a, u, n)
    x_prev = x_0
    
    for i in range(1, t + 1):
        x_i = (x_prev * x_prev) % n
        if x_i == 1 and x_prev != 1 and x_prev != n - 1:
            return True
        x_prev = x_i
    if x_prev != 1:
        return True
    return False # a is a witness that n is composite

# Key generation public and private
def extended_gcd(a,b):
    if b == 0:
        return a,1,0
    else:
        d_prime, x_prime, y_prime = extended_gcd(b, a % b)
        d = d_prime
        x = y_prime
        y = x_prime - math.ceil(a // b) * y_prime
        return d, x, y
    
# Modular Exponentiation
def modular_exponentiation(a, b, n):
    c = 0
    d = 1
    b_binary = bin(b)[2:]  # Get the binary representation of b
    k = len(b_binary) - 1
    
    for i in range(k, -1, -1):
        c = 2 * c
        d = (d * d) % n
        if b_binary[i] == '1':
            c = c + 1
            d = (d * a) % n
    return d

def mod_inverse(e,phi):
    gcd,x,i = extended_gcd(e,phi)
    if gcd != 1:
        return None
    else:
        return x % phi
    
def rsa_key_generation(p,q):
    n = p*q
    phi = (p-1)*(q-1)
    e = 7
    d = mod_inverse(e,phi)
    return (e,n),(d,n) # public key (e, n), private key (d, n)

def rsa_encode(message, public_key):
    e, n = public_key
    encoded = [pow(ord(char), e, n) for char in message]
    return encoded

def rsa_decode(encoded_message, private_key):
    d,n = private_key
    decoded = ''.join([chr(pow(char, d, n)) for char in encoded_message])
    return decoded

# Attacker
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def pollard_rho(n):
    i = 1 # iteration counter
    xi = random.randint(0,n-1)
    y = xi
    k = 2

    while True:
        i += 1
        xi = (xi **2 -1) % n # pollard's rho heuristic, generates a pseudo-random sequence
        # calculate gcd of (y - xi) and n
        d = gcd(y-xi,n)

        if d != 1 and d != n:
            return d
        
        if i == k:
            y = xi
            k *=2

def calculate_pollard_rho_time(n):
    start_time = time.time()
    try:
        factor = pollard_rho(n)
    except Exception:
        factor = None
    end_time = time.time()

    elapsed_time = end_time-start_time
    return factor,elapsed_time

def attack_rsa(encoded_message,n):
    factor, elapsed_time = calculate_pollard_rho_time(n)
    if factor:
        print(f"A non-trivial factor of {n} is {factor}")
        # Once we have a factor, we can find p and q
        p = factor
        q = n // factor
        # Generate the private key
        _, private_key = rsa_key_generation(p, q)
        # Decode the message
        decoded_message = rsa_decode(encoded_message, private_key)
        print(f"Decoded message: {decoded_message}")
        print(f"Time taken to factor n: {elapsed_time:.6f} seconds")
    else:
        print("Failed to find a factor.")

# print (pollard_rho(15))
print(miller_rabin(11,5))