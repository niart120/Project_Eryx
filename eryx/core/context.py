import sys
import os
from pathlib import Path
import importlib
from inspect import isfunction, getmembers 
from typing import Callable

def exportmacro(description:str):
	def _exportmacro(func:Callable):
		func.__dict__["macro_description"] = description
		return func
	return _exportmacro

class MacroManager:

    def __init__(self, root_path: str):
        self.plugins = {}
        self.macros = {}
        self.root_path = root_path
        sys.path.append(self.root_path)

    def load_macro_files(self):
        #for file_path in Path(self.path).glob('*.py'):
        for dir_path, _, file_names in os.walk(self.root_path):
            # ディレクトリパスの正規化
            dir_path = Path(dir_path)
            for file_name, ext in map(os.path.splitext, file_names):
                # pythonファイル以外は読み飛ばす
                if ext != ".py":continue
                # モジュール名として適切な形に変換
                module_name = os.path.join(dir_path, file_name).replace(os.path.sep,".")
                if module_name not in self.plugins:
                    self.plugins[module_name] = importlib.import_module(module_name)
                    self.load_macro(self.plugins[module_name])
                else:
                    self.plugins[module_name] = importlib.reload(self.plugins[module_name])
                    self.load_macro(self.plugins[module_name])

    def load_macro(self, macrofile):
        for name, value in getmembers(macrofile):
            if not isfunction(value):continue
            function = value
            # 辞書に登録
            if "macro_description" in value.__dict__:
                description = value.__dict__["macro_description"]
                self.macros[name] = function, description