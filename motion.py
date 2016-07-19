import pygame
import random
import pdb
import math
import os
import datetime
import csv

def getDateTimeStamp():
	d = datetime.datetime.now().timetuple()
	return "%d-%02.d-%02.d_%02.d-%02.d-%02.d" % (d[0], d[1], d[2], d[3], d[4], d[5])
	
def dist(p1, p2):
	d = (abs((p1[0]-p2[0])**2) + abs((p1[1]-p2[1])**2))**.5
	return d

colors = {
        'black': [ 0, 0, 0],
        'white': [255,255,255],
        'blue': [ 0, 0,255],
        'green': [ 0,255, 0],
        'red':   [255, 0, 0]
        }

class World():
	stop = False
	
		#object that flies around
	class Object():
		def __init__(self,x,y,xx,yy, size, color, type = '1'):
			self.x = x
			self.y = y
			self.xx = xx
			self.yy = yy
			self.size = size
			self.color = color
			self.shape = type
			
		def get_xy(self):
			return [int(self.x), int(self.y)]
	
	def __init__(self, L):
		pygame.init()
		self.resolution = [700,500]
		self.screen = pygame.display.set_mode(self.resolution)
		pygame.display.set_caption("Projectile Prediction")
		
		self.font = pygame.font.Font(None, 30)
		
		self.clock = pygame.time.Clock()
		
		
		self.margin = 0
		self.clicked = False
		self.dx = 0
		self.dy = 0
		self.count = 30
		self.reveal = 30
		self.totalc = 0
		self.hitc = 0
		self.clickc = 0
		self.tempclick = 0
		self.temptotal = 0
		
		self.object = self.Object(0,0,0,0,20,colors['green'])
		
		self.number = 200
		self.next(L)
	
		#function that randomly generates a new trial
	def next(self, L):
		d = getDateTimeStamp()
		roll = random.random()
		
		#randomly generates color
		if roll < 0.25:
			col = colors['red']
		elif roll < 0.5:
			col = colors['blue']
		elif roll < 0.75:
			col = colors['green']
		else:
			col = colors['black']
			
		#if it is not yet time for the next trial (eg, the 1 second pause
		#in between trials) set color to white, otherwise continue with normal color
		if self.count > 0:
			self.object.color = colors['white']
		else:
			self.object.color = col
			
		#randomly generate size
		roll = random.random()
		if roll < 0.34:
			self.object.size = 15
		elif roll < 0.67:
			self.object.size = 20
		else:
			self.object.size = 25
			
		roll = random.random()
		#randomly generate initial x velocities
		if roll < 0.33:
			self.object.xx = -20
		elif roll < 0.67:
			self.object.xx = 0
		else:
			self.object.xx = 20
		
		#randomly generate x positions and correct x velocities
		roll = random.random()
		if roll < 0.33:
			self.object.x = 0
			self.object.xx = 20
		elif roll < 0.67:
			self.object.x = 350
		else:
			self.object.x = 700
			self.object.xx = -20
		
		roll = random.random()
		#randomly generate initial y velocities
		if roll < 0.33:
			self.object.yy = -20
		elif roll < 0.67:
			self.object.yy = 0
		else:
			self.object.yy = 20
		
		#randomly generate y positions and correct y velocities
		roll = random.random()
		if roll < 0.33:
			self.object.y = 0
			self.object.yy = 20
		elif roll < 0.67:
			self.object.y = 250
		else:
			self.object.y = 500
			self.object.yy = -20
		
		#generate horizontal world 'gravities'
		roll = random.random()
		if roll < 0.34:
			self.dx = -0.5
		elif roll < 0.67:
			self.dx = 0
		else:
			self.dx = 0.5
		
		#generate vertical world 'gravities'
		roll = random.random()
		if roll < 0.34:
			self.dy = -0.5
		elif roll < 0.67:
			self.dy = 0
		else:
			self.dy = 0.5

		#save initial position and velocity of object for future use
		self.oriposx = self.object.x
		self.oriposy = self.object.y
		self.orivelx = self.object.xx
		self.orively = self.object.yy
		
		#end experiment if all trials have been done
		if self.number == 0:
			self.stop = True
			
		#log at the start of a new trial
		if self.count == 0:
			relx,rely = pygame.mouse.get_pos()
			m = pygame.mouse.get_pos()
			self.number = self.number - 1
			self.tempclick = 0
			self.temptotal = 0
			c.writerow([d,relx,rely,'No',self.object.x,self.object.y,dist(m,self.object.get_xy()),'No',self.object.xx,self.object.yy,self.object.color,self.object.size,self.dx,self.dy])
		
	def input(self, L):
		d = getDateTimeStamp()
		
		#Checks for mouse input
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				relx,rely = pygame.mouse.get_pos()
				m = pygame.mouse.get_pos()
				self.tempclick += 1
				self.temptotal += 1
				self.clickc += 1
				self.totalc += 1
				
				#logs mouse click that is unsuccessful in hitting the object
				c.writerow([d,relx,rely,'Yes',self.object.x,self.object.y,dist(m,self.object.get_xy()),'No',self.object.xx,self.object.yy,self.object.color,self.object.size,self.dx,self.dy,'-',self.totalc])
				if dist(m,self.object.get_xy()) <= self.object.size+5:
					#Logs mouse click that successfullly hits object. 
					#'Hit' in this case has a leeway of an extra 5-pixels
					#for the object hitbox
					self.totalc += 1
					self.hitc += 1
					c.writerow([d,relx,rely,'Yes',self.object.x,self.object.y,dist(m,self.object.get_xy()),'Yes',self.object.xx,self.object.yy,self.object.color,self.object.size,self.dx,self.dy,float(self.hitc)/float(self.totalc),self.totalc,200 - self.number])
					self.count = 30
					self.next(L)
				
			if event.type == pygame.KEYDOWN:
				k = event.key
				if k == pygame.K_ESCAPE:
					self.stop = True
	
	def logic(self, L):
		
		#logic to limit the projectile from going too fast,
		#speed should not vary too wildly for the experiment
		d = getDateTimeStamp()
		self.object.xx += self.dx
		if self.object.xx > 12:
			self.object.xx = 12
		if self.object.xx < -12:
			self.object.xx = -12
		if self.object.yy > 12:
			self.object.yy = 12
		if self.object.yy < -12:
			self.object.yy = -12
			
		#Any world 'gravities' are applied to the objects velocity, which then
		#affect the object's position
		self.object.x += self.object.xx
		self.object.yy += self.dy
		self.object.y += self.object.yy
		
		#checks to see if object goes off screen. If so, resets object position
		#and goes to a new trial
		if self.object.x > 700 + self.object.size or self.object.x < 0 - self.object.size or self.object.y > 500 + self.object.size or self.object.y < 0 - self.object.size:
			relx,rely = pygame.mouse.get_pos()
			m = pygame.mouse.get_pos()			
			c.writerow([d,relx,rely,'No',self.object.x,self.object.y,dist(m,self.object.get_xy()),'No',self.object.xx,self.object.yy,self.object.color,self.object.size,self.dx,self.dy,'','',200 - self.number])
			self.object.x = self.oriposx
			self.object.y = self.oriposy
			self.object.xx = self.orivelx
			self.object.yy = self.orively
			self.count = 30
			self.next(L)
		
	#draws the screen every frame
	def draw(self):
		self.screen.fill(colors['white'])
		pygame.draw.circle(self.screen,self.object.color,self.object.get_xy(),self.object.size)
		pygame.display.update()
	
	#The loop that runs through necessary operations. Game will automatically end
	#after hitting 200 trials, or can be exited anytime by hitting escape
	def run(self, L):
		while not self.stop:
			self.input(L)
			self.logic(L)
			self.draw()
			self.clock.tick(30)
			if self.count > 0:
				self.count -= 1
				if self.count == 0:
					self.next(L)
		"""	
class Logger():
    def __init__(self,header,dl = '\t', nl = '\n', fl = ' '):
        self.header = header
        self.delim = dl
        self.newline = nl
        self.filler = fl
        self.file = None
        return
        
    def open_log(self,fn):
        self.file = open(fn,'w')
        self.file.write(self.delim.join(self.header))
        self.file.write(self.newline)
        return
        
    def log(self,  **kwargs):
        line = [self.filler] * len(self.header) #list with filler entries
        for k, v in kwargs.iteritems(): #if keyword in header, replace filler with value
            if k in self.header:
                line[self.header.index(k)] = str(v)
        self.file.write(self.delim.join(line)) #convert list to delimited string
        self.file.write(self.newline)
        return
        
    def close_log(self):
        self.file.close()
		"""
if __name__ == "__main__":
	#S = Subject('A')
	#L = Logger(['DateTime','\t','MousePos','MouseClick','ObjectPos','Hit','ObjVelocity_X','ObjVelocity_Y','Color','Size','X_Grav','Y_Grav'])
	#L.open_log('datta.txt')
	
	#creates an excel file to store data in, I found it easier to use than txt
	c = csv.writer(open("data.csv", "wb"))
	c.writerow(['Date/Time','Mouse Position X','Mouse Position Y','Mouse Click','Object X','Object Y','Mouse-to-Obj Distance','Clicked on Object','Object\'s X Velocity','Object\'s Y Velocity','Color','Size','\"X_Gravity\"','\"Y_Gravity\"','Percent Hit','Total','Trial Number'])
	W = World(c)
	W.run(c)