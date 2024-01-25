from core.gamepad import Hat, Button, LStick, RStick, Command
from core.context import exportmacro

@exportmacro("Hello world!")
def hello(cmd:Command):
    cmd.log("Hello macro world!")

@exportmacro("フーフーする関数")
def foo(cmd:Command):
    cmd.log("Hello command!")

@exportmacro("バーバーする関数")
def bar(cmd:Command):
    cmd.log("Hello bar!")
    cmd.press(Button.A)
    cmd.press(Button.B)
    cmd.press(Button.X)
    cmd.press(Button.Y)
    for _ in range(10):
        cmd.press(Button.A)

    #cmd.press(Button.A, dur=2.0)

def piyo(cmd:Command):
    cmd.log("Goodbye command base.")
