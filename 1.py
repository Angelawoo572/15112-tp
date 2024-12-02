from cmu_graphics import *
import BFS
import random
import huffman_tree_game

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

    app.box_image = "IMG_2619.PNG"  # citation: http://xhslink.com/a/iksJYiyVbnQ0
    app.road_image = "IMG_2621.PNG"  # citation: http://xhslink.com/a/G9LEu3TShnQ0

    app.startScreen = True
    app.gameOver = False
    app.winMessage = None

    app.characterPackage = []  # store the player clicked char
    app.selectedWord = []  # store player choose chars

def setupLevel(app, level):
    levelSettings = {1: (5, 55), 2: (6, 60), 3: (7, 80)}
    app.boardSize, app.cost = levelSettings.get(level, (5, 55))

    app.cellSize = 750 // app.boardSize
    app.targetWord = huffman_tree_game.gettext(app)
    app.graphNodes = list(app.targetWord)
    app.randomCharacters = [chr(random.randint(97, 122)) for _ in range(app.boardSize**2 - len(app.graphNodes))]
    app.board = random.sample(app.graphNodes + app.randomCharacters, app.boardSize**2)  # store characters

    startIndex = app.board.index(app.targetWord[0])
    app.playerPos = (startIndex // app.boardSize, startIndex % app.boardSize)

    app.foundChars = []
    app.path = []
    app.graph = buildGraph(app)  # store positions
    app.currentHint = []
    app.charPositions = []
    app.hintActive = False
    app.currentCharIndex = 0

def onMousePress(app, mouseX, mouseY):
    huffman_tree_game.onMousePress(app, mouseX, mouseY)
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
                    app.hintType = 'n'

        elif key == 'w' and not app.gameOver:
            # Show the next step in the shortest path to find the entire target word
            if not app.currentHint or app.currentCharIndex >= len(app.currentHint) - 1:
                app.currentHint, app.charPositions = find_whole_shortest_path(app.graph, app.board, app.playerPos, app.targetWord)
                app.currentCharIndex = 0
            else:
                app.currentCharIndex += 1
            app.hintActive = True
            app.hintType = 'w'

        elif key == 'space' and app.hintActive and app.currentCharIndex < len(app.currentHint) - 1:
            # Increment the current character index to highlight the next character in the path
            app.currentCharIndex += 1

def find_whole_shortest_path(graph, board, start_pos, target_word):
    curr_pos = start_pos
    full_path = []
    char_pos = []

    for char in target_word:
        if char in board:
            pos = board.index(char)
            row, col = pos // len(board) ** 0.5, pos % len(board) ** 0.5
            row, col = int(row), int(col)
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
    else:
        # Draw the nodes (boxes) and edges (lines)
        for node, neighbors in app.graph.items():
            row, col = node
            x, y = col * app.cellSize + app.cellSize // 2, row * app.cellSize + app.cellSize // 2

            # Draw edges (lines) connecting nodes
            for neighbor in neighbors:
                n_row, n_col = neighbor
                n_x, n_y = n_col * app.cellSize + app.cellSize // 2, n_row * app.cellSize + app.cellSize // 2
                drawLine(x, y, n_x, n_y, fill='black')

            # Draw the node (box)
            box_left = x - app.cellSize // 4
            box_top = y - app.cellSize // 4
            drawRect(box_left, box_top, app.cellSize // 2, app.cellSize // 2, fill='lightGray', border='black')

            # If the player is at this node, change the color
            if (row, col) == app.playerPos:
                drawRect(box_left, box_top, app.cellSize // 2, app.cellSize // 2, fill='blue', border='black')

            # Highlight the path if hint is active
            if app.hintActive and app.currentHint:
                if app.hintType == 'w':
                    # Highlight only the next step in the path in green
                    if app.currentCharIndex < len(app.currentHint):
                        next_step = app.currentHint[app.currentCharIndex]
                        nx, ny = next_step[1] * app.cellSize + app.cellSize // 2, next_step[0] * app.cellSize + app.cellSize // 2
                        drawCircle(nx, ny, 10, fill='green')
                else:
                    # Highlight the whole path in yellow
                    for i in range(len(app.currentHint) - 1):
                        x1, y1 = app.currentHint[i][1] * app.cellSize + app.cellSize // 2, app.currentHint[i][0] * app.cellSize + app.cellSize // 2
                        x2, y2 = app.currentHint[i + 1][1] * app.cellSize + app.cellSize // 2, app.currentHint[i + 1][0] * app.cellSize + app.cellSize // 2
                        drawLine(x1, y1, x2, y2, fill='yellow', lineWidth=3)

            # Draw the character in the box
            char = app.board[row * app.boardSize + col]
            drawLabel(char, x, y, size=16, bold=True)

        # Draw additional information such as HP, collected characters, etc.
        drawLabel(f'HP: {app.cost}', app.width - 80, 20, size=16, bold=True)
        if app.winMessage:
            drawLabel(app.winMessage, 1000, app.height - 20, size=20, align='center', fill='black')

        drawLabel("Press 'n' for the next shortest path or 'w' for the whole shortest path.", 1200, 40, size=20, fill='yellow')
        drawLabel("Collected Characters:", 850, 60, size=16, bold=True, fill='blue')
        for i, char in enumerate(app.characterPackage):
            drawLabel(char, 950 + i * 20, 60, size=16, bold=True, fill='black')

        drawLabel("Selected Word:", 850, 80, size=16, bold=True, fill='green')
        drawLabel(''.join(app.selectedWord), 1200, 80, size=16, bold=True, fill='black')

        # Draw the undo box
        drawRect(700, app.height - 60, 80, 40, fill='lightPink', border='black')
        drawLabel("Undo", 740, app.height - 40, size=16, bold=True, fill='black')

        if app.gameOver:
            drawRect(500, app.height - 60, 100, 40, fill='lightGreen', border='black')
            drawLabel("Restart", 550, app.height - 40, size=16, bold=True, fill='black')

def main():
    runApp()

main()



