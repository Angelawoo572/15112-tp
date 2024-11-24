from cmu_graphics import *
import huffman_tree_game
import Caesar_Cipher_game
import RSA_game

def onAppStart(app):
    # Shared state between screens
    app.currentFloor = 1
    app.message = "Welcome to the Tower of Cipher Breaking!"
    app.huffmanScore = 0
    app.huffmanGameInitialized = False
    app.caesarGameInitialized = False
    app.rsaGameInitialized = False

############################################################
# Start Screen
############################################################

def start_redrawAll(app):
    drawLabel('Welcome to the Tower of Cipher Breaking', 300, 160, size=24, bold=True)
    drawLabel('Press space to begin!', 300, 200, size=16)
    drawLabel('Good luck solving puzzles!', 300, 240, size=16)

def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('tower')

############################################################
# Tower Screen
############################################################

def tower_onScreenActivate(app):
    # Reset tower state if necessary
    app.message = "Welcome to the Tower of Cipher Breaking!"

def tower_redrawAll(app):
    # Draw the tower
    drawRect(150, 50, 100, 400, fill='darkKhaki', border='mediumAquamarine', borderWidth=2)
    for i in range(3):
        # Three floors in the tower
        y = 290 - i * 120
        fillColor = 'orchid' if i + 1 == app.currentFloor else 'cornSilk'
        drawRect(150, y, 100, 120, fill=fillColor, border='black')
        drawLabel(f'Floor {i+1}', 200, y + 60, size=20, align='center')

    # Draw details for the current floor
    if app.currentFloor == 1:
        drawLabel("Floor 1: Huffman Coding Room", 200, 500, size=20, bold=True)
        drawRect(170, 430, 60, 40, fill='gold', border='black')
        drawLabel("Enter", 200, 450, size=14)
    elif app.currentFloor == 2:
        drawLabel("Floor 2: Caesar Cipher Room", 200, 500, size=20, bold=True)
        drawRect(170, 430, 60, 40, fill='gold', border='black')
        drawLabel("Enter", 200, 450, size=14)
    elif app.currentFloor == 3:
        drawLabel("Floor 3: RSA Cryptography Room", 200, 500, size=20, bold=True)
        drawRect(170, 430, 60, 40, fill='gold', border='black')
        drawLabel("Enter", 200, 450, size=14)

    drawLabel(app.message, 200, 20, size=16, bold=True)

def tower_onMousePress(app, mouseX, mouseY):
    # Handle door clicks for different floors
    if app.currentFloor == 1 and 170 <= mouseX <= 230 and 430 <= mouseY <= 470:
        app.huffmanDoorClicked = True
        setActiveScreen('huffman')
    elif app.currentFloor == 2 and 170 <= mouseX <= 230 and 430 <= mouseY <= 470:
        setActiveScreen('caesar')
    elif app.currentFloor == 3 and 170 <= mouseX <= 230 and 430 <= mouseY <= 470:
        setActiveScreen('rsa')

def tower_onKeyPress(app, key):
    if key == 'a':
        setActiveScreen('start')

############################################################
# Huffman Room Screen
############################################################

def huffman_onScreenActivate(app):
    # Reset the score every time we enter the Huffman room
    app.huffmanScore = 0
    if not app.huffmanGameInitialized:
        huffman_tree_game.onAppStart(app)
        app.huffmanGameInitialized = True

def huffman_redrawAll(app):
    drawLabel("Welcome to the Huffman Coding Room!", 200, 100, size=20, bold=True)
    drawLabel("Solve the puzzle to proceed!", 200, 140, size=16)
    drawLabel(f"Score: {app.huffmanScore}", 200, 180, size=16)
    drawLabel("Press b to return to the tower", 200, 220, size=16)

    huffman_tree_game.redrawAll(app)

def huffman_onMousePress(app, mouseX, mouseY):
    huffman_tree_game.onMousePress(app, mouseX, mouseY)
    app.huffmanScore += 1

def huffman_onKeyPress(app, key):
    if key == 'b' and huffman_tree_game.isPuzzleComplete(app):
        app.message = "Great job! You have completed Floor 1. Head to Floor 2 to continue!"
        app.currentFloor = 2  # Unlock Floor 2
        setActiveScreen('tower')
    elif key == 'r':
        huffman_tree_game.onAppStart(app)

############################################################
# Caesar Cipher Room Screen
############################################################

def caesar_onScreenActivate(app):
    if not app.caesarGameInitialized:
        Caesar_Cipher_game.onAppStart(app)
        app.caesarGameInitialized = True

def caesar_redrawAll(app):
    drawLabel("Welcome to the Caesar Cipher Room!", 200, 100, size=20, bold=True)
    drawLabel("Solve the Caesar Cipher to proceed!", 200, 140, size=16)
    drawLabel("Press b to return to the tower", 200, 180, size=16)
    Caesar_Cipher_game.redrawAll(app)

def caesar_onMousePress(app, mouseX, mouseY):
    Caesar_Cipher_game.onMousePress(app, mouseX, mouseY)

def caesar_onKeyPress(app, key):
    if key == 'b' and Caesar_Cipher_game.getGameState(app) == "congratulations":
        app.message = "Great job! You have completed Floor 2. Head to Floor 3 to continue!"
        app.currentFloor = 3  # Unlock Floor 3
        setActiveScreen('tower')
    else:
        Caesar_Cipher_game.onKeyPress(app, key)

############################################################
# RSA Cryptography Room
############################################################
def rsa_onScreenActivate(app):
    if not app.rsaGameInitialized:
        RSA_game.onAppStart(app)
        app.rsaGameInitialized = True

def rsa_redrawAll(app):
    drawLabel("Welcome to the RSA Cryptography Room!", 200, 100, size=20, bold=True)
    drawLabel("Solve the RSA puzzle to complete the game!", 200, 140, size=16)
    RSA_game.redrawAll(app)

def rsa_onMousePress(app, mouseX, mouseY):
    RSA_game.onMousePress(app, mouseX, mouseY)

def rsa_onKeyPress(app, key):
    RSA_game.onKeyPress(app, key)
    if key == 'y':
        RSA_game.onAppStart(app)
    elif key == 'c':
        setActiveScreen('tower')


############################################################
# Main
############################################################

def main():
    runAppWithScreens(initialScreen='start')

main()
