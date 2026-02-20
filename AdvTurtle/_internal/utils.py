from __future__ import annotations
import pygame
import typing

class KeyBinds:
    __slots__ = ("binds",)

    def __init__(
        self, 
        binds: typing.Optional[typing.Dict[str, int]] = None,
        **kwargs: int
    ) -> None: 
        self.binds = binds if binds is not None else kwargs
    
    def get_pressed(self) -> typing.Dict[str, bool]:
        processed = {}
        pressed = pygame.key.get_pressed()
        for key, _id in self.binds.items():
            processed[key] = pressed[_id]
        return processed

class Mouse:
    @staticmethod
    def get_pressed() -> typing.Tuple[int, int, int]:
        return pygame.mouse.get_pressed()
    
    @staticmethod
    def get_pos() -> typing.Tuple[int, int]:
        return pygame.mouse.get_pos()

def load_figure(file: str, size: typing.Tuple[int, int]) -> pygame.Surface:
    return pygame.transform.smoothscale(pygame.image.load(file), size)