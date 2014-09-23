#!/usr/bin/env python

import wx
import wx.lib.buttons
from wxPython.wx import *
import random

#module thread, pygame just for paly sound
#for wx.sound coundn't output sound
import thread
import pygame

class MyWindows(wx.Frame):
	"""docstring for MyWindows."""
	def __init__(self):
		self.PASSABLE = 1
		self.IMPASSABLE = 0
		self.lastChoosenCard = None
		self.ELEMENT_WIDTH = 43
		self.ELEMENT_HEIGHT = 50
		self.BUTTON_SIZE = (self.ELEMENT_WIDTH, self.ELEMENT_HEIGHT)

		self.LoadBackgroundImage("mainback.jpg")

		wx.Frame.__init__(self, None, title="MyGames", pos=(0,0), size=self.size, \
			style=wxDEFAULT_FRAME_STYLE & ~ (wxRESIZE_BORDER | wxRESIZE_BOX | wxMAXIMIZE_BOX))

		self.BackgroundImage = wx.StaticBitmap(parent=self, bitmap=self.bitmap)
		self.DrawGameBoard()

		self.Show(True)

	def LoadBackgroundImage(self, file):
		"""load image as current windows's main background."""
		image = wx.Image(file, wx.BITMAP_TYPE_JPEG)
		self.bitmap = image.ConvertToBitmap()
		self.width = self.bitmap.GetWidth()
		self.height = self.bitmap.GetHeight()
		self.size = self.width, self.height

	def DrawGameBoard(self):
		"""draw game board to display game sense, and init cards images."""
		#load images for every base element card
		self.cardimages = []
		img = wx.Bitmap("cardimages.png")
		for i in range(0, 32):
			self.cardimages.append(img.GetSubBitmap(wx.Rect(32*i, 0, 32, 32)))
		del img #of no use from now on, delete it

		#calculate the game board size according to the main background image size
		panelSize = (self.width-40)/self.ELEMENT_WIDTH*self.ELEMENT_WIDTH, \
			(self.height-40)/self.ELEMENT_HEIGHT*self.ELEMENT_HEIGHT
		xCnt = (self.width-40)/self.ELEMENT_WIDTH
		yCnt = (self.height-40)/self.ELEMENT_HEIGHT
		self.panel = wx.Panel(self, pos=(20,20), size=panelSize, name="BORAD")

		#paint the image to all card
		self.cardsStatus = {}
		#(buttonID, (position(x,y), flag))
		self.buttons = []
		i = 0
		bound = 9999
		for x in range(0, xCnt + 2):
			for y in range(0, yCnt + 2):
				if (0 == x) or (xCnt+1 == x) or (0 == y) or (yCnt+1 == y):
					#init bound route status for link detect
					cardID = -1
					self.cardsStatus[bound] = ((x,y), self.PASSABLE)
					bound = bound + 1
				else:
					cardID = random.randint(0,32-1)
					self.buttons.append(wx.BitmapButton(self.panel, -1, self.cardimages[cardID], \
						pos=(self.ELEMENT_WIDTH*(x-1), self.ELEMENT_HEIGHT*(y-1)), size=self.BUTTON_SIZE, name=str(cardID)))
					self.Bind(wx.EVT_BUTTON, self.OnClick, self.buttons[i])
					self.cardsStatus[self.buttons[i].GetId()] = ((x,y), self.IMPASSABLE)
					# print self.cardsStatus[self.buttons[i].GetId()]
					i = i + 1

	def OnClick(self, event):
		"""card has been choosen, so need to save check last choosen card ID with current card ID,
		if both with the same ID, then redraw the card as none image, else, update last choosen card
		ID for next one use."""
		button = event.GetEventObject()
		print button.GetId()
		if self.lastChoosenCard == None:
			self.lastChoosenCard = button
		elif button.GetName() == self.lastChoosenCard.GetName():
			# print "Bingo"
			# position, flag = self.cardsStatus[button.GetId()]
			# print "Current button info: pos=%s, flag=%d" %(position, flag)
			# position, flag = self.cardsStatus[self.lastChoosenCard.GetId()]
			# print "Last clicked button info: pos=%s, flag=%d" %(position, flag)
			self.DetectLink(button, self.lastChoosenCard)
			button.Hide()
			self.lastChoosenCard.Hide()
			self.lastChoosenCard = None
			thread.start_new_thread(self.play, ("./sound/Hint.wav",))
		else:
			# print "-_-'"
			self.lastChoosenCard = button
			thread.start_new_thread(self.play, ("./sound/Click.wav",))

	def DetectLink(self, button1, button2):
		"""detect the link between the two cards last clicked. Algorithm please 
		reference to "http://www.cnblogs.com/heaad/archive/2010/06/06/1752468.html"."""
		id1 = button1.GetId()
		(x1, y1), flag1 = self.cardsStatus[button1.GetId()]
		id2 = button2.GetId()
		(x2, y2), flag2 = self.cardsStatus[button2.GetId()]
		if min(x1, x2) == x1:
			src = (x1, y1)
			dst = (x2, y2)
		else:
			src = (x2, y2)
			dst = (x1, y1)

		#For route 1: a straight line
		if x1 == x2:
			i = min(y1, y2) + 1
			while(i <= max(y1, y2)):
				for (x1, i) in 
		#For route 2: one corner
		#For route 3: two corner

	def play(self, file):
		"""play a sound"""
		pygame.init()
		pygame.mixer.init()
		soundwav = pygame.mixer.Sound(file) 
		soundwav.play()

if __name__ == "__main__":
	app = wx.App(False)
	frame = MyWindows()
	app.MainLoop()