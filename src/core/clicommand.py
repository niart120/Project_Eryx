from serial import Serial
from rich.console import Console
import cv2

from typing import Union
import time

from core.controls import Button, Hat, LStick, RStick

class CLICommand():
	def __init__(self, ser:Serial, vc:cv2.VideoCapture, console:Console):
		self.ser = ser
		self.vc = vc
		self.console = console
		self.key_state = None
		self._initialize_key_state()

	def _initialize_key_state(self)->None:
		# key_state = [header,btn1,btn2,hat,lx,ly,rx,ry,kbdheader,key]
		self.key_state = bytearray([0xab, 0x0, 0x0, 0x00, 0x80, 0x80, 0x80, 0x80, 0x00, 0x00])

	def press(self, *keys:Union[Button, Hat, LStick, RStick], dur:float=0.1, wait:float=0.1):
		self.hold(*keys)
		self.wait(dur)
		self.release(*keys)
		self.wait(wait)
		pass

	def hold(self, *keys:Union[Button, Hat, LStick, RStick]):
		# key_state = [header,btn1,btn2,hat,lx,ly,rx,ry,kbdheader,key]
		for key in keys:
			if isinstance(key, Button):
				self.key_state[1] |= key & 0xFF
				self.key_state[2] |= (key>>8) & 0xFF
			elif isinstance(key, Hat):
				self.key_state[3] = key
			elif isinstance(key, LStick):
				self.key_state[4] = key.x
				self.key_state[5] = key.y
			elif isinstance(key, RStick):
				self.key_state[6] = key.x
				self.key_state[7] = key.y
		
		self.send_raw_data(self.key_state)

	def release(self, *keys:Union[Button, Hat, LStick, RStick]):
		for key in keys:
			if isinstance(key, Button):
				self.key_state[1] &= (~key & 0xFF)
				self.key_state[2] &= (~(key>>8) & 0xFF)
			elif isinstance(key, Hat):
				self.key_state[3] = Hat.CENTER
			elif isinstance(key, LStick):
				self.key_state[4] = 0x80
				self.key_state[5] = 0x80
			elif isinstance(key, RStick):
				self.key_state[6] = 0x80
				self.key_state[7] = 0x80
		
		self.send_raw_data(self.key_state)

	def wait(self, wait:float):
		time.sleep(wait)

	def log(self, *values:object, sep:str=' ', end:str='\n'):
		self.console.print(*values, sep, end)

	def capture(self):
		_, mat = self.vc.read()
		return mat

	def send_raw_data(self, raw_data):
		self.ser.write(raw_data)

	def keyboard(self, text:str):
		pass
		