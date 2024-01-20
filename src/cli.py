from typing import Union
import time

import cv2
from serial import Serial
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Column, Table

from core.context import MacroManager
from core.gamepad import Button, Hat, LStick, RStick

class CLICommand():
	def __init__(self, ser:Serial, vc:cv2.VideoCapture, console:Console):
		self.ser = ser
		self.vc = vc
		self.console = console
		self.key_state = None
		self._initialize_key_state()

	def _initialize_key_state(self)->None:
		# key_state = [header,btn1,btn2,hat,lx,ly,rx,ry,kbdheader,key]
		self.key_state = bytearray([0xab, 0x00, 0x00, Hat.CENTER, 0x80, 0x80, 0x80, 0x80, 0x00, 0x00, 0x00])

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
		

"""
自動化スクリプトを呼び出すCLIプログラム
"""
class CLIMacroController():
    def __init__(self):
        # コンソールの立ち上げ
        self.console = Console()

        # マクロの読み込み
        self.macro_manager = MacroManager("macro/")
        self.macro_manager.load_macro_files()

        # シリアルポート開通
        ser = Serial(port="COM4")
        # カメラオブジェクト取得
        vc = cv2.VideoCapture(0)

        # コマンドオブジェクト
        self.cmd = CLICommand(ser,vc,self.console)

    def show_macrolist_table(self):
        table = Table(show_header=True, header_style="bold magenta",title="Macro List")
        table.add_column("macro name")
        table.add_column("description")

        for name, (func, desc) in self.macro_manager.macros.items():
            table.add_row(name, desc)

        self.console.print(table)

    def prompt_macro_execution(self):
        macrolist = self.macro_manager.macros.keys()
        target_macro = Prompt.ask("実行するマクロ([bold magenta]macro name[/bold magenta])を入力してください.", console=self.console,choices=macrolist,show_choices=False)

        func, _ = self.macro_manager.macros[target_macro]
        func(self.cmd)

    def run(self):
        self.show_macrolist_table()
        while True:
            self.prompt_macro_execution()

def main():
    
    controller = CLIMacroController()
    controller.run()
        

if __name__ == "__main__":
    main()