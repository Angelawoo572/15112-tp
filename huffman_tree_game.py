from cmu_graphics import *
import huffman_tree
import dictionary
import random

def onAppStart(app):
    app.bg1 = "WechatIMG4213.jpg"
    app.text = random.choice(dictionary.word_dictionary)
    app.freq_table = huffman_tree.build_frequency_table(app.text)
    app.huffman_tree_root = huffman_tree.build_huffman_tree(app.freq_table)
    app.tree_image = "WechatIMG4211.jpg"
    # .items() is same like "(char, frequency[char])"
    # if I do not use enumerate:
    # i = 0
    # app.nodes = []
    # for char in app.freq_table:
    #     freq = app.freq_table[char]
    #     app.nodes.append(huffman_tree.Node(char, freq, x=50 + i * 100, y=400))
    #     i += 1
    app.nodes = [huffman_tree.Node(char, freq, x=50 + i * 100, y=400) for i, (char, freq) in enumerate(app.freq_table.items())]
    app.drag_node = None
    app.merge_candidate = None
    app.huffman_codes = huffman_tree.generate_huffman_codes(app.huffman_tree_root)
    app.encoded_message = ''.join(app.huffman_codes[char] for char in app.text)
    app.decoded_message = ""
    app.needs_redraw = True
    app.player_tree_root = None
    app.phase = 'merging'  # Start in merging phase

    app.generated_codes = app.huffman_codes  # Store generated codes for hint
    app.merge_history = []  # To keep track of merge history for undo


def handle_node_selection(app, mouseX, mouseY):
    # Handle selection of nodes for merging
    for node in app.nodes:
        if ((mouseX - node.x) ** 2 + (mouseY - node.y) ** 2) ** 0.5 <= 30:
            if app.drag_node is None:
                app.drag_node = node
                node.is_mergeable = True
            elif app.drag_node != node:
                app.merge_candidate = node
                node.is_mergeable = True
                perform_merge(app)
                app.drag_node = None
                app.merge_candidate = None
                break

def onMousePress(app, mouseX, mouseY):
    if app.phase == 'merging':
        handle_node_selection(app, mouseX, mouseY)
    elif app.phase == 'decoding':
        decode_huffman(app)

def decode_huffman(app):
    # Use the huffman_decode function from the huffman_tree module
    app.decoded_message = huffman_tree.huffman_decode(app.encoded_message, app.player_tree_root)
    app.needs_redraw = True

def draw_tree(app, node, x, y, offset=120):
    if node is not None:
        drawCircle(x, y, 30, fill='green')
        drawLabel(f"{node.char if node.char else ''}: {node.freq}", x, y, size=14, align='center', fill='brown')
        if node.left:
            drawLine(x, y, x - offset, y + 80, fill='brown')
            draw_tree(app, node.left, x - offset, y + 80, offset // 2)
        if node.right:
            drawLine(x, y, x + offset, y + 80, fill='brown')
            draw_tree(app, node.right, x + offset, y + 80, offset // 2)

def perform_merge(app):
    if app.drag_node and app.merge_candidate:
        left, right = sorted([app.drag_node, app.merge_candidate], key=lambda x: x.freq)
        """
        it's same with 
        if app.drag_node.freq <= app.merge_candidate.freq:
            left, right = app.drag_node, app.merge_candidate
        else:
            left, right = app.merge_candidate, app.drag_node
        """
        merged_node = huffman_tree.Node(None, left.freq + right.freq, (left.x + right.x) // 2, (left.y + right.y) // 2 - 50)
        merged_node.left = left
        merged_node.right = right

        # Store the merged nodes and merged_node to history for undo
        app.merge_history.append((merged_node, left, right))

        if left in app.nodes and right in app.nodes:
            app.nodes.remove(left)
            app.nodes.remove(right)
        app.nodes.append(merged_node)
        app.needs_redraw = True

        # Check if we have reached the root (only one node left)
        if len(app.nodes) == 1:
            app.player_tree_root = app.nodes[0]
            app.phase = 'decoding'  # Move to the decoding phase

def provide_hint(app):
    if app.phase == 'merging':
        # Hint about the next possible merge (e.g., the two nodes with the lowest frequency)
        if len(app.nodes) > 1:
            sorted_nodes = sorted(app.nodes, key=lambda x: x.freq)
            """
            it's same with 
            if app.drag_node.freq <= app.merge_candidate.freq:
                left, right = app.drag_node, app.merge_candidate
            else:
                left, right = app.merge_candidate, app.drag_node
            """
            hint_text = f"Hint: Try merging '{sorted_nodes[0].char if sorted_nodes[0].char else 'None'} ({sorted_nodes[0].freq})' and '{sorted_nodes[1].char if sorted_nodes[1].char else 'None'} ({sorted_nodes[1].freq})' as they have the lowest frequencies."
            drawLabel(hint_text, 400, 500, size=15, align='center', fill='white')
    elif app.phase == 'decoding':
        # Hint about the generated Huffman codes
        hint_text = "Generated Huffman Codes: " + ", ".join([f"'{char}': {code}" for char, code in app.generated_codes.items()])
        drawLabel(hint_text, 400, 500, size=15, align='center', fill='white')


def undo_merge(app):
    if app.merge_history:
        merged_node, left, right = app.merge_history.pop()
        left.is_mergeable = False
        right.is_mergeable = False
        if merged_node in app.nodes:
            app.nodes.remove(merged_node)
        if left not in app.nodes:
            app.nodes.append(left)
        if right not in app.nodes:
            app.nodes.append(right)
        app.needs_redraw = True

def redrawAll(app):
    drawImage(app.bg1,0,0,width = 1800,height = 1100)
    # Draw frequency table
    drawLabel(f"Frequency Table: {app.freq_table}", 20, 20, size=20, align='left', fill='yellow')

    if app.phase == 'merging':
        # Draw nodes for merging
        for node in app.nodes:
            color = 'lightgreen' if node.is_mergeable else 'lightblue'
            drawCircle(node.x, node.y, 30, fill=color)
            drawLabel(f"{node.char if node.char else ''}: {node.freq}", node.x, node.y, size=14, align='center', fill='black')

    elif app.phase == 'decoding':
        # Draw the current Huffman tree for decoding
        if app.player_tree_root:
            drawImage(app.tree_image, 850,200,width=500, height=800)
            draw_tree(app, app.player_tree_root, 1100, 400)

    # Display encoded and decoded messages
    drawLabel(f"Encoded Message: {app.encoded_message}", 500, 1000, size=15, align='center', fill='red')
    drawLabel("Press u to undo the action",500,950,size = 15,fill = "skyblue")
    if app.decoded_message:
        drawLabel(f"Decoded Message: {app.decoded_message}", 500, 900, size=15, align='center', fill='red')
        if app.decoded_message == app.text:
            drawLabel("Congratulations! You successfully decoded the message!", 400, 450, size=20, align='center', fill='white')
        else:
            drawLabel("Incorrect decoding. Press 'r' to restart.", 400, 150, size=20, align='center', fill='red')
            drawLabel("Hint: compare the tree you generated with the correct generated Huffman codes to try again.",420, 220, size=16, align='center', fill='pink')
            drawLabel("The left branch is 0, the right branch is 1",420,250,size = 16,align='center', fill='pink')

    # Provide hints
    provide_hint(app)

def onKeyPress(app, key):
    if key == 'r':
        onAppStart(app)
    elif key == 'u' and app.phase == 'merging':
        undo_merge(app)

def main():
    runApp()

main()