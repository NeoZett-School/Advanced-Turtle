from .core import Turtle as _Turtle
from .utils import KeyBinds, Mouse
import pygame
import typing

class Turtle(_Turtle):
    """The advanced turtle provides keybinds and mouse."""

    __slots__ = ("keybinds", "mouse")

    def __init__(
        self,
        figure: typing.Optional[pygame.Surface] = None,
        undo_stack: int = 1000,
        visible: bool = True, 
        keybinds: typing.Optional[KeyBinds] = None,
    ) -> None:
        _Turtle.__init__(self, figure, undo_stack, visible)

        self.keybinds = keybinds
        self.mouse = Mouse()