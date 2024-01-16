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

    def load_macro_files(self):
        for file_path in Path(self.path).glob('*.py'):
            module_name = file_path.stem
            if module_name not in self.plugins:
                self.plugins[module_name] = importlib.import_module(module_name)
                self.load_macro(self.plugins[module_name])
            else:
                self.plugins[module_name] = importlib.reload(self.plugins[module_name])
                self.load_macro(self.plugins[module_name])
        
        self.macros["exit"] = (lambda x:sys.exit(0)), "ランチャーを終了します"

    def load_macro(self, macrofile):
        for name, value in getmembers(macrofile):
            if not isfunction(value):continue
            function = value
            # 辞書に登録
            if "macro_description" in value.__dict__:
                description = value.__dict__["macro_description"]
                self.macros[name] = function, description