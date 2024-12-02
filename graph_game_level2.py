from cmu_graphics import *
import dijkstra
import huffman_tree_game
import random

def getGameState(app):
    return app.winMessage

def buildGraph(app): # weighted
    graph = {}
    for row in range(app.boardSize):
        for col in range(app.boardSize):
            node = (row, col)
            graph[node] = {} # store both neighboring nodes and wights of the edges
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                newRow, newCol = row + dr, col + dc
                if 0 <= newRow < app.boardSize and 0 <= newCol < app.boardSize:
                    weight = random.randint(1, 10)  # Random positive weight for each edge
                    graph[node][(newRow, newCol)] = weight
    return graph

def onAppStart(app):
    app.box_image = "IMG_2619.PNG" # citation: http://xhslink.com/a/iksJYiyVbnQ0
    app.road_image = "IMG_2621.PNG" # citation: http://xhslink.com/a/G9LEu3TShnQ0
    app.pos_image = "IMG_2646.PNG" # citation: http://xhslink.com/a/2KfFN1pzsYP0


    huffman_tree_game.onAppStart(app)
    app.startScreen = True
    app.gameOver = False
    app.winMessage = None

    app.characterPackage = [] # store the player clicked char
    app.selectedWord = [] # store player choose chars

def setupLevel(app,level):
    if level == 1:
        app.boardSize = 5
        app.cost = 150
    elif level == 2:
        app.boardSize = 6
        app.cost = 250
    elif level == 3:
        app.boardSize = 7
        app.cost = 500

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
            distances, predecessors = dijkstra.dijkstra(app.graph, app.playerPos)
            path_to_new_pos = dijkstra.find_shortest_path(predecessors, newPos)
            if path_to_new_pos:
                cost_to_move = sum(app.graph[path_to_new_pos[i]][path_to_new_pos[i + 1]] for i in range(len(path_to_new_pos) - 1))
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

        elif key == 'w' and not app.gameOver:
            # Show the whole shortest path to find the entire target word
            app.currentHint,app.charPositions= hint_whole_graph(app.graph, app.playerPos, app.targetWord,app.board)
            app.hintActive = True
            app.currentCharIndex = 0
        elif key == 'space' and app.hintActive and app.currentCharIndex < len(app.charPositions) - 1:
            # Increment the current character index to highlight the next character in the path
            app.currentCharIndex += 1
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
        for row in range(app.boardSize):
            for col in range(app.boardSize):
                left = col * app.cellSize
                top = row * app.cellSize
                char = app.board[row * app.boardSize + col]
                # Draw the background image for the cell
                drawImage(app.box_image, left, top, width=app.cellSize, height=app.cellSize)

                if (row, col) == app.playerPos and not app.gameOver:
                    player_left = app.playerPos[1] * app.cellSize
                    player_top = app.playerPos[0] * app.cellSize
                    drawImage(app.pos_image, player_left, player_top, width=app.cellSize/2, height=app.cellSize/2)
                elif (row, col) in app.currentHint and app.hintActive:
                    if app.currentCharIndex >= 0 and app.currentCharIndex < len(app.charPositions) and (row, col) == app.charPositions[app.currentCharIndex]:
                        border_color = 'green'  # Highlight the next character in the path in green
                    else:
                        border_color = 'yellow'  # Highlight the path in yellow
                    drawRect(left, top, app.cellSize, app.cellSize, fill=None, border=border_color, borderWidth=5)  # Increase borderWidth for visibility
                drawLabel(char, left + app.cellSize / 2, top + app.cellSize / 2, size=16, bold=True)

        # Draw the weights for edges if weight hint is active
        if app.weightHintActive and not app.gameOver:
            weight_pos = set()
            for node, neighbors in app.graph.items(): # citation: I learned from https://www.w3schools.com/python/ref_dictionary_items.asp
                for neighbor, weight in neighbors.items():
                    if (node, neighbor) in weight_pos or (neighbor, node) in weight_pos:
                        continue  # Avoid drawing the same weight multiple times
                    weight_pos.add((node, neighbor))
                    x1, y1 = node[1] * app.cellSize + app.cellSize / 2, node[0] * app.cellSize + app.cellSize / 2
                    x2, y2 = neighbor[1] * app.cellSize + app.cellSize / 2, neighbor[0] * app.cellSize + app.cellSize / 2
                    midX, midY = (x1 + x2) / 2, (y1 + y2) / 2
                    drawLabel(f'{weight}', midX, midY, size=20, fill='mediumSlateBlue', bold=True)

        drawLabel(f'HP: {app.cost}', app.width - 80, 20, size=16, bold=True)

        if app.winMessage:
            drawLabel(app.winMessage, 1000, app.height-20, size=20, align='center', fill='black')

        drawLabel("Press 'n' for the next shortest path or 'w' for the whole shortest path. Press v to see the weight.", 1200, 40, size=20, fill='black')
        
        # Draw the character package at the bottom of the screen
        drawLabel("Collected Characters:", 850, 60, size=16, bold=True, fill='blue')
        for i, char in enumerate(app.characterPackage):
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