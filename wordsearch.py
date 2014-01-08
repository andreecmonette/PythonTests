import time, curses, random
LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'


def adjacent(coordTuple, width, height):
	x,y = coordTuple
	adjacentSet = set((x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1))
	if x == 0:
		adjacentSet.difference_update((x-1,y-1),(x-1,y),(x-1,y+1))
	elif x == width:
		adjacentSet.difference_update((x+1,y-1),(x+1,y),(x+1,y+1))
	if y == 0:
		adjacentSet.difference_update((x-1,y-1),(x,y-1),(x+1,y-1))
	elif y == height:
		adjacentSet.difference_update((x-1,y+1),(x,y+1),(x+1,y+1))
	return adjacentSet


class Game(object):
	def __init__(self, screen, gameWindow, height, width):
		self.over = False
		self.screen = screen
		self.gameWindow = gameWindow
		self.height = height-2
		self.width = width-2
		self.newBoard()
	
	def newBoard(self):
		self.charLocs = {}
		for letter in LOWERCASE:
			self.charLocs[letter] = set()
	
		self.squares = []		
		for i in xrange(self.width):
			self.squares.append([])
			for j in xrange(self.height):
				randChar = getRandChar()
				self.squares[i].append(randChar)
				self.charLocs[randChar].add((i,j))

				self.gameWindow.addch(i+1,j+1, ord(randChar))
		self.time = time.time()
		self.words = []
		self.selectedWord = 0

	def replaceChar(self, x, y):
		newChar = getRandChar()
		self.charLocs[self.squares[x][y]].remove((x,y))
		self.charLocs[newChar].add((x,y))
		self.squares[x][y] = newChar
		self.gameWindow.addch(x+1,y+1,ord(newChar))

	def restart(self):
		self.over = False
		self.newBoard()



	def extendWord(self):



def getRandChar():
	return LOWERCASE[random.randrange(26)]

def main(screen, gameWidth = 40, gameHeight = 20):
	screen.clear()
	scrWidth, scrHeight = screen.getmaxyx()
	finalHeight, finalWidth = min(gameHeight, scrHeight-2), min(gameWidth,scrWidth-2)
	curses.init_pair(1,2,3)
	gameWindow = screen.subwin(finalWidth,finalHeight,0,0)
	gameWindow.border()
	game = Game(screen, gameWindow, finalHeight, finalWidth)
	screen.nodelay(1)

	while not game.over:		
		game.time = time.time()
		curKey = screen.getch()
#		game.gameWindow.addch(2,3,ord('w'),curses.color_pair(1))
		game.gameWindow.refresh()
		if 0 < curKey < 256:
			curKey = chr(curKey)
			if curKey in LOWERCASE:


			if curKey == ' ':
				game.over = True

if __name__ == "__main__":
	curses.wrapper(main)