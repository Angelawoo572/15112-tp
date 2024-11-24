from cmu_graphics import *
import RSA
import random

# The Miller-Rabin primality test is used with increased iterations for better accuracy.
def generate_prime_numbers(range_start, range_end, count):
    primes = []
    while len(primes) < count:
        num = random.randint(range_start, range_end)
        if RSA.miller_rabin(num, 10) == 'prime':
            primes.append(num)
    return primes

def onAppStart(app):
    app.state = 'input'
    app.inputText = ''
    app.generatedNumbers = []
    app.selectedNumber = None
    app.selectedNumber2 = None
    app.attackTime = None
    app.encodedMessage = None
    app.decodedMessage = None

def onKeyPress(app, key):
    if app.state == 'input':
        if key == 'enter':
            app.generatedNumbers = generate_prime_numbers(10, 1000, 5)
            app.state = 'select'
        elif key == 'backspace':
            app.inputText = app.inputText[:-1]
        else:
            app.inputText += ' ' if key == 'space' else key if key.isalnum() or key in ['!', '?', '.', ','] else ''
    elif app.state == 'select':
        if key.isdigit():
            selected_index = int(key) - 1
            if 0 <= selected_index < len(app.generatedNumbers):
                app.selectedNumber = app.generatedNumbers[selected_index]
                # Ensure p and q are distinct
                while True:
                    q = random.choice(app.generatedNumbers)
                    if q != app.selectedNumber:
                        app.selectedNumber2 = q
                        break
                app.state = 'attack'
                app.attackTime = RSA.calculate_pollard_rho_time(app.selectedNumber * app.selectedNumber2)

def onMousePress(app, mouseX, mouseY):
    if app.state == 'attack':
        p = app.selectedNumber
        q = app.selectedNumber2
        n = p * q
        app.encodedMessage = RSA.rsa_encode(app.inputText, (7, n))
        _, elapsed_time = app.attackTime
        if elapsed_time < 5:  # Arbitrary threshold for demonstration
            _, private_key = RSA.rsa_key_generation(p, q)
            if private_key[0] is not None and private_key[1] is not None:
            # Explanation: The private key might fail if e (fixed as 7 here) is not coprime to φ(n) = (p-1)*(q-1).
            # If e and φ(n) have a common factor, the modular inverse does not exist, resulting in a failed key generation.
                try:
                    app.decodedMessage = RSA.rsa_decode(app.encodedMessage, private_key)
                except ValueError:
                    app.decodedMessage = "Decoding failed due to invalid characters."
            else:
                app.decodedMessage = "Private key generation failed."
        else:
            app.decodedMessage = "The prime you picked is secure! Pollard's Rho method couldn't factorize it quickly."
        app.state = 'result'

def redrawAll(app):
    if app.state == 'input':
        drawLabel('Enter a short message:', 400, 400, size=20)
        drawLabel(app.inputText, 400, 430, size=20)
    elif app.state == 'select':
        drawLabel('Pick a number for p:', 400, 400, size=20)
        for i, num in enumerate(app.generatedNumbers):
            drawLabel(f'{i + 1}: {num}', 400, 440 + i * 30, size=20)
    elif app.state == 'attack':
        factor, elapsed_time = app.attackTime
        drawLabel(f'Attempting to attack with Pollard Rho...', 400, 400, size=20)
        drawLabel(f'Time taken: {elapsed_time:.6f} seconds', 400, 430, size=20)
        if factor:
            drawLabel(f'Factor found: {factor}', 400, 460, size=20)
        else:
            drawLabel('No factor found.', 400, 460, size=20)
    elif app.state == 'result':
        drawLabel('Attack Result:', 400, 500, size=20)
        drawLabel(f'Encoded Message: {app.encodedMessage}', 400, 530, size=15)
        if app.decodedMessage:
            drawLabel(f'Decoded Message: {app.decodedMessage}', 400, 560, size=15)

# def main():
#     runApp()

# main()
