#!/usr/bin/env python

class CardInfo:
	"""Base information of every element(card)"""
	def __init__(self, cardID, position, flag):
		self.cardID = cardID
		self.position = position
		self.flag = flag

	def GetPosition(self):
		return self.position

	def GetCardId(self):
		return self.cardID

	def GetFalg(self):
		return self.flag

	def SetFlag(self, flag):
		self.flag = flag




