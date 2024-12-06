from cmu_graphics import *
import BFS
import random
import huffman_tree_game
from PIL import Image

def getCmuImage(path):
    pilImage = Image.open(path)
    cmuImage = CMUImage(pilImage)
    return cmuImage

def getGameState(app):
    return app.winMessage

def buildGraph(app):
    graph = {}
    for row in range(app.boardSize):
        for col in range(app.boardSize):
            node = (row, col)
            graph[node] = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                newRow, newCol = row + dr, col + dc
                if 0 <= newRow < app.boardSize and 0 <= newCol < app.boardSize:
                    graph[node].append((newRow, newCol))
    return graph

def onAppStart(app):
    huffman_tree_game.onAppStart(app)

    app.box_image = getCmuImage("IMG_2619.PNG") # citation: http://xhslink.com/a/iksJYiyVbnQ0
    app.road_image = getCmuImage("IMG_2621.PNG") # citation: http://xhslink.com/a/G9LEu3TShnQ0
    app.pos_image = getCmuImage("IMG_2646.PNG") # citation: http://xhslink.com/a/2KfFN1pzsYP0
    
    app.startScreen = True
    app.gameOver = False
    app.winMessage = None

    app.characterPackage = [] # store the player clicked char
    app.selectedWord = [] # store player choose chars

def setupLevel(app,level):
    if level == 1:
        app.boardSize = 5
        app.cost = 55
    elif level == 2:
        app.boardSize = 6
        app.cost = 60
    elif level == 3:
        app.boardSize = 7
        app.cost = 80

    app.cellSize = 750 // app.boardSize

    app.targetWord = huffman_tree_game.gettext(app)#"electricalengineering"
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
    app.currentCharIndex = 0

    # Cost settings
    min_moves = len(app.targetWord)  # Minimum moves to collect all characters (one per character)
    base_cost = min_moves * 3  # Base cost allows for exploration but requires efficiency

    # Add difficulty factor: Higher levels have tighter costs
    if level == 1:
        app.cost = base_cost + 15  # Extra buffer for easier completion without hints
    elif level == 2:
        app.cost = base_cost + 10  # Moderate buffer, player may need hints
    elif level == 3:
        app.cost = base_cost + 5  # Tight buffer, hints are likely needed for success

    # Adjust the cost so that using hints guarantees success
    # This ensures that with hints, the player can always reach all required nodes
    app.cost += len(app.targetWord) // 2  # Extra cost to account for optimal hint use

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

        if newPos in app.graph and app.cost > 0:
            level, parent = BFS.bfs(app.graph, app.playerPos)
            path_to_new_pos = BFS.find_shortest_path(parent, app.playerPos, newPos)
            if path_to_new_pos:
                cost_to_move = len(path_to_new_pos) - 1  # cost is equal to the number of edges
                if app.cost >= cost_to_move:
                    app.playerPos = newPos
                    app.cost -= cost_to_move
                    char = app.board[row * app.boardSize + col]
                    if len(app.foundChars) < len(app.targetWord) and char == app.targetWord[len(app.foundChars)]:
                        app.foundChars.append(char)
                        app.currentCharIndex += 1
                    app.characterPackage.append(char)  # Add character to package

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

def onKeyPress(app, key):
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
                        level, p = BFS.bfs(app.graph, app.playerPos)
                        if (row, col) in level and level[(row, col)] < min_distance:
                            min_distance = level[(row, col)]
                            goal = (row, col)

                if goal:
                    level, parent = BFS.bfs(app.graph, app.playerPos)
                    app.currentHint = BFS.find_shortest_path(parent, app.playerPos, goal)
                    app.hintActive = True
                    app.currentCharIndex = len(app.currentHint) - 1

        elif key == 'w' and not app.gameOver:
            # Show the whole shortest path to find the entire target word
            app.currentHint, app.charPositions = find_whole_shortest_path(app.graph, app.board, app.playerPos, app.targetWord)
            app.hintActive = True
            app.currentCharIndex = 0

def find_whole_shortest_path(graph, board, start_pos, target_word):
    curr_pos = start_pos
    full_path = []
    char_pos = []

    for char in target_word:
        if char in board:
            pos = board.index(char)
            row, col = int(pos // len(board) ** 0.5), int(pos % len(board) ** 0.5)
            goal = (row, col)

            level, parent = BFS.bfs(graph, curr_pos)
            path = BFS.find_shortest_path(parent, curr_pos, goal)
            if path:
                full_path.extend(path[1:])  # Skip the current position itself
                char_pos.append(goal)
                curr_pos = goal
    
    return full_path, char_pos

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
    # Step 1: Draw the background boxes
        for row in range(app.boardSize):
            for col in range(app.boardSize):
                left = col * app.cellSize
                top = row * app.cellSize
                char = app.board[row * app.boardSize + col]

                # Draw the box image first (background layer)
                drawImage(app.box_image, left, top, width=app.cellSize, height=app.cellSize)

        # Step 2: Draw roads to indicate the path (middle layer)
        if app.hintActive:
            for i in range(len(app.currentHint) - 1):
                start = app.currentHint[i]
                end = app.currentHint[i + 1]

                # Coordinates for start and end cells
                startX = start[1] * app.cellSize
                startY = start[0] * app.cellSize
                endX = end[1] * app.cellSize
                endY = end[0] * app.cellSize

                # Determine the direction of movement and draw the road image accordingly
                if start[0] == end[0]:  # Horizontal movement (same row)
                    # Draw horizontal road image between the cells
                    if start[1] < end[1]:  # Moving to the right
                        drawImage(app.road_image, startX + app.cellSize / 1.5, startY + app.cellSize / 4,
                                width=app.cellSize/1.5, height=app.cellSize / 2, rotateAngle=0)
                    else:  # Moving to the left
                        drawImage(app.road_image, endX + app.cellSize / 1.5, endY + app.cellSize / 4,
                                width=app.cellSize/1.5, height=app.cellSize / 2, rotateAngle=0)

                elif start[1] == end[1]:  # Vertical movement (same column)
                    # Draw vertical road image between the cells
                    if start[0] < end[0]:  # Moving down
                        drawImage(app.road_image, startX + app.cellSize / 4, startY + app.cellSize / 2,
                                width=app.cellSize / 2, height=app.cellSize/1.5, rotateAngle=90)
                    else:  # Moving up
                        drawImage(app.road_image, endX + app.cellSize / 4, endY + app.cellSize / 2,
                                width=app.cellSize / 2, height=app.cellSize/1.5, rotateAngle=90)

        # Step 3: Draw player and additional elements (top layer)
        for row in range(app.boardSize):
            for col in range(app.boardSize):
                left = col * app.cellSize
                top = row * app.cellSize
                char = app.board[row * app.boardSize + col]

                border_color = None
                if (row, col) == app.playerPos and not app.gameOver:
                    # Draw the player position image
                    player_left = app.playerPos[1] * app.cellSize
                    player_top = app.playerPos[0] * app.cellSize
                    drawImage(app.pos_image, player_left+app.cellSize/12, player_top + app.cellSize / 4,
                            width=app.cellSize / 2, height=app.cellSize / 2)
                elif (row, col) in app.currentHint and app.hintActive:
                    if (0 <= app.currentCharIndex < len(app.charPositions)) and (row, col) == app.charPositions[app.currentCharIndex]:
                        border_color = 'green'  # Highlight the next character in the path in green

                # Draw the cell border and label
                drawRect(left, top, app.cellSize, app.cellSize, fill=None, border=border_color, borderWidth=3)
                drawLabel(char, left + app.cellSize / 2, top + app.cellSize / 2, size=26, bold=True)

        
        drawLabel(f'HP: {app.cost}', app.width - 80, 20, size=16, bold=True)
        if app.winMessage:
            drawRect(840, app.height - 35, 350, 35, fill='white', border='black')
            drawLabel(app.winMessage, 1000, app.height-20, size=20, align='center', fill='black')

        drawLabel("Press 'n' for the next shortest path or 'w' for the whole shortest path.", 1200, 40, size=20, fill='yellow')
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