from cmu_graphics import *

class Node:
    # Node class represents each character and its frequency in the Huffman tree
    def __init__(self,char,freq,x=0, y=0):
        self.char =char
        self.freq = freq
        self.left = None
        self.right = None
        self.x = x
        self.y = y
        self.is_mergeable = False

    def __lt__(self,other):
        return self.freq < other.freq #compare based on requency for sorting
    
# build frequency table
def build_frequency_table(text):
    frequency = dict()
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1
    return frequency

# build Huffman tree
def build_huffman_tree(frequency):
    # create a list of nodes for each character and its frequency
    nodes = [Node(char, frequency[char]) for char in frequency]
    # keep combining nodes until the root (one node) is left
    while len(nodes) >1:
        nodes.sort()
        left = nodes.pop(0) # smallest frequency
        right = nodes.pop(0) # second smallest frequency node

        # create a new merged node with combined frequency
        merged = Node(None,left.freq+right.freq)
        merged.left = left
        merged.right = right

        nodes.append(merged)
    return nodes[0] if nodes else None # return the root

# Collect only leaf nodes from the Huffman tree initially
def collect_leaf_nodes(node):
    nodes = []
    if node is not None:
        if node.char is not None:
            nodes.append(node)
        nodes+=collect_leaf_nodes(node.left)
        nodes+=collect_leaf_nodes(node.right)
    return nodes

# Collect all nodes from the Huffman tree
def collect_nodes(node, nodes=[]):
    if node is not None:
        nodes.append(node)
        collect_nodes(node.left, nodes)
        collect_nodes(node.right, nodes)
    return nodes

def find_parent_nodes(node,char,parents):
    if node is None:
        return False
    if node.char == char:
        return True
    if find_parent_nodes(node.left,char,parents) or find_parent_nodes(node.right,char,parents):
        parents.append(node)
        return True
    return False

# Huffman codes
def generate_huffman_codes(node, track = "",codeh = dict()):
    if node is not None:
        if node.char is not None: # if it's a leaf node 
            # since every leaf node is the char from the original text
            codeh[node.char] = track
        # traverse left chid
        generate_huffman_codes(node.left,track+"0",codeh) # left all 0
        # traverse right child
        generate_huffman_codes(node.right,track+"1",codeh)
    return codeh

# Encode the text using the generated Huffman codes
def huffman_encode(text, codeh):
    return "".join(codeh[char] for char in text)

# decode huffman encoded message
def huffman_decode(binary_code, root):
    decode_text = ""
    curr_node = root

    for bit in binary_code:
        if bit == "0":
            curr_node = curr_node.left # traverse left
        else: # 1
            curr_node = curr_node.right # traverse right

        # if leaf node is reached, add the character
        if curr_node.char is not None:
            decode_text += curr_node.char
            curr_node = root # go back to root for next character
    return decode_text

# # Test
# text = "electricalengineering"

# # Step 1: Build Frequency Table
# frequency = build_frequency_table(text)
# print("Frequency Table:")
# print(frequency)

# # Step 2: Build Huffman Tree
# root = build_huffman_tree(frequency)

# # Step 3: Generate Huffman Codes
# codes = generate_huffman_codes(root)
# print("\nGenerated Huffman Codes:")
# for char, code in codes.items():
#     print(f"'{char}': {code}")

# # Step 4: Encode the Text
# encoded_text = huffman_encode(text, codes)
# print("\nEncoded Text:")
# print(encoded_text)

# # Step 5: Decode the Encoded Text
# decoded_text = huffman_decode(encoded_text, root)
# print("\nDecoded Text:")
# print(decoded_text)

# # Verification
# print("\nVerification:")
# if decoded_text == text:
#     print("Success: The decoded text matches the original text.")
# else:
#     print("Error: The decoded text does not match the original text.")