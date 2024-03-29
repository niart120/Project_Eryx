import math
from enum import IntEnum
from typing import Union, Protocol

class Button(IntEnum):
	Y = 0x0001
	B = 0x0002
	A = 0x0004
	X = 0x0008

	L = 0x0010
	R = 0x0020
	ZL = 0x0040
	ZR = 0x0080

	MINUS = 0x0100
	PLUS = 0x0200

	LS = 0x0400
	RS = 0x0800
	HOME = 0x1000
	CAP = 0x2000

class Hat(IntEnum):
	UP = 0x00
	UPRIGHT = 0x01
	RIGHT = 0x02
	DOWNRIGHT = 0x03
	DOWN = 0x04
	DOWNLEFT = 0x05
	LEFT = 0x06
	UPLEFT = 0x07
	CENTER = 0x08

class LStick():
	def __init__(self, rad:float, magnification:float, is_degree = False):
		if is_degree == True: 
			rad = math.radians(rad) # 入力を度数法として解釈
		self.rad = rad
		self.mag = magnification
		if magnification > 1.0:
			self.mag = 1.0
		if magnification < 0:
			self.mag = 0.0

		# 小数点演算誤差を考慮する必要は無い
		self.x = math.ceil(127.5 * math.cos(rad) * self.mag + 127.5) 
		self.y = 255 - math.ceil(127.5 * math.sin(rad) * self.mag + 127.5) #y軸のみ反転を考慮する

LStick.RIGHT = LStick((0/8)*math.tau, 1.0)
LStick.UPRIGHT = LStick((1/8)*math.tau, 1.0)
LStick.UP = LStick((2/8)*math.tau, 1.0)
LStick.UPLEFT = LStick((3/8)*math.tau, 1.0)
LStick.LEFT = LStick((4/8)*math.tau, 1.0)
LStick.DOWNLEFT = LStick((5/8)*math.tau, 1.0)
LStick.DOWN = LStick((6/8)*math.tau, 1.0)
LStick.DOWNRIGHT = LStick((7/8)*math.tau, 1.0)
LStick.CENTER = LStick(0.0, 0.0)

class RStick():
	def __init__(self, rad:float, magnification:float, is_degree = False):
		if is_degree == True: 
			rad = math.radians(rad) # 入力を度数法として解釈
		self.rad = rad
		self.mag = magnification
		if magnification > 1.0:
			self.mag = 1.0
		if magnification < 0:
			self.mag = 0.0

		# 小数点演算誤差を考慮する必要は無い
		self.x = math.ceil(127.5 * math.cos(rad) * self.mag + 127.5) 
		self.y = 255 - math.ceil(127.5 * math.sin(rad) * self.mag + 127.5) #y軸のみ反転を考慮する

RStick.RIGHT = RStick((0/8)*math.tau, 1.0)
RStick.UPRIGHT = RStick((1/8)*math.tau, 1.0)
RStick.UP = RStick((2/8)*math.tau, 1.0)
RStick.UPLEFT = RStick((3/8)*math.tau, 1.0)
RStick.LEFT = RStick((4/8)*math.tau, 1.0)
RStick.DOWNLEFT = RStick((5/8)*math.tau, 1.0)
RStick.DOWN = RStick((6/8)*math.tau, 1.0)
RStick.DOWNRIGHT = RStick((7/8)*math.tau, 1.0)
RStick.CENTER = RStick(0.0, 0.0)

class Command(Protocol):
	def press(self, *keys:Union[Button, Hat, LStick, RStick], dur:float=0.1, wait:float=0.1):
		"""_summary_

		Args:
			dur (float, optional): _description_. Defaults to 0.1.
			wait (float, optional): _description_. Defaults to 0.1.
		"""
		pass

	def hold(self, *keys:Union[Button, Hat, LStick, RStick]):
		"""_summary_
		"""
		pass

	def release(self, *keys:Union[Button, Hat, LStick, RStick]):
		"""_summary_
		"""
		pass

	def wait(self, wait:float):
		"""_summary_

		Args:
			wait (float): _description_
		"""
		pass

	def log(self, *values:object, sep:str=' ', end:str='\n'):
		"""_summary_

		Args:
			sep (str, optional): _description_. Defaults to ' '.
			end (str, optional): _description_. Defaults to '\n'.
		"""
		pass

	def capture(self):
		"""_summary_
		"""
		pass

	def send_raw_data(self, raw_data):
		"""_summary_

		Args:
			raw_data (_type_): _description_
		"""
		pass

	def keyboard(self, text:str):
		"""_summary_

		Args:
			text (str): _description_
		"""
		pass
		