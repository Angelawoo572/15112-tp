from cmu_graphics import *
from PIL import Image
import graph_game_level1
import graph_game_level2
import huffman_tree_game

def getCmuImage(path):
    pilImage = Image.open(path)
    cmuImage = CMUImage(pilImage)
    return cmuImage

def onAppStart(app):
    app.stepCount = 0
    app.walkerAnimationSpeed = 10
    app.score = 0
    # Shared state between screens
    app.url = "IMG_2645.PNG" # citation: http://xhslink.com/a/9cfN0svTeYP0
    app.walkerImages = [ # citation http://xhslink.com/a/tbU5KDDYmYP0
        "IMG_2634.PNG",  # Walker frame 1 
        "IMG_2635.PNG",  # Walker frame 2
        "IMG_2633.PNG"   # Walker frame 3
    ]
    app.walkerIndex = 0

    app.image_player = getCmuImage("IMG_2591.PNG") # citation: http://xhslink.com/a/2KfFN1pzsYP0 getCmuImage
    app.image_person = getCmuImage("IMG_2593.PNG") # citation: http://xhslink.com/a/j9syk8NQGYP0
    app.image_rescue1 = getCmuImage("IMG_2595.PNG")# citation for rescue1234: http://xhslink.com/a/eSq0dwgFAYP0
    app.image_rescue2 = getCmuImage("IMG_2628.PNG")
    app.image_rescue3 = getCmuImage("IMG_2597.PNG")
    app.image_rescue4 = getCmuImage("IMG_2629.PNG")
    app.image_end = getCmuImage("IMG_2610.PNG") # citation: http://xhslink.com/a/2KfFN1pzsYP0

    app.image_die = getCmuImage("IMG_2604.PNG") # citation: http://xhslink.com/a/PCQdSH05LYP0

    app.bg1 = getCmuImage("WechatIMG4237 1.06.25 AM.jpg") # citation: http://xhslink.com/a/a2qAJVdoTYP0

    app.message = "Welcome to the Tower of Cipher Breaking!"

    app.playerX = 0 # Player's X-coordinate 600
    app.playerY = 0  # Player's Y-coordinate (floor level starts at bottom) 900
    app.doorX = 700  # Door X-coordinate
    app.doorY = 900  # Door Y-coordinate

    app.huffmanGameInitialized = False
    app.level1Initialized = False
    app.level2Initialized = False
    app.endInitialized = False
    
    app.playerDirection = None

    # Initialize attributes for level1

############################################################
# Start Screen
############################################################
def start_redrawAll(app):
    drawImage(app.bg1, 0, 0, width=1800, height=1100)

    # Draw a rectangle to create a background for the instructions
    drawRect(300, 100, 1200, 550, fill='lightgrey', border='black', borderWidth=5)

    # Draw labels for instructions
    drawLabel('Welcome to the Tower of Cipher Breaking', 900, 150, size=24, bold=True, fill='black')
    drawLabel("In this game, you will embark on an exciting mission to rescue someone trapped in a mysterious tower.", 900, 200, size=20, fill='black')
    drawLabel("Solve puzzles and navigate obstacles to save the person at the top of the tower.", 900, 230, size=20, fill='black')
    drawLabel("How to Play:", 900, 280, size=24, bold=True, fill='black')
    drawLabel("Start the Game: Press the space bar to begin.", 900, 320, size=20, fill='black')
    drawLabel("Movement: Use arrow keys to move your character.", 900, 350, size=20, fill='black')
    drawLabel("Rescue Mission: Decode the message with limited HP to rescue the person.", 900, 380, size=20, fill='black')
    drawLabel("Pathfinding: Choose efficient paths to minimize costs and progress.", 900, 410, size=20, fill='black')
    drawLabel("Objective:", 900, 460, size=24, bold=True, fill='black')
    drawLabel("Rescue the Person: Solve puzzles and navigate levels to save them.", 900, 500, size=20, fill='black')
    drawLabel("Score Points: Earn points by solving puzzles. Reach 30 points to rescue the person!", 900, 530, size=20, fill='black')
    drawLabel("In the creation Mode, you can input the words to add to dictionary", 900, 560, size=20, fill='black')
    drawLabel("Press space to begin!", 900, 600, size=26, bold=True, fill='black')

def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('tower')

############################################################
# Tower Screen
############################################################
def tower_onScreenActivate(app):
    # Reset tower state if necessary
    app.playerX = 0
    app.playerY = 900

def tower_redrawAll(app):
    drawImage(app.bg1, 0, 0, width=1800, height=1100)
    # Draw the tower and current state
    drawImage(app.url, 400, 0, width=800, height=1000)
    if app.playerDirection == 'right':
        drawImage(app.walkerImages[app.walkerIndex], app.playerX, app.playerY, width=100, height=100)
    else:
        drawImage(app.image_player, app.playerX, app.playerY, width=100, height=100)
    # Draw the person to rescue (always at the top of the tower)
    drawImage(app.image_person, 750, 350, width=80, height=80)

    # Draw a rectangle on the left side to provide the story context about the Living Tree of Knowledge
    drawRect(20, 150, 450, 450, fill='lightblue', border='black', borderWidth=3)

    # Draw labels inside the left-side rectangle for story context
    drawLabel("The Living Tree of Knowledge", 245, 180, size=24, bold=True, fill='black')
    drawLabel("The tower is protected by a magical tree", 245, 220, size=18, fill='black')
    drawLabel("that holds the secret to rescue the person.", 245, 250, size=18, fill='black')
    drawLabel("The tree encodes messages using branches:", 245, 290, size=18, fill='black')
    drawLabel("left = 0, right = 1.", 245, 320, size=18, fill='black')
    drawLabel("The trapped person left a message, but the", 245, 360, size=18, fill='black')
    drawLabel("branches scattered into chaos.", 245, 390, size=18, fill='black')
    drawLabel("Reconstruct the tree to decode the message.", 245, 430, size=18, fill='black')
    drawLabel("Only by understanding the tree's logic", 245, 470, size=18, fill='black')
    drawLabel("can you unlock the secrets to rescue them.", 245, 500, size=18, fill='black')

    # Draw a rectangle on the right side to provide information about Huffman Tree
    drawRect(1250, 150, 450, 450, fill='lightyellow', border='black', borderWidth=3)

    # Draw labels inside the right-side rectangle for Huffman Tree information
    drawLabel("Tree Decoding Guide", 1475, 180, size=24, bold=True, fill='black')
    drawLabel("The person in the tower may have left", 1475, 220, size=18, fill='black')
    drawLabel("an encoded message using Huffman coding.", 1475, 250, size=18, fill='black')
    drawLabel("To decode the message:", 1475, 300, size=20, bold=True, fill='black')
    drawLabel("Follow the Path:", 1475, 340, size=18, fill='black')
    drawLabel("0 = Left, 1 = Right", 1475, 370, size=18, fill='black')
    drawLabel("Find a Letter:", 1475, 410, size=18, fill='black')
    drawLabel("Stop at a leaf to get a letter.", 1475, 440, size=18, fill='black')
    drawLabel("Repeat:", 1475, 480, size=18, fill='black')
    drawLabel("Continue until the message is complete.", 1475, 510, size=18, fill='black')


def tower_onKeyPress(app, key):
    if key in ['left','right','up','down']:
        app.playerDirection = key

def tower_onKeyRelease(app,key):
    if key in ['left', 'right', 'up', 'down']:
        app.playerDirection = None

def tower_onStep(app):
    app.stepCount += 5
    # Handle player movement based on direction
    if app.playerDirection == 'left':
        app.playerX = max(400, app.playerX - 5)  # Boundaries to prevent moving off screen
    elif app.playerDirection == 'right':
        app.playerX = min(1150, app.playerX + 5)
        if app.stepCount % app.walkerAnimationSpeed == 0:
            app.walkerIndex = (app.walkerIndex + 1) % len(app.walkerImages)
    elif app.playerDirection == 'up':
        app.playerY = max(0, app.playerY - 5)
    elif app.playerDirection == 'down':
        app.playerY = min(1000, app.playerY + 5)

    # Check if player overlaps with the door
    if abs(app.playerX - app.doorX) < 50 and abs(app.playerY - app.doorY) < 50:
        setActiveScreen('rescue')

############################################################
# Rescue Screen
############################################################
def rescue_redrawAll(app):
    drawImage(app.bg1, 0, 0, width=1800, height=1100)
    # Draw background and player
    drawImage(app.image_rescue1, 400, 0, width=800, height=1000)
    drawImage(app.image_player, app.playerX, app.playerY, width=250, height=250)
    
    # Draw labels for instructions, moved to the right white space
    drawRect(1170, 80, 460, 300, fill='lightyellow', border='black', borderWidth=3)
    drawLabel("Press 1 to save your score.", 1400, 100, size=16, fill='black')
    drawLabel("Winning a level adds 10 points.", 1400, 140, size=16, fill='black')
    drawLabel("Press 2 to switch to another Level or Restart to try again.", 1400, 180, size=16, fill='black')
    drawLabel("Be careful! If HP reaches 0, the person will not survive.", 1400, 220, size=16, fill='black')
    drawLabel("Level 1: Each step consumes the same amount of HP.", 1400, 260, size=16, fill='black')
    drawLabel("Can you make it in time?", 1400, 280, size=16, fill='black')
    drawLabel("Level 2: Different steps consume different amounts of HP.", 1400, 320, size=16, fill='black')
    drawLabel("Strategize to save the person!", 1400, 340, size=16, fill='black')

    # Draw level selection buttons (rectangles and labels)
    drawRect(150, 770, 200, 60, fill='lightblue', border='black')
    drawLabel("Choose Level 1", 250, 800, size=25, fill='black')

    # drawRect(650, 770, 200, 60, fill='lightblue', border='black')
    # drawLabel("Choose Level 3", 750, 800, size=25, fill='black')

    drawRect(1150, 770, 200, 60, fill='lightblue', border='black')
    drawLabel("Choose Level 2", 1250, 800, size=25, fill='black')

def rescue_onMouseMove(app, mouseX, mouseY):
    # Update player position to follow the mouse
    app.playerX = mouseX - 125  # Offset to center the image at the mouse position
    app.playerY = mouseY - 125  # Offset to center the image at the mouse position

def rescue_onMousePress(app, mouseX, mouseY):
    # Check for level selection clicks
    if 150 < mouseX < 350 and 770 < mouseY < 830:
        setActiveScreen('level1')
    
    # elif 650 < mouseX < 850 and 770 < mouseY < 830:
    #     setActiveScreen('level3')

    elif 1150 < mouseX < 1350 and 770 < mouseY < 830:
        setActiveScreen('level2')

############################################################
# level1 Screen
############################################################
def level1_onStep(app):
    huffman_tree_game.onStep(app)

def level1_onScreenActivate(app):
    graph_game_level1.onAppStart(app)
    # Reset the score every time we enter the Huffman room
    if not app.level1Initialized:
        app.level1Initialized = True

def level1_redrawAll(app):
    drawImage(app.bg1, 0, 0, width=1800, height=1100)
    drawLabel(f"Score: {app.score}",950,100,size=16, bold=True, fill='black')
    graph_game_level1.redrawAll(app)
    if app.score == 10:
        drawImage(app.image_rescue2, 0, app.height-350, width=300, height=350)
    elif app.score == 20:
        drawImage(app.image_rescue3, 0, app.height-350, width=300, height=350)
    elif app.score == 30:
        drawRect(750, 830, 500, 50, fill='blue', border='black', borderWidth=2)
        drawLabel("Congratulations! You rescue the person. Press r", 1000, 855, fill='yellow', size=20)
        drawImage(app.image_rescue4, 0, app.height-350, width=300, height=350)
    elif graph_game_level1.getGameState(app) == "Out of money! Game Over. Restart":
        drawImage(app.image_rescue1, 0, app.height-350, width=300, height=350)
        drawImage(app.image_die, 0, app.height-450, width=50, height=50)
    else:
        drawImage(app.image_rescue1, 0, app.height-350, width=300, height=350)

    # drawImage(app.image_player, app.playerX, app.playerY, width=50, height=50)

def level1_onKeyPress(app, key):
    # Use the onKeyPress function from graph_game_level1 for hints and movement
    graph_game_level1.onKeyPress(app, key)
    if key == '1' and graph_game_level1.getGameState(app) == "You win!":
        app.score += 10
    if key == '2' and graph_game_level1.getGameState(app) == "You win!":
        app.level1Initialized = False
        setActiveScreen('rescue')
    if key == 'r' and app.score == 30:
        app.level1Initialized = False
        setActiveScreen('end')

def level1_onMousePress(app,mouseX,mouseY):
    graph_game_level1.onMousePress(app,mouseX,mouseY)

# def level1_onMouseMove(app,mouseX,mouseY):
#     app.playerX = mouseX
#     app.playerY = mouseY

############################################################
# level2 Screen
############################################################
def level2_onStep(app):
    huffman_tree_game.onStep(app)

def level2_onScreenActivate(app):
    graph_game_level2.onAppStart(app)
    # Reset the score every time we enter the Huffman room
    if not app.level2Initialized:
        app.level2Initialized = True

def level2_redrawAll(app):
    drawImage(app.bg1, 0, 0, width=1800, height=1100)
    drawLabel(f"Score: {app.score}",950,100,size=16, bold=True, fill='black')
    graph_game_level2.redrawAll(app)
    if app.score == 10:
        drawImage(app.image_rescue2, 0, app.height-350, width=300, height=350)
    elif app.score == 20:
        drawImage(app.image_rescue3, 0, app.height-350, width=300, height=350)
    elif app.score == 30:
        drawRect(750, 830, 500, 50, fill='blue', border='black', borderWidth=2)
        drawLabel("Congratulations! You rescue the person. Press r", 1000, 855, fill='yellow', size=20)
        drawImage(app.image_rescue4, 0, app.height-350, width=300, height=350)
    elif graph_game_level2.getGameState(app) == "Out of money! Game Over. Restart":
        drawImage(app.image_rescue1, 0, app.height-350, width=300, height=350)
        drawImage(app.image_die, 0, app.height-450, width=50, height=50)
    else:
        drawImage(app.image_rescue1, 0, app.height-350, width=300, height=350)

    # drawImage(app.image_player, app.playerX, app.playerY, width=50, height=50)

def level2_onKeyPress(app, key):
    # Use the onKeyPress function from graph_game_level1 for hints and movement
    graph_game_level2.onKeyPress(app, key)
    if key == '1' and graph_game_level2.getGameState(app) == "You win!":
        app.score += 10
    if key == '2' and graph_game_level2.getGameState(app) == "You win!":
        app.level2Initialized = False
        setActiveScreen('rescue')
    if key == 'r' and app.score == 30:
        app.level2Initialized = False
        setActiveScreen('end')

def level2_onMousePress(app,mouseX,mouseY):
    graph_game_level2.onMousePress(app,mouseX,mouseY)

# def level2_onMouseMove(app,mouseX,mouseY):
#     app.playerX = mouseX
#     app.playerY = mouseY

############################################################
# end Screen
############################################################
def end_onScreenActivate(app):
    # Reset the score every time we enter the Huffman room
    if not app.endInitialized:
        app.endInitialized = True

def end_redrawAll(app):
    drawImage(app.bg1, 0, 0, width=1800, height=1100)
    drawImage(app.image_end,400, app.height-350, width=400, height=450)
    drawLabel("The End", 900, 100, size=50, fill='yellow')

    drawRect(800, 600, 200, 100, fill='gray', border='black', borderWidth=3)
    drawLabel("Restart", 900, 650, size=30, fill='black')

    drawImage(app.image_player, app.playerX, app.playerY, width=50, height=50)

def end_onMousePress(app, mouseX, mouseY):
    if 800 <= mouseX <= 1000 and 600 <= mouseY <= 700:
        onAppStart(app)
        setActiveScreen('start')

def end_onMouseMove(app,mouseX,mouseY):
    app.playerX = mouseX
    app.playerY = mouseY

############################################################
# Main
############################################################

def main():
    runAppWithScreens(initialScreen='start')

main()