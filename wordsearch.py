import time, curses, random
LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'

WORDSCORES = dict(zip(LOWERCASE,
	[1,3,3,2,1,4,2,4,1,8,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10]))


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
	def __init__(self, screen, gameWindow, infoWindow, height, width):
		self.over = False
		self.screen = screen
		self.gameWindow = gameWindow
		self.infoWindow = infoWindow
		self.height = height-2
		self.width = width-2
		self.newBoard()
		self.scoredWords = []

	def newBoard(self):
		self.score = 0
		self.infoWindow.addstr(1,1,str(self.score))
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

	def scoreWord(self):
		self.scoredWords.append(self.currentWord)
		wordScore = 0
		for coords in self.words[self.selectedWord]:
			x,y = coords
			wordScore += WORDSCORES[self.squares[x][y]]
			self.replaceChar(x,y)

		self.score += wordScore
		self.infoWindow.addstr(1,1,str(self.score))
		self.infoWindow.addstr(2,1,self.currentWord)
		self.words = []
		self.selectedWord = 0
		self.wordBuffer = []
		self.currentWord = ''
		self.highlightWords()	
		self.infoWindow.refresh()
		


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
		
		if not 0 <= len(self.wordBuffer) <= 1:
			self.wordBuffer.pop()
			self.words = self.wordBuffer[-1]

		elif len(self.wordBuffer) == 1:
			self.wordBuffer = []
			self.words = []
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
			if self.selectedWord >= len(self.words):
				self.selectedWord = 0
			for letter in self.words[self.selectedWord]:
				x,y = letter
				self.gameWindow.chgat(x+1,y+1,1,curses.A_BOLD + curses.color_pair(2))

	def nextSelection(self):
		self.selectedWord += 1
		if self.selectedWord >= len(self.words):   #Something about preincrementing?
			self.selectedWord = 0
		self.highlightWords()

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
	infoWindow = screen.subwin(20,finalHeight,0,finalWidth+2)
	infoWindow.border()

	game = Game(screen, gameWindow, infoWindow, finalHeight, finalWidth)
	screen.nodelay(1)
	curses.curs_set(0)

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
				game.scoreWord()

			if curKey == '\t':
				game.nextSelection()


		if curKey == curses.KEY_BACKSPACE:
			game.deleteLetter()
if __name__ == "__main__":
	curses.wrapper(main)