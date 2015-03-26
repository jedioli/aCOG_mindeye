#from Tkinter import *
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
import random

# ADDED FEATURES:
# - hard drop (press space)
# - rotate clockwise (Shift + Up)
# - (partially) object oriented

def drawGame():
	# draw orange rectangle in the background
	canvas.create_rectangle(0, 0, canvas.cellSize*(2+canvas.width), canvas.cellSize*(2+canvas.height), fill="orange")
	drawBoard() # draw the blue cells
	
def drawBoard():
	drawScore() # display the score
	board = canvas.board # variable to hold canvas.board
	for row in range(canvas.height): # for each row in the board:
		for col in range(canvas.width): # for each col in the row:
			drawCell(row, col, board[row][col]) # draw a cell with the color specified in board at (row,col)

# iterates to make the pieces fall
def timerFired():
	redrawAll() # redraw the game
	if canvas.isGameOver: # if game over:
		return # exit the function
	delay = 500 # delay interval
	canvas.after(delay, timerFired) #calls timerFired() every 500 milliseconds
	if not moveFallingPiece(1,0): # if piece can't legally move down any more:
		placeFallingPiece() # place the piece on the board
		newFallingPiece() # generate a new piece
	
# function to draw the last row of a piece if only the top row is available for piece placing
def drawLastRowOfPiece():
	pieceRow = canvas.fallingPiece[-1] # variable to hold last row of a piece
	colOffset = 0 # horizontal offset
	for cell in pieceRow: # for each cell in the row:
		if cell == True: # if cell isn't empty:
			row = 0	# only appears on top row
			col = canvas.fallingPieceCol + colOffset # position is horizontal location of piece + offset
			canvas.board[row][col] = canvas.pieceColor # set appropriate cell to piece's color
		colOffset += 1 # increment the horizontal offset
	
def placeFallingPiece():
	redrawAll() # redraw the game
	rowOffset = 0 # vertical offset of current cell in the piece
	topRowReached = False # tests if the top row of the board has been reached
	for pieceRow in canvas.fallingPiece: # for each row in the piece:
		colOffset = 0 # horizontal offset
		for cell in pieceRow: # for each cell in the row:
			if cell == True: # if cell isn't empty:
				row = canvas.fallingPieceRow + rowOffset # row position of cell
				col = canvas.fallingPieceCol + colOffset # col position of cell
				canvas.board[row][col] = canvas.pieceColor # set appropriate cell to piece's color
				if row in[0,1] or canvas.board[row][col] != canvas.pieceColor: # if the piece is near the top of the board:
					if row == 0: # if the piece is at the top of the board:
						topRowReached = True # the top of the board has been reached
					canvas.isGameOver = True # set game state to game over
					if not topRowReached: # if the top row has not been reached:
						drawLastRowOfPiece() # only draw the last row of the piece
			colOffset += 1 # increment the horizontal offset of the cell
		rowOffset += 1 # increment the vertical offset of the cell
	removeFullRows() # remove any rows that have been filled
	redrawAll() # redraw the game
			
def drawCell(row, col, color):
	board = canvas.board # variable to store canvas.board
	topX = canvas.cellSize*(1+col) # top horizontal position of each cell
	topY = canvas.cellSize*(1+row) # top vertical position of each cell
	bottomX = topX + canvas.cellSize # bottom horizontal position of each cell
	bottomY = topY + canvas.cellSize # bottom horizontal position of each cell
	thickness = (canvas.cellSize*0.02) # line thickness is 5% of box side length
	canvas.create_rectangle(topX,topY,bottomX,bottomY,fill="black") # create a black rectangle as an outline
	# create the cell and set it to the specified color
	canvas.create_rectangle(topX+thickness,topY+thickness,\
							bottomX-thickness,bottomY-thickness,fill=color)
	
def redrawAll():
	canvas.delete(ALL) # clear the canvas to get rid of lag
	drawGame() # draw the game

def keyPressed(event):
	if event.keysym == "Up": # if Up key pressed:
		rotateFallingPiece() # rotate the piece
	elif event.keysym == "Down": # if Down key pressed:
		if not moveFallingPiece(1,0): # move the piece down; if piece cannot move down any more:
			placeFallingPiece() # place the piece
	elif event.keysym == "Right": # if Right key pressed:
		moveFallingPiece(0,1) # move the piece right
	elif event.keysym == "Left": # if Left key pressed:
		moveFallingPiece(0,-1) # move the piece left
	if canvas.isGameOver: # if game over:
		if event.keysym == 'r': # if r key pressed:
			canvas.isGameOver = False # reset the game
			init() # start the game again
			
def hardDrop(event):
	while moveFallingPiece(1,0):
		pass

def rotateClockwise(event):
	for i in xrange(3):
		rotateFallingPiece()

def drawFallingPiece():
	redrawAll() # redraw everything
	board = canvas.board # variable to hold canvas.board
	rowOffset = 0 # vertical offset of each cell
	for pieceRow in canvas.fallingPiece: # for each row in the piece:
		colOffset = 0 # horizontal offset of each cell
		for cell in pieceRow: # for each cell in the row:
			if cell == True: # if cell not empty:
				row = canvas.fallingPieceRow + rowOffset # set row of the cell
				col = canvas.fallingPieceCol + colOffset # set col of the cell
				if not canvas.isGameOver: # if not game over:
					# draw the cell at the appropriate location
					drawCell(canvas.fallingPieceRow+rowOffset,canvas.fallingPieceCol+colOffset,canvas.pieceColor)
			colOffset += 1 # increment col offset
		rowOffset += 1 # increment row offset

def newFallingPiece():
	pieces = canvas.data["tetrisPieces"] # variable to store the tetris pieces
	canvas.fallingPiece = pieces[random.randint(0,len(pieces)-1)] # select a random piece
	colors = canvas.data["tetrisPieceColors"] # varaible to store the piece colors
	canvas.pieceColor = colors[pieces.index(canvas.fallingPiece)] # select the color corresponding to the correct piece
	canvas.fallingPieceRow = 0 # initial vertical position is at the top of the board
	canvas.fallingPieceCol = (canvas.width/2)-(len(canvas.fallingPiece[0])/2) # intial horizontal position is at the middle of the board
	canvas.fallingPieceWidth = len(canvas.fallingPiece[0]) # length of the piece
	canvas.fallingPieceHeight = len(canvas.fallingPiece) # height of the piece
	if not canvas.isGameOver: # if not game over:
		drawFallingPiece() # draw the piece
	
def moveFallingPiece(d_row, d_col):
	redrawAll() # redraw the game
	canvas.fallingPieceRow += d_row # increase the row location of the piece by specified amount
	canvas.fallingPieceCol += d_col # increase the col location of the piece by specified amount
	if not fallingPieceIsLegal(): # if the new position is not legal:
		# undo the position changes
		canvas.fallingPieceRow -= d_row
		canvas.fallingPieceCol -= d_col
		drawFallingPiece() # draw the piece
		return False # return False if piece cannot be moved there
	drawFallingPiece() # draw the piece
	return True # return True if piece can be moved there

# function to rotate a list counterclockwise
def invertList(origList):
	newList = zip(*origList)[::-1] # rotate the list
	return newList # return the list
	
# returns the coordinates of the center of a piece
def fallingPieceCenter():
	centerRow = canvas.fallingPieceRow+(canvas.fallingPieceHeight/2)
	centerCol = canvas.fallingPieceCol+(canvas.fallingPieceWidth/2)
	return (centerRow,centerCol)

# rotates a piece	
def rotateFallingPiece():
	redrawAll()
	# make copies of fallingPiece properties
	_fallingPiece = canvas.fallingPiece
	_fallingPieceRow = canvas.fallingPieceRow
	_fallingPieceCol = canvas.fallingPieceCol
	_fallingPieceWidth = canvas.fallingPieceWidth
	_fallingPieceHeight = canvas.fallingPieceHeight
	(oldCenterRow,oldCenterCol) = fallingPieceCenter() # define old center
	canvas.fallingPiece = invertList(canvas.fallingPiece) # rotate the piece
	# swap the height and width
	canvas.fallingPieceHeight = _fallingPieceWidth
	canvas.fallingPieceWidth = _fallingPieceHeight
	(newCenterRow,newCenterCol) = fallingPieceCenter() # find new center after rotating
	moveFallingPiece(oldCenterRow-newCenterRow,oldCenterCol-newCenterCol) # shift the piece to keep its center constant
	if not fallingPieceIsLegal(): # if piece cannot legally be moved there:
		moveFallingPiece(newCenterRow-oldCenterRow,newCenterCol-oldCenterCol) # shift the piece back
		# restore the width and height
		canvas.fallingPieceWidth = _fallingPieceWidth
		canvas.fallingPieceHeight = _fallingPieceHeight
		canvas.fallingPiece = _fallingPiece # set fallingPiece back to original shape (unrotated)
	drawFallingPiece() # draw the piece
	
def fallingPieceIsLegal():
	rowOffset = 0
	for pieceRow in canvas.fallingPiece: # for each row in fallingPiece:
		cellOffset = 0
		for cell in pieceRow: # for each cell:
			# location of the cell
			location = [canvas.fallingPieceCol+cellOffset, canvas.fallingPieceRow+rowOffset]
			if cell == True: # if cell isn't empty:
				if (location[0] >= canvas.width): # if cell is too far to the right:
					return False
				if (location[1] >= canvas.height): # if cell is too far down:
					return False
				if (location[0] < 0): # if cell is too far to the left
					return False
				if (location[1] <= 0): # if cell is too high:
					moveFallingPiece(1,0) # push the piece down
					return False
				# if destination cell is not empty:
				if canvas.board[location[1]][location[0]] != canvas.emptyColor:
					return False
			cellOffset += 1
		rowOffset += 1
	return True # return True if all edge cases pass

def removeFullRows():
	board = canvas.board
	fullRows = 0 # number of rows filled
	newRow = canvas.height - 1 # index of the bottom row
	for oldRow in range(canvas.height-1,-1,-1): # iterate from the bottom row of the board
		if canvas.emptyColor in board[oldRow]: # if row is not full:
			# copy row to newRow
			tempRow = board[oldRow]
			board[newRow] = tempRow
			newRow -= 1
		elif canvas.emptyColor not in board[oldRow]: # else if row is full:
			fullRows += 1 # increment the number of rows filled
			board.pop(oldRow) # remove the row
			oldRow -= 1 # decrement index to check same row again
			board.insert(0,[canvas.emptyColor]*canvas.width) # insert empty row on top of board
		#newRow -= 1 # decrease newRow by 1
	redrawAll() # redraw the game
	canvas.score += (fullRows**2) # add the square of the number of rows filled to canvas.score

def drawScore():
	if not canvas.isGameOver: # if game not over:
		output = "Score: " + str(canvas.score) # display score
	else: # if game over:
		output = "GAME OVER. Please press 'r'." # display GAME OVER and prompt user to press r to play again
	canvas.create_text(240, 25, text=output, fill="black", font="Ariel") # print the message
			
class pieces():
	iPiece = [
		[True,True,True,True]
	]
	jPiece = [
		[True,False,False],
		[True,True,True]
	]
	lPiece = [
		[False,False,True],
		[True,True,True]
	]
	oPiece = [
		[True,True],
		[True,True]
	]
	sPiece = [
		[False,True,True],
		[True,True,False]
	]
	tPiece = [
		[False,True,False],
		[True,True,True]
	]
	zPiece = [
		[True,True,False],
		[False,True,True]
	]
	pieceList = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
	def getAllPieces(self):
		return pieces.pieceList

def init():
	canvas.board = [[canvas.emptyColor]*canvas.width for row in range(canvas.height)] # define the game board
	drawGame() # draw the game
	tetrisPiecesObject = pieces() # store tetris pieces in tetrisPieces
	tetrisPieces = tetrisPiecesObject.getAllPieces()
	tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"] # store piece colors
	canvas.data = {} # dictionary to store pieces and colors
	canvas.data["tetrisPieces"] = tetrisPieces # list of pieces
	canvas.data["tetrisPieceColors"] = tetrisPieceColors # list of colors
	canvas.score = 0 # initial score is 0
	newFallingPiece() # create a new piece
	timerFired() # initialize timerFired()

def run(rows, cols):
    # create the root and the canvas
	root = Tk()
	cellSize = 40 # length of each cell
	# adjust canvas size based on cell size
	global canvas
	canvas = Canvas(root, width=(cellSize*(cols+2)), height=(cellSize*(rows+2)))
	canvas.pack()
	canvas.cellSize = cellSize # store cellSize in canvas
	root.resizable(width=0, height=0)
	canvas.emptyColor = "blue" # color of empty cells
	canvas.score = 0 # create score variable
	canvas.board = [[canvas.emptyColor]*cols for row in range(rows)] # list of lists; cells are blue by default
	canvas.width = cols # width = number of cols
	canvas.height = rows # height = number of rows
	canvas.isGameOver = False # gameOver is initially set to False
	init() # call the init function
	root.bind("<Key>", keyPressed) # bind key presses to commands defined in keyPressed()
	root.bind("<space>",hardDrop)
	root.bind("<Shift-Up>",rotateClockwise)
	root.mainloop()

run(15,10) # run the program