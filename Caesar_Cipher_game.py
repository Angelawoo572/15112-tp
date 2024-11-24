from cmu_graphics import *
import Caesar_Cipher

def getGameState(app):
    return app.gameState

def onAppStart(app):
    app.plaintext = ''
    app.ciphertext = ''
    app.key = 0
    app.userInput = ''
    app.isTypingPlaintext = False
    app.isTypingKey = False
    app.gameState = "waiting" # waiting, input_plaintext, input_key, verify

def onMousePress(app, mouseX, mouseY):
    # Restart if the user wants to try again
    if app.gameState == "try_again":
        app.gameState = "waiting"
        app.plaintext = ""
        app.ciphertext = ""
        app.key = 0
        app.userInput = ""
        app.isTypingPlaintext = False
        app.isTypingKey = False

def onKeyPress(app, key):
    if app.gameState == "waiting" and key == 'd':
        # Start the input process for plaintext
        app.gameState = "input_plaintext"
        app.isTypingPlaintext = True
        app.userInput = ""
    elif app.isTypingPlaintext:
        if key == 'enter':
            app.plaintext = app.userInput
            app.isTypingPlaintext = False
            app.gameState = "input_key"
            app.isTypingKey = True
            app.userInput = ""
        elif key == 'backspace':
            app.userInput = app.userInput[:-1]
        else:
            app.userInput += ' ' if key == 'space' else key if key.isalnum() or key in ['!', '?', '.', ','] else ''
    elif app.isTypingKey:
        if key.isdigit():
            app.userInput += key
        elif key == 'enter' and app.userInput.isdigit():
            app.key = int(app.userInput)
            app.ciphertext = Caesar_Cipher.encrypt(app.plaintext, app.key)
            app.gameState = "verify"
            app.isTypingKey = False
            app.userInput = ""
        elif key == 'backspace':
            app.userInput = app.userInput[:-1]
    elif app.gameState == "verify":
        if key == 'enter':
            if app.userInput == app.plaintext:
                app.gameState = "congratulations"
            else:
                app.gameState = "try_again"
        elif key == 'backspace':
            app.userInput = app.userInput[:-1]
        else:
            app.userInput += ' ' if key == 'space' else key

def redrawAll(app):
    if app.gameState == "waiting":
        drawLabel("Press 'd' to start the Caesar Cipher challenge!", 300, 200, size=16)
    elif app.gameState == "input_plaintext":
        drawLabel("Enter a short sentence (plaintext):", 200, 400, size=20)
        drawRect(100, 450, 300, 50, fill='white', border='black')
        drawLabel(app.userInput, 250, 480, size=20)
    elif app.gameState == "input_key":
        drawLabel("Enter a key (number):", 200, 400, size=20)
        drawRect(100, 450, 300, 50, fill='white', border='black')
        drawLabel(app.userInput, 250, 480, size=20)
    elif app.gameState == "verify":
        drawLabel("Letter List: " + Caesar_Cipher.letter_list, 300, 500, size=20)
        shifted_list = Caesar_Cipher.letter_list[app.key:] + Caesar_Cipher.letter_list[:app.key]
        drawLabel(f"Shifted List (Key = {app.key}): " + shifted_list, 300, 550, size=20)
        drawLabel("Ciphertext: " + app.ciphertext, 200, 600, size=20)
        drawLabel("Decrypted Message: ", 200, 220, size=16)
        drawRect(100, 230, 300, 50, fill='white', border='black')
        drawLabel(app.userInput, 250, 255, size=20)
    elif app.gameState == "congratulations":
        drawLabel("Congratulations! You decoded the message correctly!", 250, 200, size=16)
    elif app.gameState == "try_again":
        drawLabel(f"Incorrect! The key was {app.key}. Try again!", 200, 200, size=20)
        drawLabel("Click anywhere to try again.", 200, 230, size=15)

# def main():
#     runApp()

# main()