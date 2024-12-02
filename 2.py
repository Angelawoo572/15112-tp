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
    app.box_image = "IMG_2619.PNG"
    app.startScreen = True
    app.gameOver = False
    app.winMessage = None
    app.characterPackage = []
    app.selectedWord = []

def setupLevel(app, level):
    if level == 1:
        app.boardSize = 5
        app.cost = 55
    elif level == 2:
        app.boardSize = 6
        app.cost = 60
    elif level == 3:
        app.boardSize = 7
        app.cost = 80

    app.lastkey = None

    app.cellSize = 750 // app.boardSize
    app.targetWord = huffman_tree_game.gettext(app)
    app.graphNodes = list(app.targetWord)
    app.randomCharacters = [chr(random.randint(97, 122)) for _ in range(app.boardSize**2 - len(app.graphNodes))]
    app.board = random.sample(app.graphNodes + app.randomCharacters, app.boardSize**2)
    
    startIndex = app.board.index(app.targetWord[0])
    app.playerPos = (startIndex // app.boardSize, startIndex % app.boardSize)

    app.foundChars = []
    app.path = []
    app.graph = buildGraph(app)
    app.currentHint = []
    app.charPositions = []
    app.hintActive = False
    app.currentCharIndex = 0

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
                    app.currentCharIndex = 0

        elif key == 'w' and not app.gameOver:
            app.currentHint, app.charPositions = find_whole_shortest_path(app.graph, app.board, app.playerPos, app.targetWord)
            app.hintActive = True
            app.currentCharIndex = 0

        elif key == 'space' and app.hintActive and app.currentCharIndex < len(app.charPositions) - 1:
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
                full_path.extend(path[1:])
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
        for row in range(app.boardSize):
            for col in range(app.boardSize):
                left = col * app.cellSize
                top = row * app.cellSize
                char = app.board[row * app.boardSize + col]
                if (row, col) == app.playerPos and not app.gameOver:
                    fill = 'blue'
                elif (row, col) in app.currentHint and app.hintActive:
                    if app.lastkey == 'n' and (row, col) in app.currentHint:
                        fill = 'yellow'  # Highlight the path in yellow when 'n' is pressed
                    elif app.currentCharIndex >= 0 and app.currentCharIndex < len(app.charPositions) and (row, col) == app.charPositions[app.currentCharIndex]:
                        fill = 'green'
                    else:
                        fill = 'lightGray'
                else:
                    fill = 'lightGray'
                drawRect(left, top, app.cellSize, app.cellSize, fill=fill, border='black')
                drawLabel(char, left + app.cellSize / 2, top + app.cellSize / 2, size=16, bold=True)

        drawLabel(f'HP: {app.cost}', app.width - 80, 20, size=16, bold=True)
        if app.winMessage:
            drawLabel(app.winMessage, 1000, app.height - 20, size=20, align='center', fill='black')

        drawLabel("Press 'n' for the next shortest path or 'w' for the whole shortest path.", 1200, 40, size=20, fill='yellow')
        drawLabel("Collected Characters:", 850, 60, size=16, bold=True, fill='blue')
        for i, char in enumerate(app.characterPackage):
            drawLabel(char, 950 + i * 20, 60, size=16, bold=True, fill='black')
        drawLabel("Selected Word:", 850, 80, size=16, bold=True, fill='green')
        drawLabel(''.join(app.selectedWord), 1200, 80, size=16, bold=True, fill='black')
        drawRect(700, app.height - 60, 80, 40, fill='lightPink', border='black')
        drawLabel("Undo", 740, app.height - 40, size=16, bold=True, fill='black')

        if app.gameOver:
            drawRect(500, app.height - 60, 100, 40, fill='lightGreen', border='black')
            drawLabel("Restart", 550, app.height - 40, size=16, bold=True, fill='black')

def main():
    runApp()

main()
