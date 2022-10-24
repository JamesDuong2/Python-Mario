import pygame
import time
import random
from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, x, y, w, h, model):
		self.model = model
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.vertical_velocity = 0.0
		self.flip = False
		
		
	def update(self):
		pass
	def isMario(self):
		return False
	def amIBrick(self):
		return False
	def AmICoinBlock(self):
		return False
	def ImACoin(self):
		return False
	#checks collision 
	def checkCollision(self, model, mario, sprite):
		if(self.x + self.w <sprite.x):
			return False
		if(self.x > sprite.x + sprite.w):
			return False
		if(self.y + self.h < sprite.y):
			return False
		if(self.y > sprite.y +sprite.h):
			return False
		self.fixPosition(model, mario, sprite)
		return True
	


class Model():
	def __init__(self):
		
		self.cameraPosition = 0
		self.moveRight = False
		self.moveLeft = False
		#loads the images into model class
		self.bricks = pygame.image.load("brick.png")
		self.coinbricks = pygame.image.load("block1.png")
		self.emptycoin = pygame.image.load("block2.png")
		#Hardcode bricks and coin bricks into the sprite
		self.sprites = []
		self.mario = Mario(300, 0, 65, 80, self)
		
		self.sprites.append(self.mario)
		self.brick2 = Brick(560, 400, 100,100, self)
		self.sprites.append(self.brick2)
		self.brick3= Brick(500, 600, 100,100, self)
		self.sprites.append(self.brick3)
		self.brick4= Brick(700, 600, 100,100, self)
		self.sprites.append(self.brick4)
		self.bricks5 = Brick(1300, 600, 100, 100, self)
		self.bricks6 = Brick(1020, 300, 100, 100, self)
		self.bricks7 = Brick(1720, 300, 100, 100, self)
		self.sprites.append(self.bricks5)
		self.sprites.append(self.bricks6)
		self.sprites.append(self.bricks7)
		
		self.coinBrick1 = CoinBrick(800, 300, 100, 100, self)
		self.coinBrick2 = CoinBrick(600, 300, 100, 100, self)
		self.sprites.append(self.coinBrick1)
		self.sprites.append(self.coinBrick2)
		self.coinbricks = pygame.transform.scale(self.coinbricks, (100,100))
		self.bricks = pygame.transform.scale(self.bricks, (100,100))
		


	def update(self):
		self.mario = self.sprites[0]
		
		#For loop that checks the collision into either bricks or coin bricks
		for k in self.sprites:
			k.update()
			if(k.amIBrick()):
				if(self.mario.checkCollision(self, self.mario, k)):
					pass
			if(k.AmICoinBlock()):
				if(self.mario.checkCollision(self, self.mario, k)):
					pass
						
	def removeCoin(self, coin):
		self.sprites.remove(coin)
	def addCoin(self, x, y, w, h):
		self.sprites.append(Coin(x, y, w, h, self))
		


class View():
	def __init__(self, model):
		screen_size = (1200,800)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		self.marioImages = []
		self.manyMarioPics = ["mario1.png", "mario2.png", "mario3.png", "mario4.png", "mario5.png"]
		#loop that loops through the images of mario
		for i in range(5):
			self.marioImages.append(pygame.image.load(self.manyMarioPics[i]))

		self.MarioImage = pygame.image.load("mario1.png")
		self.floor = pygame.image.load("stoneGround.png")
		self.floor = pygame.transform.scale(self.floor, (1000, 600))
		self.IbeCoinBrick = pygame.image.load("block1.png")
		self.IbeEmptyCoinBrick = pygame.image.load("block2.png")
		self.background = pygame.image.load("Background.png")
		self.coin = pygame.image.load("coin.png")
		self.differentImage = 0
		self.bricks = pygame.image.load("brick.png")
		self.bricks = pygame.transform.scale(self.bricks, (100,100))
		

	def update(self):
		self.mario = self.model.sprites[0]
		self.model.cameraPosition = self.mario.x - 300
		#draws the background and floor for the game
		for i in range(5):
			self.screen.blit(self.background,[(i * 1000) - (self.model.cameraPosition/ 12), -200])
			self.screen.blit(self.floor, [(i *1000) - (self.model.cameraPosition/12), 700, 1500, 300])
			
		#for loop that deciphers whether the sprites are either mario, brick, coin brick, or coin then draws them
		for i in range(self.model.sprites.__len__()):
			sprite = self.model.sprites[i]
			#this if statement draws mario and different images of mario as if he's walking when pressing the left or right key
			if(sprite.isMario()):
				#draws mario depending on which arrow key is pressed
				self.screen.blit(pygame.transform.flip(self.marioImages[self.differentImage],sprite.flip,False),(self.mario.x - self.model.cameraPosition, self.mario.y))
				if(self.model.moveRight):
					self.screen.blit(self.marioImages[self.differentImage], (self.mario.x - self.model.cameraPosition, self.mario.y))
					self.differentImage += 1
					if(self.differentImage == 5):
						self.differentImage = 0
				elif(self.model.moveLeft):
						self.screen.blit(pygame.transform.flip(self.marioImages[self.differentImage], True, False), (self.mario.x - self.model.cameraPosition, self.mario.y))
						self.differentImage += 1
						if(self.differentImage == 5):
							self.differentImage = 0
					
			#checks if the sprite is a brick and then draws it if it is
			if(sprite.amIBrick()):
				self.screen.blit(self.bricks, [sprite.x - self.model.cameraPosition, sprite.y])
			#checks if the sprite is a coin block and draws it if it is
			if(sprite.AmICoinBlock()):
				if(sprite.amountCoins < 5):
					self.screen.blit(self.IbeCoinBrick, [sprite.x - self.model.cameraPosition, sprite.y, sprite.w ,sprite.h])
				else:
					self.screen.blit(self.IbeEmptyCoinBrick, [sprite.x - self.model.cameraPosition, sprite.y, sprite.w, sprite.h])
			if(sprite.ImACoin()):
				self.screen.blit(self.coin, [sprite.x - self.model.cameraPosition, sprite.y])
				
		pygame.display.flip()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True
		self.Mario = self.model.sprites[0]
	def update(self):
		self.Mario.prevDes()
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
				if event.key == K_LEFT:
						self.model.moveLeft = True
				if event.key == K_RIGHT:
						self.model.moveRight = True
			elif event.type == KEYUP:
				if event.key == K_RIGHT:
					self.model.moveRight = False
				if event.key == K_LEFT:
					self.model.moveLeft = False
		#controller to move mario from left to right and jump
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.Mario.x -= 8
			self.model.mario.direction = -1
			self.model.mario.flip = True
		if keys[K_RIGHT]:
			self.Mario.x += 8
			self.model.direction = 1
			self.model.mario.flip = False
		if keys[K_SPACE]:
			if self.Mario.jump < 5:
				self.Mario.vertical_velocity -= 10.5
				self.Mario.y += self.Mario.vertical_velocity
		
		
			
class Mario(Sprite):
	marioImages = []
	
	
	def __init__(self, x, y, w, h, model):
		super(Mario,self).__init__(x, y, 60, 90, model) #Calls the super constructor in sprite class
		self.prevX = 0
		self.prevY = 0
		marioImages = None
		self.jump = 0
		self.direction = 1
		self.flip = False
		
	def update(self):
		#checks gravity
		if self.y < 620:
			self.vertical_velocity += 3.5
			self.y += self.vertical_velocity
		
		if self.y >= 620:
			self.jump = 0
			self.y = 620
			self.vertical_velocity = 0.0
		self.jump+=1
			
	def prevDes(self):
		self.prevX = self.x
		self.prevY = self.y
	#abstract methods to check what the sprites are
	def isMario(self):
		return True
	def amIBrick(self):
		return False
	def ImACoin(self):
		return False
	def AmICoinBlock(self):
		return False
	
	#fixes the collision of mario, bricks, and coin bricks
	def fixPosition(self, model, mario, sprite):
		if(self.x + self.w >= sprite.x and self.prevX + self.w <= sprite.x):
			self.x = sprite.x - self.w - 7
		elif (self.x <= sprite.x + sprite.w and self.prevX >= sprite.x + sprite.w):
			self.x = sprite.x + sprite.w + 7
		elif (self.y + self.h > sprite.y and self.prevY + self.h <= sprite.y + sprite.h):
			self.y = sprite.y - self.h
			self.jump = 0
			self.vertical_velocity = 3.1
			self.coinPop =0
		elif (self.y < sprite.y + sprite.h and self.prevY >= sprite.h):
			self.y = sprite.y + sprite.h
			self.vertical_velocity = 0.0
			if(sprite.AmICoinBlock() and self.coinPop == 0):
				self.coinPop+=1
				sprite.amountCoins+=1
				if(sprite.amountCoins <= 5):
					model.addCoin(sprite.x, sprite.y, 60, 60)
	

class Brick(Sprite):
	def __init__(self, x, y, w, h, model):
		super(Brick, self).__init__(x, y, 100, 100, model) #calls super constructor in sprite class
	#abstract method to check what the sprite is
	def isMario(self):
		return False
	def amIBrick(self):
		return True
	def update(self):
		pass
	def AmICoinBlock(self):
		return False
	def ImACoin(self):
		return False

class CoinBrick(Sprite):
	def __init__(self, x, y, w, h, model):
		super(CoinBrick, self).__init__(x, y, 100, 100, model)#calls super constructor in sprite class
		self.amountCoins = 0
	#abstract method to check what the sprite is
	def isMario(self):
		return False
	def amIBrick(self):
		return False
	def AmICoinBlock(self):
		return True
	def ImACoin(self):
		return False
	def update(self):
		pass
		
class Coin(Sprite):
	def __init__(self, x, y, w, h, model):
		super(Coin, self). __init__( x, y, w, h, model)#calls super constructor in sprite class
		self.coinDrop = random.randint(1, 10)
		self.vertical_velocity = -19.0
		
	def update(self):
		if(self.y < 620):
			self.vertical_velocity += 1.0
			self.y += self.vertical_velocity
			self.vertical_velocity += 3.5
			
			self.y += self.vertical_velocity
			if(self.coinDrop <= 5):
				self.x += self.coinDrop + 5
			else:
				self.x -= self.coinDrop
		if(self.y >= 620):
			self.model.removeCoin(self)
	#abstract method to check what the sprite is
	def amIBrick(self):
		return False
	def AmICoinBlock(self):
		return False
	def ImACoin(self):
		return True
	def isMario(self):
		return False

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)




while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")