from cmu_graphics import *
import dijkstra
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
    app.bg2 = "WechatIMG4218.jpg"

    app.gameOver = False
    app.winMessage = None
    app.hintMessage = None

    app.boardSize = 15
    app.cellSize = 60
    app.width = app.boardSize * app.cellSize
    app.height = app.boardSize * app.cellSize

    app.targetWord = "electricalengineering"
    app.graphNodes = list(app.targetWord)
    app.randomCharacters = [chr(random.randint(97, 122)) for _ in range(app.boardSize**2 - len(app.graphNodes))]
    app.board = random.sample(app.graphNodes + app.randomCharacters, app.boardSize**2) # store characters
    
    startIndex = app.board.index('e')
    app.playerPos = (startIndex // app.boardSize, startIndex % app.boardSize)

    app.cost = 350
    app.foundChars = []
    app.path = []
    app.graph = buildGraph(app) # store positions
    app.currentHint = []
    app.charPositions = []
    app.hintActive = False
    app.weightHintActive = False
    app.currentCharIndex = 0

def onMousePress(app, mouseX, mouseY):
    if app.gameOver:
        return

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
                if char == app.targetWord[len(app.foundChars)]:
                    app.foundChars.append(char)
                    app.currentCharIndex += 1

                if ''.join(app.foundChars) == app.targetWord:
                    app.winMessage = "You win!"
                    app.gameOver = True

    if app.cost <= 0 and not app.gameOver:
        app.winMessage = "Out of money! Game Over."
        app.gameOver = True

def onKeyPress(app,key):
    if key == 'h' and not app.gameOver:
        app.hintMessage = "Press 'n' for the next shortest path or 'w' for the whole shortest path. Press v to see the weight."
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
                    distances, predecessors = dijkstra.dijkstra(app.graph, app.playerPos)
                    if (row, col) in distances and distances[(row, col)] < min_distance:
                        min_distance = distances[(row, col)]
                        goal = (row, col)

            if goal:
                distances, predecessors = dijkstra.dijkstra(app.graph, app.playerPos)
                app.currentHint = dijkstra.find_shortest_path(predecessors, goal)
                app.hintActive = True
    elif key == "r":
        onAppStart(app)

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

    # Draw the weights for edges if weight hint is active
    if app.weightHintActive and not app.gameOver:
        weight_pos = set()
        for node, neighbors in app.graph.items():
            for neighbor, weight in neighbors.items():
                if (node, neighbor) in weight_pos or (neighbor, node) in weight_pos:
                    continue  # Avoid drawing the same weight multiple times
                weight_pos.add((node, neighbor))
                x1, y1 = node[1] * app.cellSize + app.cellSize / 2, node[0] * app.cellSize + app.cellSize / 2
                x2, y2 = neighbor[1] * app.cellSize + app.cellSize / 2, neighbor[0] * app.cellSize + app.cellSize / 2
                midX, midY = (x1 + x2) / 2, (y1 + y2) / 2
                drawLabel(f'{weight}', midX, midY, size=20, fill='mediumSlateBlue', bold=True)

    drawLabel(f'Cost: ${app.cost}', app.width - 80, 20, size=16, bold=True)

    if app.winMessage:
        drawLabel(app.winMessage, 1000, 650, size=20, align='center', fill='purple')

    if app.hintMessage:
        drawLabel(app.hintMessage, 1200, 1000, size=20, fill='black')


# def main():
#     runApp()


# main()