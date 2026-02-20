import pygame
import typing

class KeyBinds:
    def __init__(
        self, 
        binds: typing.Optional[typing.Dict[str, int]] = None,
        **kwargs: int
    ) -> None: ...
    def get_pressed(self) -> typing.Dict[str, bool]: ...

class Mouse:
    @staticmethod
    def get_pressed() -> typing.Tuple[int, int, int]: ...
    @staticmethod
    def get_pos() -> typing.Tuple[int, int]: ...

def load_figure(file: str, size: typing.Tuple[int, int]) -> pygame.Surface: ...