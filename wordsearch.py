import time, curses, random
LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'




def adjacent(coordTuple, width, height):
	x,y = coordTuple
	adjacentSet = set([(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)])
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
		self.wordBuffer = []
		self.currentWord = ''

	def replaceChar(self, x, y):
		newChar = getRandChar()
		self.charLocs[self.squares[x][y]].remove((x,y))
		self.charLocs[newChar].add((x,y))
		self.squares[x][y] = newChar
		self.gameWindow.addch(x+1,y+1,ord(newChar))

	def restart(self):
		self.over = False
		self.newBoard()


	def extendWord(self, letter):
		if self.words == []:
			for firstletter in self.charLocs[letter]:
				self.words.append([firstletter,])
			if not self.words == []:	
				self.wordBuffer.append(self.words)
				self.currentWord = self.currentWord + letter
				self.highlightWords()
		else:
			newWords = []
	#		try:
			for word in self.words:
				for nextLetter in adjacent(word[-1],self.height,self.width).intersection(self.charLocs[letter]).difference(word):
					newWords.append(word + [nextLetter,])
	#		except:
	#			raise RuntimeError(word)
			if not newWords == []:
				self.words = newWords
				self.wordBuffer.append(self.words)	
				self.currentWord = self.currentWord + letter
				self.highlightWords()
		self.selectedWord = 0 # this should be whatever the index of the first returned word is


	def deleteLetter(self):
		self.wordBuffer.pop()
		self.words = self.wordBuffer[-1]
		self.highlightWords()

	def highlightWords(self):
		for i in xrange(self.width):
			for j in xrange(self.height):
				self.gameWindow.chgat(i+1,j+1, 1,curses.A_NORMAL)
		if not self.words == []:


			for word in self.words:
				for letter in word:
				
					x,y = letter

					self.gameWindow.chgat(x+1,y+1,1,curses.A_BOLD + curses.color_pair(1))
			for letter in self.words[self.selectedWord]:
				x,y = letter
				self.gameWindow.chgat(x+1,y+1,1,curses.A_BOLD + curses.color_pair(2))

	def nextSelection(self):
		self.selectedWord += 1
		if self.selectedWord >= len(self.words):   #Something about preincrementing?
			self.selectedWord = 0

def getRandChar():
	return LOWERCASE[random.randrange(26)]

def main(screen, gameWidth = 40, gameHeight = 20):
	screen.clear()
	scrWidth, scrHeight = screen.getmaxyx()
	finalHeight, finalWidth = min(gameHeight, scrHeight-2), min(gameWidth,scrWidth-2)
	curses.init_pair(1,curses.COLOR_YELLOW,curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
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
				game.extendWord(curKey)

			if curKey == '0':
				game.over = True

			if curKey == ' ':
				game.deleteLetter()

			if curKey == "\t":
				game.nextSelection()
				
if __name__ == "__main__":
	curses.wrapper(main)