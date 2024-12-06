from cmu_graphics import *
import huffman_tree
import dictionary
import random
import time
from PIL import Image

def getCmuImage(path):
    pilImage = Image.open(path)
    cmuImage = CMUImage(pilImage)
    return cmuImage

def gettext(app):
    return app.text

def onAppStart(app):
    app.leaf = getCmuImage("IMG_2643.PNG") # citation: http://xhslink.com/a/ohXRoaaAYYP0
    app.leaf_change = getCmuImage('IMG_2700.PNG') # citation: http://xhslink.com/a/jKUcjV7s8P50
    app.showHint = False

    app.text = random.choice(list(dictionary.word_dictionary))
    app.freq_table = huffman_tree.build_frequency_table(app.text)
    app.huffman_tree_root = huffman_tree.build_huffman_tree(app.freq_table)
    app.tree_image = getCmuImage("IMG_2600.PNG") # citation: http://xhslink.com/a/ohXRoaaAYYP0
    # citations: https://www.w3schools.com/python/ref_dictionary_items.asp
    # *** 
    # I learned how it works from this website, did not copy, the citation is just the website I learned from, not directly use codes

    # .items() is same like "(char, frequency[char])"
    # if I do not use enumerate:
    # i = 0
    # app.nodes = []
    # for char in app.freq_table:
    #     freq = app.freq_table[char]
    #     app.nodes.append(huffman_tree.Node(char, freq, x=50 + i * 100, y=400))
    #     i += 1
    app.nodes = [huffman_tree.Node(char, freq, x=50 + i * 100, y=400) for i, (char, freq) in enumerate(app.freq_table.items())]
    app.huffman_codes = huffman_tree.generate_huffman_codes(app.huffman_tree_root)
    app.encoded_message = ''.join(app.huffman_codes[char] for char in app.text)
    app.decoded_message = ""
    app.needs_redraw = True
    app.gameState = "verify"
    app.userInput = ""

    app.node_images = {node: app.leaf for node in huffman_tree.collect_nodes(app.huffman_tree_root)}
    app.hint_boxes = []

    app.last_action_time = time.time()
    app.timer = 5

    app.creationMode = False
    app.newWordInput = ""

def decode_huffman(app):
    # Use the huffman_decode function from the huffman_tree module
    app.decoded_message = huffman_tree.huffman_decode(app.encoded_message, app.player_tree_root)
    app.needs_redraw = True

def draw_tree(app, node, x, y, offset=120):
    if node is not None:
        drawImage(app.node_images.get(node, app.leaf), x-20, y-15, width=50, height=50)
        drawLabel(f"{node.char if node.char else ''}: {node.freq}", x, y, size=14, align='center', fill='black')
        if node.left:
            drawLine(x, y, x - offset, y + 80, fill='brown')
            draw_tree(app, node.left, x - offset, y + 80, offset // 2)
        if node.right:
            drawLine(x, y, x + offset, y + 80, fill='brown')
            draw_tree(app, node.right, x + offset, y + 80, offset // 2)

def redrawAll(app):
    # Draw frequency table
    drawLabel(f"Frequency Table: {app.freq_table}", 1200, 20, size=20, fill='yellow')

    drawImage(app.tree_image, 850, 200, width=500, height=800)
    draw_tree(app, app.huffman_tree_root, 1100, 350)

    # Draw game states for user interaction
    if app.gameState == "verify":
        drawLabel("Enter the decoded message:", 1400, 800, size=20)
        drawRect(1250, 810, 300, 50, fill='lightyellow', border='black')
        drawLabel(app.userInput, 1400, 830, size=20)
    elif app.gameState == "congratulations":
        drawRect(1250, 880, 300, 40, fill='lightblue', border="black", borderWidth=2)
        drawLabel(f"Congratulations! {app.text}", 1400, 900, size=16)
        if not app.creationMode:
            drawRect(1250, 950, 300, 50, fill='lightgreen', border='black')
            drawLabel("Creation Mode", 1400, 975, size=18)
        else:
            drawRect(1250, 950, 300, 50, fill='lightyellow', border='black')
            drawLabel(app.newWordInput, 1400, 975, size=18)
    elif app.gameState == "try_again":
        drawLabel("Incorrect decoding. try again.", 1400, 900, size=15)
        drawRect(1350, 950, 100, 40, fill='lightblue', border='black')
        drawLabel("Try Again", 1400, 970, size=16)

    drawRect(1250, 720, 150, 50, fill='lightgreen', border='black')
    drawLabel("Hint", 1325, 740, size=18)

    if app.showHint:
        hintX = 1500  # X position for the hint column
        hintYStart = 200  # Starting Y position for the hint column
        rowHeight = 40  # Height for each hint row

        for i, (char, code) in enumerate(app.huffman_codes.items()):
            y = hintYStart + i * rowHeight
            drawRect(hintX - 10, y - 20, 200, 30, fill='lightgray', border='black')  # Background for each hint
            drawLabel(f"{char}: {code}", hintX + 90, y - 5, size=16, align='center', fill='darkblue')

    # Display encoded message
    drawRect(830, app.height-65, 850, 30, fill='lightblue', border='black')  # Add a rectangle to highlight the encoded message
    drawLabel(f"Encoded Message: {app.encoded_message}", 1200, 1030, size=16, fill='black',align = 'center')

    # Draw timer countdown
    drawLabel(f"Time left: {app.timer:.1f} seconds", 1400, 100, size=20, fill='yellow')

def onKeyPress(app, key):
    app.last_action_time = time.time() # reset
    if app.gameState == "verify":
        if key == 'enter':
            if app.userInput == app.text:
                app.gameState = "congratulations"
            else:
                app.gameState = "try_again"
        elif key == 'backspace':
            app.userInput = app.userInput[:-1]
        else:
            app.userInput += ' ' if key == 'space' else key
    elif app.creationMode:
        if key == 'enter':
            if app.newWordInput:
                # Add the new word to the dictionary
                dictionary.word_dictionary.add(app.newWordInput)
                app.creationMode = False
                app.newWordInput = ""
                app.needs_redraw = True
        elif key == 'backspace':
            app.newWordInput = app.newWordInput[:-1]
        else:
            app.newWordInput += ' ' if key == 'space' else key

def onMousePress(app, mouseX, mouseY):
    app.last_action_time = time.time() # reset
    if app.gameState == "try_again":
        # Check if the player clicked the "Try Again" button
        if 1350 <= mouseX <= 1450 and 950 <= mouseY <= 990:
            app.gameState = "verify"
            app.userInput = ""
            app.needs_redraw = True

    elif app.gameState == "congratulations":
        # Check if the player clicked the "Creation Mode" button
        if 1250 <= mouseX <= 1550 and 950 <= mouseY <= 1000:
            app.creationMode = not app.creationMode
            app.newWordInput = "" if app.creationMode else app.newWordInput
            app.needs_redraw = True
    
    # Toggle hint visibility
    if 1250 <= mouseX <= 1400 and 720 <= mouseY <= 770:
        app.showHint = not app.showHint
        if app.showHint:
            # Generate hint boxes only when hints are shown
            hintX = 1500  # X position for the hint column
            hintYStart = 200  # Starting Y position for the hint column
            rowHeight = 40  # Height for each hint row

            app.hint_boxes = []  # Clear hint boxes before drawing them

            for i, (char, code) in enumerate(app.huffman_codes.items()):
                y = hintYStart + i * rowHeight
                app.hint_boxes.append((hintX - 10, y - 20, hintX + 190, y + 10, char))  # Store bounding box and character

     # Check if a hint box is clicked
    if app.showHint:
        for (x1, y1, x2, y2, char) in app.hint_boxes:
            if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
                app.node_images = {node: app.leaf for node in app.node_images}
                target_node = next((node for node in app.node_images if node.char == char), None)
                if target_node:
                    app.node_images[target_node] = app.leaf_change
                    parents = []
                    huffman_tree.find_parent_nodes(app.huffman_tree_root, char, parents)
                    for parent in parents:
                        app.node_images[parent] = app.leaf_change
                app.needs_redraw = True
                break

def onStep(app):
    current_time = time.time()
    elapsed_time = current_time - app.last_action_time
    app.timer = max(0, 5 - elapsed_time)
    if elapsed_time >= 5:
        # Reset all node images to default after 5 seconds of inactivity
        app.node_images = {node: app.leaf for node in app.node_images}
        app.needs_redraw = True


# def main():
#     runApp()

# main()