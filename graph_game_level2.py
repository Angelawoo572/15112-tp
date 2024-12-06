from cmu_graphics import *
import dijkstra
import huffman_tree_game
import random
from PIL import Image

def calculateInitialCost(app):
    curr_pos = app.playerPos
    min_cost = 0

    for char in app.targetWord:
        if char in app.board:
            pos = app.board.index(char)
            row, col = pos // app.boardSize, pos % app.boardSize
            goal = (row, col)

            distances, predecessors = dijkstra.dijkstra(app.graph, curr_pos)
            if goal in distances:
                min_cost += distances[goal]
                curr_pos = goal

    # Add a buffer to the minimum cost to allow some flexibility
    buffer = min_cost * 0.5  # 50% extra cost buffer
    return int(min_cost + buffer)

def getCmuImage(path):
    pilImage = Image.open(path)
    cmuImage = CMUImage(pilImage)
    return cmuImage

def getGameState(app):
    return app.winMessage

def buildGraph(app): # weighted
    graph = {}
    for row in range(app.boardSize):
        for col in range(app.boardSize):
            node = (row, col)
            if node not in graph:
                graph[node] = {} # store both neighboring nodes and wights of the edges
            # Define all possible neighbors (up, down, left, right)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    newRow, newCol = row + dr, col + dc
                    if 0 <= newRow < app.boardSize and 0 <= newCol < app.boardSize:
                        neighbor = (newRow, newCol)

                        # Assign a weight if not already present in either direction
                        if neighbor not in graph or node not in graph[neighbor]:
                            weight = random.randint(1, 10)  # Random positive weight for each edge
                            
                            # Assign weight in both directions to maintain symmetry
                            if neighbor not in graph:
                                graph[neighbor] = {}
                            graph[node][neighbor] = weight
                            graph[neighbor][node] = weight

    return graph # symmetric

def onAppStart(app):
    app.box_image = getCmuImage("IMG_2619.PNG") # citation: http://xhslink.com/a/iksJYiyVbnQ0
    app.road_image = getCmuImage("IMG_2621.PNG") # citation: http://xhslink.com/a/G9LEu3TShnQ0
    app.pos_image = getCmuImage("IMG_2646.PNG") # citation: http://xhslink.com/a/2KfFN1pzsYP0

    huffman_tree_game.onAppStart(app)
    app.startScreen = True
    app.gameOver = False
    app.winMessage = None

    app.characterPackage = [] # store the player clicked char
    app.selectedWord = [] # store player choose chars

def setupLevel(app,level):
    if level == 1:
        app.boardSize = 5
        app.cost = 800
    elif level == 2:
        app.boardSize = 6
        app.cost = 800
    elif level == 3:
        app.boardSize = 7
        app.cost = 800

    app.cellSize = 750 // app.boardSize

    app.targetWord = huffman_tree_game.gettext(app)
    app.graphNodes = list(app.targetWord)
    app.randomCharacters = [chr(random.randint(97, 122)) for _ in range(app.boardSize**2 - len(app.graphNodes))]
    app.board = random.sample(app.graphNodes + app.randomCharacters, app.boardSize**2) # store characters
    
    startIndex = app.board.index(app.targetWord[0])
    app.playerPos = (startIndex // app.boardSize, startIndex % app.boardSize)

    app.foundChars = []
    app.path = []
    app.graph = buildGraph(app) # store positions
    app.currentHint = []
    app.charPositions = []
    app.hintActive = False
    app.weightHintActive = False
    app.currentCharIndex = 0

    app.hintType = None
    # Calculate minimum cost to reach all nodes of the target word
    app.cost = calculateInitialCost(app)

def onMousePress(app, mouseX, mouseY):
    huffman_tree_game.onMousePress(app,mouseX,mouseY)
    if app.startScreen:
        if 100 <= mouseX <= 200 and 150 <= mouseY <= 200:
            setupLevel(app, 1)  # Level 1
            app.startScreen = False
        elif 250 <= mouseX <= 350 and 150 <= mouseY <= 200:
            setupLevel(app, 2)  # Level 2
            app.startScreen = False
        elif 400 <= mouseX <= 500 and 150 <= mouseY <= 200:
            setupLevel(app, 3)  # Level 3
            app.startScreen = False
    elif app.gameOver:
        # Restart button
        if 500 <= mouseX <= 600 and app.height - 60 <= mouseY <= app.height - 20:
            onAppStart(app)  # Restart the game
    else:
        col = mouseX // app.cellSize
        row = mouseY // app.cellSize
        newPos = (row, col)

         # Check if new position is valid and player has enough cost to move
        if newPos in app.graph and app.cost > 0:
            distances, predecessors = dijkstra.dijkstra(app.graph, app.playerPos)
            if newPos in distances:
                path_to_new_pos = dijkstra.find_shortest_path(predecessors, newPos)
                if path_to_new_pos:
                    cost_to_move = sum(app.graph[path_to_new_pos[i]][path_to_new_pos[i + 1]] for i in range(len(path_to_new_pos) - 1))

                    if app.cost >= cost_to_move:
                        app.playerPos = newPos
                        app.cost -= cost_to_move
                        char = app.board[row * app.boardSize + col]
                        
                        # Update found characters and character package
                        if len(app.foundChars) < len(app.targetWord) and char == app.targetWord[len(app.foundChars)]:
                            app.foundChars.append(char)
                            app.currentCharIndex += 1
                        app.characterPackage.append(char)

        if app.cost <= 0 and not app.gameOver:
            app.winMessage = "Out of money! Game Over. Restart"
            app.gameOver = True

        # Click on the character package to select a character to form the word
        packageY = 60
        packageStartX = 950
        if packageY - 20 <= mouseY <= packageY + 20:
            for i, char in enumerate(app.characterPackage):
                # citation Note: learned from the website: https://www.geeksforgeeks.org/enumerate-in-python/
                charX = packageStartX + i * 20
                if charX - 10 <= mouseX <= charX + 10:
                    app.selectedWord.append(char)
                    break

        if ''.join(app.selectedWord) == app.targetWord:
            app.winMessage = "You win!"
            app.gameOver = True

        # remove the last selected character
        undoBoxX = 700
        undoBoxY = app.height - 60
        if undoBoxX <= mouseX <= undoBoxX + 80 and undoBoxY - 20 <= mouseY <= undoBoxY + 20:
            if app.selectedWord:
                app.selectedWord.pop()

def onKeyPress(app,key):
    if app.startScreen:
        huffman_tree_game.onKeyPress(app, key)
    elif not app.gameOver:
        huffman_tree_game.onKeyPress(app, key)
        if key == 'n' and not app.gameOver:
            app.currentHint = []
            if len(app.foundChars) < len(app.targetWord):
                char = app.targetWord[len(app.foundChars)]
                min_distance = float('inf')
                goal = None

                # Find the closest character matching the next target
                for pos, boardChar in enumerate(app.board):
                    # citation Note: learned from the website: https://www.geeksforgeeks.org/enumerate-in-python/
                    if boardChar == char:
                        row, col = (pos // app.boardSize, pos % app.boardSize)
                        distances, predecessors = dijkstra.dijkstra(app.graph, app.playerPos)
                        if (row, col) in distances and distances[(row, col)] < min_distance:
                            min_distance = distances[(row, col)]
                            goal = (row, col)

                if goal:
                    distances, predecessors = dijkstra.dijkstra(app.graph, app.playerPos)
                    app.currentHint = dijkstra.find_shortest_path(predecessors, goal)
                    app.hintActive = True
                    app.hintType = 'n'

        elif key == 'w' and not app.gameOver:
            # Show the whole shortest path to find the entire target word
            app.currentHint,app.charPositions= hint_whole_graph(app.graph, app.playerPos, app.targetWord,app.board)
            app.hintActive = True
            app.currentCharIndex = 0
            app.hintType = 'w'
        elif key == 'v' and not app.gameOver:
            # Activate weight hint
            app.weightHintActive = not app.weightHintActive

def hint_whole_graph(graph,start_pos,target_word,board):
    curr_pos = start_pos
    full_path = []
    char_pos = []

    for char in target_word:
        if char in board:
            pos = board.index(char)
            row, col = pos // len(board) ** 0.5, pos % len(board) ** 0.5
            row, col = int(row), int(col)
            goal = (row, col)

            distances, predecessors = dijkstra.dijkstra(graph, curr_pos)
            path = dijkstra.find_shortest_path(predecessors, goal)
            if path:
                full_path.extend(path[1:])  # Skip the current position itself
                char_pos.append(goal)
                curr_pos = goal
    
    return full_path,char_pos

def redrawAll(app):
    huffman_tree_game.redrawAll(app)
    if app.startScreen:
        drawLabel('Select Difficulty Level', 300, 50, size=30, align='center', bold=True)
        drawRect(100, 150, 100, 50, fill='lightBlue', border='black')
        drawLabel('level 1', 150, 175, size=20, align='center')
        drawRect(250, 150, 100, 50, fill='lightGreen', border='black')
        drawLabel('level 2', 300, 175, size=20, align='center')
        drawRect(400, 150, 100, 50, fill='lightCoral', border='black')
        drawLabel('level 3', 450, 175, size=20, align='center')

        drawRect(100, 230, 400, 50, fill='pink', border='black')
        drawLabel('From level 1 to 3, the number of islands increases.', 300, 255, size=15, align='center')
    else:
        # Draw the nodes (boxes) and edges (lines)
        for node, neighbors in app.graph.items(): # citation: I learned from https://www.w3schools.com/python/ref_dictionary_items.asp
            row, col = node
            x, y = col * app.cellSize + app.cellSize // 2, row * app.cellSize + app.cellSize // 2

            # Draw edges (images) connecting nodes
            for neighbor in neighbors:
                n_row, n_col = neighbor
                n_x, n_y = n_col * app.cellSize + app.cellSize // 2, n_row * app.cellSize + app.cellSize // 2

                # Determine the direction of the road image
                if row == n_row:  # Horizontal road
                    drawImage(app.road_image, min(x, n_x), y - app.cellSize // 4, width=abs(x - n_x), height=app.cellSize // 2)
                elif col == n_col:  # Vertical road
                    drawImage(app.road_image, x - app.cellSize // 8, min(y, n_y) + 30, width=app.cellSize // 3, height=abs(y - n_y)//1.5,rotateAngle = 110)


        if app.weightHintActive and not app.gameOver:
            weight_pos = set()
            for node, neighbors in app.graph.items():  # citation: I learned from https://www.w3schools.com/python/ref_dictionary_items.asp
                for neighbor, weight in neighbors.items():
                    # Avoid drawing the same weight multiple times for undirected edges
                    if (node, neighbor) in weight_pos or (neighbor, node) in weight_pos:
                        continue
                    weight_pos.add((node, neighbor))
                    x1, y1 = node[1] * app.cellSize + app.cellSize / 2, node[0] * app.cellSize + app.cellSize / 2
                    x2, y2 = neighbor[1] * app.cellSize + app.cellSize / 2, neighbor[0] * app.cellSize + app.cellSize / 2
                    midX, midY = (x1 + x2) / 2, (y1 + y2) / 2
                    if node[0] == neighbor[0]:  # Horizontal edge
                        drawLabel(f'{weight}', midX+15, midY, size=20, fill='mediumSlateBlue', bold=True)
                    elif node[1] == neighbor[1]:  # Vertical edge
                        drawLabel(f'{weight}', midX + 45, midY, size=20, fill='mediumSlateBlue', bold=True)

        # Draw nodes (boxes) with hint borders if applicable
        for node in app.graph:
            row, col = node
            x, y = col * app.cellSize + app.cellSize // 2, row * app.cellSize + app.cellSize // 2
            box_size = (app.cellSize * 3) // 4  # Increase the box size to 3/4 of cell size
            box_left = x - box_size // 2
            box_top = y - box_size // 2
            border_color = None
            drawImage(app.box_image, x - box_size // 2, y - box_size // 2, width=box_size, height=box_size)

            # Change the border color for hints
            if app.hintActive and app.currentHint:
                if app.hintType == 'n' and node in app.currentHint:
                    # Draw yellow border for the next shortest path hint
                    border_color = 'yellow'
                elif app.hintType == 'w':
                    # Highlight the current character in green
                    if app.currentCharIndex >= 0 and app.currentCharIndex < len(app.charPositions) and node == app.charPositions[app.currentCharIndex]:
                        border_color = 'green'

            drawRect(box_left, box_top, box_size, box_size, fill=None, border=border_color, borderWidth=2)

            # Change the fill color if the player is at this node
            if (row, col) == app.playerPos and not app.gameOver:
                    # Draw the player position image
                    player_left = app.playerPos[1] * app.cellSize
                    player_top = app.playerPos[0] * app.cellSize
                    drawImage(app.pos_image, player_left+app.cellSize/12, player_top + app.cellSize / 4,
                            width=app.cellSize / 2, height=app.cellSize / 2)

        # Draw the hint path if active for 'w'
        if app.hintActive and app.hintType == 'w' and len(app.currentHint) > 1:
            for i in range(len(app.currentHint) - 1):
                start = app.currentHint[i]
                end = app.currentHint[i + 1]
                startX = start[1] * app.cellSize + app.cellSize / 2
                startY = start[0] * app.cellSize + app.cellSize / 2
                endX = end[1] * app.cellSize + app.cellSize / 2
                endY = end[0] * app.cellSize + app.cellSize / 2
                drawLine(startX, startY, endX, endY, fill='yellow', lineWidth=2, arrowEnd=True)

        # Draw the character in the box (after everything else to ensure it is on top)
        for node in app.graph:
            row, col = node
            x, y = col * app.cellSize + app.cellSize // 2, row * app.cellSize + app.cellSize // 2
            char = app.board[row * app.boardSize + col]
            drawLabel(char, x, y, size=26, bold=True)

        drawLabel(f'HP: {app.cost}', app.width - 80, 20, size=16, bold=True)

        if app.winMessage:
            drawRect(840, app.height - 35, 350, 35, fill='white', border='black')
            drawLabel(app.winMessage, 1000, app.height-20, size=20, align='center', fill='black')

        drawLabel("Press 'n' for the next shortest path or 'w' for the whole shortest path. Press v to see the weight.", 1200, 40, size=20, fill='black')
        
        # Draw the character package at the bottom of the screen
        drawLabel("Collected Characters:", 850, 60, size=16, bold=True, fill='blue')
        for i, char in enumerate(app.characterPackage):
            # citation Note: learned from the website: https://www.geeksforgeeks.org/enumerate-in-python/
            drawLabel(char, 950 + i * 20, 60, size=16, bold=True, fill='black')

        # Draw the currently selected word
        drawLabel("Selected Word:", 850, 80, size=16, bold=True, fill='green')
        drawLabel(''.join(app.selectedWord),1200, 80, size=16, bold=True, fill='black')

        # Draw the undo box
        drawRect(700, app.height - 60, 80, 40, fill='lightPink', border='black')
        drawLabel("Undo", 740, app.height - 40, size=16, bold=True, fill='black')

        if app.gameOver:
            drawRect(500, app.height - 60, 100, 40, fill='lightGreen', border='black')
            drawLabel("Restart", 550, app.height - 40, size=16, bold=True, fill='black')


# def main():
#     runApp()


# main()