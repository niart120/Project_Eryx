import sys
from pathlib import Path
import importlib
from inspect import isfunction, getmembers 

class MacroManager:

    def __init__(self, path: str):
        self.plugins = {}
        self.macros = {}
        self.path = path
        sys.path.append(self.path)

    def scan_macro_file(self):
        for file_path in Path(self.path).glob('*.py'):
            self.load_macro_file(file_path)

    def load_macro_file(self, file_path):
        module_name = file_path.stem
        if module_name not in self.plugins:
            self.plugins[module_name] = importlib.import_module(module_name)
            self.load_macro(self.plugins[module_name])
        else:
            self.plugins[module_name] = importlib.reload(self.plugins[module_name])
            self.load_macro(self.plugins[module_name])

    def load_macro(self, macrofile):
        for name, value in getmembers(macrofile):
            if not isfunction(value):continue
            # 辞書に登録
            if "macro_name" in value.__dict__:
                self.macros[name] = value