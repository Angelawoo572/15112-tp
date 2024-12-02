from cmu_graphics import *
import huffman_tree
import dictionary
import random

def gettext(app):
    return app.text

def onAppStart(app):
    app.leaf = "IMG_2643.PNG" # citation: http://xhslink.com/a/ohXRoaaAYYP0
    app.showHint = False

    app.text = random.choice(dictionary.word_dictionary)
    app.freq_table = huffman_tree.build_frequency_table(app.text)
    app.huffman_tree_root = huffman_tree.build_huffman_tree(app.freq_table)
    app.tree_image = "IMG_2600.PNG" # citation: http://xhslink.com/a/ohXRoaaAYYP0
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

def decode_huffman(app):
    # Use the huffman_decode function from the huffman_tree module
    app.decoded_message = huffman_tree.huffman_decode(app.encoded_message, app.player_tree_root)
    app.needs_redraw = True

def draw_tree(app, node, x, y, offset=120):
    if node is not None:
        drawImage(app.leaf,x-20, y-15,width=50, height=50)
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
        drawLabel(f"Congratulations! {app.text}", 1400, 900, size=16)
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
    drawLabel(f"Encoded Message: {app.encoded_message}", 1200, 1000, size=15, align='center', fill='black')

def onKeyPress(app, key):
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

def onMousePress(app, mouseX, mouseY):
    if app.gameState == "try_again":
        # Check if the player clicked the "Try Again" button
        if 1350 <= mouseX <= 1450 and 950 <= mouseY <= 990:
            app.gameState = "verify"
            app.userInput = ""
            app.needs_redraw = True
    
    # Toggle hint visibility
    if 1250 <= mouseX <= 1400 and 720 <= mouseY <= 770:
        app.showHint = not app.showHint


# def main():
#     runApp()

# main()