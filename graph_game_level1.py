from cmu_graphics import *
import BFS
import random
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
    app.bg2 = "WechatIMG4218.jpg" # citation
    app.gameOver = False
    app.winMessage = None
    app.hintMessage = None

    app.boardSize = 15
    app.cellSize = 52
    app.width = app.boardSize * app.cellSize
    app.height = app.boardSize * app.cellSize

    app.targetWord = "electricalengineering"
    app.graphNodes = list(app.targetWord)
    app.randomCharacters = [chr(random.randint(97, 122)) for _ in range(app.boardSize**2 - len(app.graphNodes))]
    app.board = random.sample(app.graphNodes + app.randomCharacters, app.boardSize**2) # store characters
    
    startIndex = app.board.index('e')
    app.playerPos = (startIndex // app.boardSize, startIndex % app.boardSize)

    app.cost = 120
    app.foundChars = []
    app.path = []
    app.graph = buildGraph(app) # store positions
    app.currentHint = []
    app.charPositions = []
    app.hintActive = False
    app.currentCharIndex = 0

def onMousePress(app, mouseX, mouseY):
    if app.gameOver:
        return

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
                if char == app.targetWord[len(app.foundChars)]:
                    app.foundChars.append(char)
                    app.currentCharIndex += 1

                if ''.join(app.foundChars) == app.targetWord:
                    app.winMessage = "You win!"
                    app.gameOver = True

    if app.cost <= 0 and not app.gameOver:
        app.winMessage = "Out of money! Game Over."
        app.gameOver = True

def onKeyPress(app, key):
    if key == 'h' and not app.gameOver:
        app.hintMessage = "Press 'n' for the next shortest path or 'w' for the whole shortest path."
    elif key == 'n' and not app.gameOver:
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

    elif key == 'w' and not app.gameOver:
        # Show the whole shortest path to find the entire target word
        app.currentHint, app.charPositions = find_whole_shortest_path(app.graph, app.board, app.playerPos, app.targetWord)
        app.hintActive = True
        app.currentCharIndex = 0
    elif key == 'space' and app.hintActive and app.currentCharIndex < len(app.charPositions) - 1:
        # Increment the current character index to highlight the next character in the path
        app.currentCharIndex += 1
    elif key == "r":
        onAppStart(app)


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
    drawImage(app.bg2,0,0,width = 1800,height = 1100)
    for row in range(app.boardSize):
        for col in range(app.boardSize):
            left = col * app.cellSize
            top = row * app.cellSize
            char = app.board[row * app.boardSize + col]
            if (row, col) == app.playerPos and not app.gameOver:
                fill = 'blue'
            elif (row, col) in app.currentHint and app.hintActive:
                if app.currentCharIndex >= 0 and app.currentCharIndex < len(app.charPositions) and (row, col) == app.charPositions[app.currentCharIndex]:
                    fill = 'green'  # Highlight the next character in the path in green
                else:
                    fill = 'yellow'  # Highlight the path in yellow
            else:
                fill = 'lightGray'
            drawRect(left, top, app.cellSize, app.cellSize, fill=fill, border='black')
            drawLabel(char, left + app.cellSize / 2, top + app.cellSize / 2, size=16, bold=True)
    
    drawLabel(f'Cost: ${app.cost}', app.width - 80, 20, size=16, bold=True)
    if app.winMessage:
        drawLabel(app.winMessage, 1000, 650, size=20, align='center', fill='purple')

    if app.hintMessage:
        drawLabel(app.hintMessage, 1200, 750, size=20, fill='black')

# def main():
#     runApp()

# main()