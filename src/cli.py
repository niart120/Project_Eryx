import cv2
import serial

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Column, Table

from core.clicommand import CLICommand
from core.misc import MacroManager

"""
自動化スクリプトを呼び出すCLIプログラム
"""
class CLIMacroController():
    def __init__(self):
        # コンソールの立ち上げ
        self.console = Console()

        # マクロの読み込み
        self.macro_manager = MacroManager("macro/")
        self.macro_manager.scan_macro_file()

        # シリアルポート開通
        ser = serial.Serial(port="COM4")
        # カメラオブジェクト取得
        vc = cv2.VideoCapture(0)

        # コマンドオブジェクト
        self.cmd = CLICommand(ser,vc,self.console)

    def show_macrolist_table(self):
        table = Table(show_header=True, header_style="bold magenta",title="Macro List")
        table.add_column("macro name")
        table.add_column("description")

        for name, func in self.macro_manager.macros.items():
            table.add_row(name, func.__dict__["macro_name"])

        self.console.print(table)

    def prompt_macro_execution(self):
        macrolist = self.macro_manager.macros.keys()
        target_macro = Prompt.ask("実行するマクロ([bold magenta]macro name[/bold magenta])を入力してください.", console=self.console,choices=macrolist,show_choices=False)

        func = self.macro_manager.macros[target_macro]
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