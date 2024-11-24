from cmu_graphics import *
import huffman_tree

def onAppStart(app):
    app.text = "electricalengineering"
    app.freq_table = huffman_tree.build_frequency_table(app.text)
    app.huffman_tree_root = huffman_tree.build_huffman_tree(app.freq_table)
    app.nodes = [huffman_tree.Node(char, freq, x=50 + i * 100, y=400) for i, (char, freq) in enumerate(app.freq_table.items())]
    app.drag_node = None
    app.merge_candidate = None
    app.huffman_codes = huffman_tree.generate_huffman_codes(app.huffman_tree_root)
    app.encoded_message = ''.join(app.huffman_codes[char] for char in app.text)
    app.decoded_message = ""
    app.needs_redraw = True
    app.player_tree_root = None
    app.phase = 'merging'  # Start in merging phase

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

def draw_tree(app, node, x, y, offset=100):
    if node is not None:
        drawCircle(x, y, 30, fill='lightblue')
        drawLabel(f"{node.char if node.char else ''}: {node.freq}", x, y, size=14, align='center', fill='black')
        if node.left:
            drawLine(x, y, x - offset, y + 80, fill='black')
            draw_tree(app, node.left, x - offset, y + 80, offset // 2)
        if node.right:
            drawLine(x, y, x + offset, y + 80, fill='black')
            draw_tree(app, node.right, x + offset, y + 80, offset // 2)

def perform_merge(app):
    if app.drag_node and app.merge_candidate:
        left, right = sorted([app.drag_node, app.merge_candidate], key=lambda x: x.freq)
        merged_node = huffman_tree.Node(None, left.freq + right.freq, (left.x + right.x) // 2, (left.y + right.y) // 2 - 50)
        merged_node.left = left
        merged_node.right = right
        app.nodes.remove(left)
        app.nodes.remove(right)
        app.nodes.append(merged_node)
        app.needs_redraw = True

        # Check if we have reached the root (only one node left)
        if len(app.nodes) == 1:
            app.player_tree_root = app.nodes[0]
            app.phase = 'decoding'  # Move to the decoding phase
            print("Tree fully constructed! Proceeding to decoding phase.")

def isPuzzleComplete(app):
    # Check if there is only one node left, which means the tree is complete
    return len(app.nodes) == 1 and app.phase == 'decoding'

def redrawAll(app):
    # Draw frequency table
    drawLabel(f"Frequency Table: {app.freq_table}", 20, 20, size=20, align='left', fill='black')

    if app.phase == 'merging':
        # Draw nodes for merging
        for node in app.nodes:
            color = 'lightgreen' if node.is_mergeable else 'lightblue'
            drawCircle(node.x, node.y, 30, fill=color)
            drawLabel(f"{node.char if node.char else ''}: {node.freq}", node.x, node.y, size=14, align='center', fill='black')

    elif app.phase == 'decoding':
        # Draw the current Huffman tree for decoding
        if app.player_tree_root:
            draw_tree(app, app.player_tree_root, 800, 100)

    # Display encoded and decoded messages
    drawLabel(f"Encoded Message: {app.encoded_message}", 500, 1000, size=15, align='center', fill='red')
    if app.decoded_message:
        drawLabel(f"Decoded Message: {app.decoded_message}", 200, 390, size=15, align='center', fill='purple')
        if app.decoded_message == app.text:
            drawLabel("Congratulations! You successfully decoded the message!", 400, 450, size=20, align='center', fill='green')
        else:
            drawLabel("Incorrect decoding. Press 'r' to restart.", 400, 450, size=20, align='center', fill='red')

def onKeyPress(app, key):
    if key == 'r':
        onAppStart(app)

# def main():
#     runApp()

# main()