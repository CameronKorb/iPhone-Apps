import pygame

from random import randint



black = (0, 0, 0)

grey = (50, 50, 50)

turquoise = (45, 255, 254)

green = (133, 253, 49)

red   = (252, 13, 27)

blue  = (11, 36, 251)

purple = (252, 40, 252)

orange = (253, 164, 40)

yellow = (255, 253, 56)



BLOCK_SIZE = 35



def get_row_top_loc(rowNum):



	return rowNum * BLOCK_SIZE + 10





def get_col_left_loc(colNum):



	return colNum * BLOCK_SIZE + 10







class Game():



	def __init__(self, lateral_size, vertical_size):



		window_size = [lateral_size * BLOCK_SIZE + 20, vertical_size * BLOCK_SIZE + 20]

		self.screen = pygame.display.set_mode(window_size)	

		self.board = Board(lateral_size, vertical_size, self.screen)

		self.screen.fill(grey)



		pygame.init()

		pygame.display.set_caption("Tetris")

		clock = pygame.time.Clock()

		self.start(self.screen, self.board, 0, clock, False, False)

		



	def start(self,screen, board, moveCount, clock, stop, pause):



		self.board.drawEmptyBlocks()

		self.board.blockGroup.draw(self.screen)

		pygame.display.flip()



		speed = 200



		while stop == False:

			for event in pygame.event.get():

				if event.type == pygame.QUIT: #user clicks close

					stop = True

					pygame.quit()

				elif event.type == pygame.KEYDOWN:

					

					if event.key == pygame.K_RIGHT:

						self.board.updatePiecePosition(1,0)

					elif event.key == pygame.K_LEFT:

						self.board.updatePiecePosition(-1,0)

					elif event.key == pygame.K_UP:

						self.board.rotatePiece()

					elif event.key == pygame.K_DOWN:

						speed = 5

				elif event.type == pygame.KEYUP:



					if event.key == pygame.K_DOWN:

						speed = 200

						





			if stop == False and pause == False:



				

				self.board.nextStep()

				self.board.blockGroup.draw(self.screen)

				pygame.display.flip()

				pygame.time.wait(speed)

				clock.tick(60)

				self.board.updatePiecePosition(0,1)

				self.board.nextStep()

				self.board.blockGroup.draw(self.screen)

				pygame.display.flip()









class Board():



	def __init__(self, lateral_size, vertical_size, screen):

		

		self.vertical_size = vertical_size

		self.lateral_size = lateral_size

		self.blockGroup = pygame.sprite.RenderPlain()

		self.blocks = []

		self.screen = screen

		self.piecePosition = (4,0)

		self.cur_piece = I_Piece(self.piecePosition)

		self.nextPiece = S_Piece(self.piecePosition)

		self.updateNextPiece()





	def drawEmptyBlocks(self):





		for row in range(self.vertical_size):

			for column in range(self.lateral_size):

				block = Block(row,column)

				self.blockGroup.add(block)

				self.blocks.append(block)





	def nextStep(self):



		for index in self.cur_piece.get_OccupiedBlockIndexes(): # 

			prev_b = self.blocks[index[1] * self.lateral_size + index[0]]

			prev_b.set_occupation(False)



		self.cur_piece.updateOccupiedBlocks() # Updates current pieces occupation indexes







		for row in range(self.vertical_size):

			for column in range(self.lateral_size):



				b = self.blocks[row * self.lateral_size + column]

				if self.cur_piece.doBlockHasColor(row,column):

					b.changeColor(self.cur_piece.get_color())

					b.set_occupation(True)

				elif not b.get_occupation():

					b.changeColor(black)

					b.set_occupation(False)



		if self.checkGameOver():

			pygame.quit()





		if self.cur_piece.lowestBlockIndex() == self.vertical_size - 1 or self.checkBottomOfPiece(): # Checks if the piece reached the bottom

			self.piecePosition = self.cur_piece.set_position(4,0)

			self.cur_piece = self.nextPiece

			self.updateNextPiece()

			self.deleteLines()





	def updatePiecePosition(self,lateral_change,vertical_change):

		

		if not self.checkRightAndLeft(lateral_change) or not vertical_change == 0:

			self.piecePosition = self.cur_piece.updatePosition(lateral_change,vertical_change)

			self.nextStep()

			self.blockGroup.draw(self.screen)

			pygame.display.flip()

		

		



	def checkBottomOfPiece(self):

		for index in self.cur_piece.get_OccupiedBlockIndexes():

			next_b = self.blocks[(index[1] + 1) * self.lateral_size + index[0]]

			if next_b.get_occupation() and not ((index[0],(index[1] + 1)) in self.cur_piece.get_OccupiedBlockIndexes()):

				return True

		return False



	def checkRightAndLeft(self,change):

		for index in self.cur_piece.get_OccupiedBlockIndexes():

			next_b = self.blocks[index[1] * self.lateral_size + index[0] + change]

			if (next_b.get_occupation() and not ((index[0] + change,(index[1])) in self.cur_piece.get_OccupiedBlockIndexes())) or index[0] + change >= self.lateral_size or index[0] % self.lateral_size == 0:

				return True

		return False



	def deleteLines(self):

		shouldBeDeletedLines = []

		for row in range(self.vertical_size):

			shouldBeDeleted = True

			for column in range(self.lateral_size):

				b = self.blocks[row * self.lateral_size + column]

				if not b.get_occupation():

					shouldBeDeleted = False

			if shouldBeDeleted:

				shouldBeDeletedLines.append(row)



		for row in shouldBeDeletedLines:

			for column in range(self.lateral_size):

				b = self.blocks[row * self.lateral_size + column]

				b.set_occupation(False)

				b.changeColor(black)



		for deletedRowIndex in shouldBeDeletedLines:

			for row in reversed(range(0,deletedRowIndex)):

				for column in range(self.lateral_size):

					b = self.blocks[row * self.lateral_size + column]

					b_below = self.blocks[(row + 1) * self.lateral_size + column]

					b_below.set_occupation(b.get_occupation())

					b_below.changeColor(b.get_color())





	def checkGameOver(self):

		num = 0 # Number of rows that at least has one filled block

		

		for row in range(self.vertical_size):

			for column in range(self.lateral_size):



				b = self.blocks[row * self.lateral_size + column]

				if b.get_occupation():

					num += 1

					break

					

		if num == self.vertical_size:

			return True

		else:

			return False







	def rotatePiece(self):

		self.cur_piece.rotate()



	def updateNextPiece(self):

		ran = randint(0,6)

		if ran == 0:

			self.nextPiece = I_Piece(self.piecePosition)

		elif ran == 1:

			self.nextPiece = O_Piece(self.piecePosition)

		elif ran == 2:

			self.nextPiece = J_Piece(self.piecePosition)

		elif ran == 3:

			self.nextPiece = L_Piece(self.piecePosition)

		elif ran == 4:

			self.nextPiece = Z_Piece(self.piecePosition)

		elif ran == 5:

			self.nextPiece = S_Piece(self.piecePosition)

		elif ran == 6:

			self.nextPiece = T_Piece(self.piecePosition)



class Piece():



	def __init__(self, pos):

		self.position = pos

		self.color = black

		self.maxRotation = 0

		self.rotation = 0

		self.occupiedBlockIndexes = []



	def doBlockHasColor (self,row,col,position):

		pass



	def get_color(self):

		return self.color



	def rotate(self):

		if self.rotation + 1 <= self.maxRotation:

			self.rotation += 1

		else:

			self.rotation = 0



	def updatePosition(self,lateral_change,vertical_change):

		self.position = (self.position[0] + lateral_change, self.position[1] + vertical_change)

		return self.position



	def set_position(self,xPos,yPos):

		self.position = (xPos,yPos)

		return self.position



	def updateOccupiedBlocks(self):

		pass



	def get_OccupiedBlockIndexes(self):

		return self.occupiedBlockIndexes



	def doBlockHasColor (self,row,col):

		return (col, row) in self.occupiedBlockIndexes



	def lowestBlockIndex(self):

		lowest = 0

		for index in self.occupiedBlockIndexes:

			if lowest < index[1]:

				lowest = index[1]

		return lowest













class I_Piece (Piece):

	

	def __init__(self,pos):

		self.position = pos

		self.color = red

		self.maxRotation = 1

		self.rotation = 0

		self.occupiedBlockIndexes = []

		self.updateOccupiedBlocks()



	def updateOccupiedBlocks(self):

		x = self.position[0]

		y = self.position[1]

		if self.rotation == 0:

			self.occupiedBlockIndexes = [(x, y), (x, y + 1),(x, y + 2),(x, y + 3)]

		elif self.rotation == 1:

			self.occupiedBlockIndexes = [(x, y), (x + 1, y),(x + 2, y),(x + 3, y)]



	



class O_Piece (Piece):

	

	def __init__(self,pos):

		self.position = pos

		self.color = yellow

		self.maxRotation = 0

		self.rotation = 0

		self.occupiedBlockIndexes = []

		self.updateOccupiedBlocks()



	def updateOccupiedBlocks(self):

		x = self.position[0]

		y = self.position[1]

		if self.rotation == 0:

			self.occupiedBlockIndexes = [(x, y), (x, y + 1),(x + 1, y),(x + 1, y + 1)]





class J_Piece (Piece):

	

	def __init__(self,pos):

		self.position = pos

		self.color = blue

		self.maxRotation = 3

		self.rotation = 0

		self.occupiedBlockIndexes = []

		self.updateOccupiedBlocks()



	def updateOccupiedBlocks(self):

		x = self.position[0]

		y = self.position[1]

		if self.rotation == 0:

			self.occupiedBlockIndexes = [(x, y), (x + 1, y),(x + 2, y), (x + 2, y + 1)]

		elif self.rotation == 1:

			self.occupiedBlockIndexes = [(x + 1, y), (x + 1, y + 1), (x + 1, y + 2), (x, y + 2)]

		elif self.rotation == 2:

			self.occupiedBlockIndexes = [(x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x, y)]

		elif self.rotation == 3:

			self.occupiedBlockIndexes = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y)]





				

class L_Piece (Piece):

	

	def __init__(self,pos):

		self.color = orange

		self.maxRotation = 3

		self.rotation = 0

		self.position = pos

		self.occupiedBlockIndexes = []

		self.updateOccupiedBlocks()



	def updateOccupiedBlocks(self):

		x = self.position[0]

		y = self.position[1]

		if self.rotation == 0:

			self.occupiedBlockIndexes = [(x, y), (x + 1, y),(x + 2, y), (x, y + 1)]

		elif self.rotation == 1:

			self.occupiedBlockIndexes = [(x + 1, y), (x + 1, y + 1), (x + 1, y + 2), (x, y + 2)]

		elif self.rotation == 2:

			self.occupiedBlockIndexes = [(x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 2, y)]

		elif self.rotation == 3:

			self.occupiedBlockIndexes = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y + 2)]





class Z_Piece (Piece):

	

	def __init__(self,pos):

		self.color = green

		self.maxRotation = 1

		self.rotation = 0

		self.position = pos

		self.occupiedBlockIndexes = []

		self.updateOccupiedBlocks()



	def updateOccupiedBlocks(self):

		x = self.position[0]

		y = self.position[1]

		if self.rotation == 0:

			self.occupiedBlockIndexes = [(x, y), (x + 1, y), (x + 1, y + 1), (x + 2, y + 1)]

		elif self.rotation == 1:

			self.occupiedBlockIndexes = [(x, y + 1), (x, y + 2), (x + 1, y), (x + 1, y + 1)]





class S_Piece (Piece):

	

	def __init__(self,pos):

		self.position = pos

		self.color = purple

		self.maxRotation = 1

		self.rotation = 0

		self.occupiedBlockIndexes = []

		self.updateOccupiedBlocks()



	def updateOccupiedBlocks(self):

		x = self.position[0]

		y = self.position[1]

		if self.rotation == 0:

			self.occupiedBlockIndexes = [(x + 1, y), (x + 2, y), (x, y + 1), (x + 1, y + 1)]

		elif self.rotation == 1:

			self.occupiedBlockIndexes = [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y + 2)]







class T_Piece (Piece):

	

	def __init__(self,pos):

		self.position = pos

		self.color = turquoise

		self.maxRotation = 3

		self.rotation = 0

		self.occupiedBlockIndexes = []

		self.updateOccupiedBlocks()



	def updateOccupiedBlocks(self):

		x = self.position[0]

		y = self.position[1]

		if self.rotation == 0:

			self.occupiedBlockIndexes = [(x, y), (x + 1, y),(x + 2, y), (x + 1, y + 1)]

		elif self.rotation == 1:

			self.occupiedBlockIndexes = [(x + 1, y), (x + 1, y + 1), (x + 1, y + 2), (x, y + 1)]

		elif self.rotation == 2:

			self.occupiedBlockIndexes = [(x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 1, y)]

		elif self.rotation == 3:

			self.occupiedBlockIndexes = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y + 1)]







class Block(pygame.sprite.Sprite):



	def __init__(self,row,col):

		

		pygame.sprite.Sprite.__init__(self)

		self.row = row

		self.col = col

		self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])



		self.occupation = False

		

		self.color = black

		self.image.fill(self.color)

		self.rect = self.image.get_rect()

		self.rect.x = get_col_left_loc(col)

		self.rect.y = get_row_top_loc(row)



		pygame.draw.rect(self.image, grey, pygame.Rect(0,0,BLOCK_SIZE,BLOCK_SIZE), 1)



	def changeColor(self,color):

		self.color = color

		self.image.fill(self.color)

		pygame.draw.rect(self.image, grey, pygame.Rect(0,0,BLOCK_SIZE,BLOCK_SIZE), 1)



	def get_color(self):

		return self.color



	def get_occupation(self):

		return self.occupation



	def set_occupation(self,new_occupation):

		self.occupation = new_occupation





game = Game(10,20)



    