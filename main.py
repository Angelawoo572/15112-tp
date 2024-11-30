from cmu_graphics import *
import huffman_tree_game
import graph_game_level1
import graph_game_level2

def onAppStart(app):
    # Shared state between screens
    app.url = "WechatIMG4203.jpg" # citation!!!
    app.image_player = "WechatIMG4206.jpg" # citations
    app.image_person = "WechatIMG4207.jpg"
    app.image_rescue1 = "WechatIMG4208.jpg"
    app.image_rescue2 = "WechatIMG4209.jpg"
    app.image_die = "WechatIMG4216.jpg"

    app.currentFloor = 1
    app.message = "Welcome to the Tower of Cipher Breaking!"

    app.playerX = 0 # Player's X-coordinate 600
    app.playerY = 0  # Player's Y-coordinate (floor level starts at bottom) 900
    app.doorX = 700  # Door X-coordinate
    app.doorY = 900  # Door Y-coordinate

    app.rescueX = 700  # Position of the person to rescue
    app.rescueY = 300  # Position on the top floor

    app.huffmanGameInitialized = False
    app.level1Initialized = False
    app.level2Initialized = False

    app.caesarGameInitialized = False
    app.rsaGameInitialized = False

    app.huffmanCompleted = False
    
    app.playerDirection = None

    # Initialize attributes for level1
    graph_game_level1.onAppStart(app)
    graph_game_level2.onAppStart(app)

############################################################
# Start Screen
############################################################
def start_redrawAll(app):
    drawLabel('Welcome to the Tower of Cipher Breaking', 800, 400, size=24, bold=True)
    drawLabel('Press space to begin!', 800, 450, size=16)
    drawLabel('Good luck solving puzzles!', 800, 500, size=16)

def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('tower')

############################################################
# Tower Screen
############################################################
def tower_onScreenActivate(app):
    # Reset tower state if necessary
    app.message = "Welcome to the Tower of Cipher Breaking!"
    if app.huffmanCompleted:
        app.playerY = 600  # Place the player at the Huffman floor after completing it
    elif app.currentFloor == 1:
        app.playerY = 900

def tower_redrawAll(app):
    # Draw the tower and current state
    drawImage(app.url, 400, 0, width=800, height=1000)
    drawImage(app.image_player, app.playerX, app.playerY, width=100, height=100)
    # Draw the person to rescue (always at the top of the tower)
    drawImage(app.image_person, app.rescueX, app.rescueY, width=80, height=80)
    drawLabel(app.message,1000, 50, size=16, bold=True)

def tower_onKeyPress(app, key):
    if key == 'left':
        app.playerX = max(400, app.playerX - 20)  # Boundaries to prevent moving off screen
    elif key == 'right':
        app.playerX = min(1150, app.playerX + 20)

    # Check if player overlaps with the door
    if abs(app.playerX - app.doorX) < 50 and abs(app.playerY - app.doorY) < 50:
        if app.currentFloor == 1 and not app.huffmanCompleted:
            moveToHuffmanGame(app)

def moveToHuffmanGame(app):
    app.message = "Entering Huffman Tree Puzzle..."
    setActiveScreen('huffman')

############################################################
# Huffman Room Screen
############################################################
def huffman_onScreenActivate(app):
    # Reset the score every time we enter the Huffman room
    if not app.huffmanGameInitialized:
        huffman_tree_game.onAppStart(app)
        app.huffmanGameInitialized = True

def huffman_redrawAll(app):
    huffman_tree_game.redrawAll(app)
    drawLabel("Welcome to the Huffman Coding Room!", 200, 100, size=20, bold=True,fill = "white")
    drawLabel("Solve the puzzle to proceed!", 200, 120, size=16,fill = "white")
    drawImage(app.image_player, app.playerX, app.playerY, width=100, height=100)

def huffman_onMousePress(app, mouseX, mouseY):
    huffman_tree_game.onMousePress(app, mouseX, mouseY)

def huffman_onKeyPress(app, key):
    if key == "left":
        app.playerDirection = 'left'  # Boundaries to prevent moving off screen
    elif key == 'right':
        app.playerDirection = 'right'
    elif key == 'up':
        app.playerDirection = 'up'
    elif key == 'down':
        app.playerDirection = 'down'
    else:
        huffman_tree_game.onKeyPress(app, key)

    if huffman_tree_game.app.decoded_message == app.text:
        # Check if player overlaps with the Huffman tree image
        if 850 - 50 < app.playerX < 850 + 50 and 200 <= app.playerY <= 1000:  # Refined overlap check
            setActiveScreen('rescue')

def huffman_onKeyRelease(app, key):
    if key in ['left', 'right', 'up', 'down']:
        app.playerDirection = None

def huffman_onStep(app):
    if app.playerDirection == 'left':
        app.playerX = max(10, app.playerX - 5)
    elif app.playerDirection == 'right':
        app.playerX = min(1300, app.playerX + 5)
    elif app.playerDirection == 'up':
        app.playerY = max(200, app.playerY - 5)
    elif app.playerDirection == 'down':
        app.playerY = min(1000, app.playerY + 5)

def huffman_onMouseMove(app, mouseX, mouseY):
    # Update player position to follow the mouse
    app.playerX = mouseX - 125  # Offset to center the image at the mouse position
    app.playerY = mouseY - 125

############################################################
# Rescue Screen
############################################################
def rescue_redrawAll(app):
    # Draw background and player
    drawImage(app.image_rescue1, 400, 0, width=800, height=1000)
    drawImage(app.image_player, app.playerX, app.playerY, width=250, height=250)
    
    # Draw labels for instructions, moved to the right white space
    drawLabel("Now you reconstruct the tree, there is a person trapped!", 1400, 100, size=20, fill='black')
    drawLabel("You have a fixed amount of money to form 'electricalengineering',", 1400, 150, size=20, fill='black')
    drawLabel("which is the message you just decoded.", 1400, 180, size=20, fill='black')
    drawLabel("If you cost all the money, the person will die.", 1400, 230, size=20, fill='black')

    # Draw level selection buttons (rectangles and labels)
    drawRect(150, 770, 200, 60, fill='lightblue', border='black')
    drawLabel("Choose Level 1", 250, 800, size=25, fill='black')

    drawRect(650, 770, 200, 60, fill='lightblue', border='black')
    drawLabel("Choose Level 2", 750, 800, size=25, fill='black')

    drawRect(1150, 770, 200, 60, fill='lightblue', border='black')
    drawLabel("Choose Level 3", 1250, 800, size=25, fill='black')

def rescue_onMouseMove(app, mouseX, mouseY):
    # Update player position to follow the mouse
    app.playerX = mouseX - 125  # Offset to center the image at the mouse position
    app.playerY = mouseY - 125  # Offset to center the image at the mouse position

def rescue_onMousePress(app, mouseX, mouseY):
    # Check for level selection clicks
    if 150 < mouseX < 350 and 770 < mouseY < 830:
        setActiveScreen('level1')
    
    elif 650 < mouseX < 850 and 770 < mouseY < 830:
        setActiveScreen('level2')

    elif 1150 < mouseX < 1350 and 770 < mouseY < 830:
        setActiveScreen('level3')

############################################################
# level1 Screen
############################################################
def level1_onScreenActivate(app):
    # Reset the score every time we enter the Huffman room
    if not app.level1Initialized:
        app.level1Initialized = True

def level1_redrawAll(app):
    graph_game_level1.redrawAll(app)
    if graph_game_level1.getGameState(app) == "You win!":
        drawImage(app.image_rescue2, 1000, 100, width=400, height=450)
        drawLabel("Press a to back to tower to transmit message",1000,800,fill = "black")
        drawLabel("Press b to try other levels, and you can directly rescue the person",800,850,fill = "black")
    elif graph_game_level1.getGameState(app) == "Out of money! Game Over.":
        drawImage(app.image_rescue1, 1000, 100, width=400, height=450)
        drawImage(app.image_die, 1050, 100, width=50, height=50)
    else:
        drawImage(app.image_rescue1, 1000, 100, width=400, height=450)

    drawImage(app.image_player, app.playerX, app.playerY, width=50, height=50)
    drawLabel("Press h for hint, and Press r to restart",1000,600,fill = "black")

def level1_onKeyPress(app, key):
    # Use the onKeyPress function from graph_game_level1 for hints and movement
    graph_game_level1.onKeyPress(app, key)
    if key == 'a' and graph_game_level1.getGameState(app) == "You win!":
        setActiveScreen('tower')
    if key == 'b' and graph_game_level1.getGameState(app) == "You win!":
        app.level1Initialized = False
        setActiveScreen('rescue')

def level1_onMousePress(app,mouseX,mouseY):
    graph_game_level1.onMousePress(app,mouseX,mouseY)

def level1_onMouseMove(app,mouseX,mouseY):
    app.playerX = mouseX
    app.playerY = mouseY

############################################################
# level2 Screen
############################################################
def level2_onScreenActivate(app):
    # Reset the score every time we enter the Huffman room
    if not app.level2Initialized:
        app.level2Initialized = True

def level2_redrawAll(app):
    graph_game_level2.redrawAll(app)
    if graph_game_level2.getGameState(app) == "You win!":
        drawImage(app.image_rescue2, 1000, 100, width=400, height=450)
        drawLabel("Press a to back to tower to transmit message",1000,800,fill = "black")
        drawLabel("Press b to try other levels, and you can directly rescue the person",800,850,fill = "black")
    elif graph_game_level2.getGameState(app) == "Out of money! Game Over.":
        drawImage(app.image_rescue1, 1000, 100, width=400, height=450)
        drawImage(app.image_die, 1050, 100, width=50, height=50)
    else:
        drawImage(app.image_rescue1, 1000, 100, width=400, height=450)

    drawImage(app.image_player, app.playerX, app.playerY, width=50, height=50)
    drawLabel("Press h for hint, and Press r to restart",1000,600,fill = "black")

def level2_onKeyPress(app, key):
    # Use the onKeyPress function from graph_game_level1 for hints and movement
    graph_game_level2.onKeyPress(app, key)
    if key == 'a' and graph_game_level2.getGameState(app) == "You win!":
        setActiveScreen('tower')
    if key == 'b' and graph_game_level2.getGameState(app) == "You win!":
        app.level1Initialized = True
        setActiveScreen('rescue')

def level2_onMousePress(app,mouseX,mouseY):
    graph_game_level2.onMousePress(app,mouseX,mouseY)

def level2_onMouseMove(app,mouseX,mouseY):
    app.playerX = mouseX
    app.playerY = mouseY

############################################################
# level3 Screen
############################################################






############################################################
# Main
############################################################

def main():
    runAppWithScreens(initialScreen='start')

main()