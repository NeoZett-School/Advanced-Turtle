# Copyright (c) 2026 Neo Zetterberg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations
from collections import deque
import pygame
import typing
import math
import sys

ColorValue: typing.TypeAlias = typing.Union[typing.Tuple[int, int, int], typing.Sequence, pygame.Color]

_ExitCode: typing.TypeAlias = typing.Union[str, int, None]

P = typing.ParamSpec("P")

T = typing.TypeVar("T", bound=typing.Callable)
T2 = typing.TypeVar("T2")

def standardize_color(color: ColorValue) -> pygame.Color:
    if isinstance(color, (typing.Sequence, tuple)):
        return pygame.Color(*color)
    return color

class Vec2D(tuple):
    def __new__(cls, x: float, y: float) -> Vec2D:
        return tuple.__new__(cls, (x, y))
    def __add__(self, other: typing.Tuple[float, float]) -> Vec2D:
        return Vec2D(self[0]+other[0], self[1]+other[1])
    def __mul__(self, other: typing.Tuple[float, float])-> typing.Union[Vec2D, float]:
        if isinstance(other, Vec2D):
            return self[0]*other[0]+self[1]*other[1]
        return Vec2D(self[0]*other, self[1]*other)
    def __rmul__(self, other: typing.Tuple[float, float]) -> Vec2D:
        if isinstance(other, int) or isinstance(other, float):
            return Vec2D(self[0]*other, self[1]*other)
        return NotImplemented
    def __sub__(self, other: typing.Tuple[float, float]) -> Vec2D:
        return Vec2D(self[0]-other[0], self[1]-other[1])
    def __neg__(self) -> Vec2D:
        return Vec2D(-self[0], -self[1])
    def __abs__(self) -> float:
        return math.hypot(*self)
    def rotate(self, angle: int) -> Vec2D:
        perp = Vec2D(-self[1], self[0])
        angle = math.radians(angle)
        c, s = math.cos(angle), math.sin(angle)
        return Vec2D(self[0]*c+perp[0]*s, self[1]*c+perp[1]*s)
    def __getnewargs__(self) -> typing.Tuple[float, float]:
        return (self[0], self[1])
    def __repr__(self) -> str:
        return "(%.2f,%.2f)" % self

class Pen:
    def __init__(
        self, 
        position: Vec2D, 
        heading: float, 
        color: ColorValue, 
        size: int, 
        figure: typing.Optional[pygame.Surface] = None
    ) -> None:
        self.position = position
        self.heading = heading
        self.color = standardize_color(color)
        self.size = size
        self.figure = figure
        self.path = list()

        self._pen_down = True
        self._visible = True
    
    def set_size(self, size: int = 2) -> None:
        self.size = size
    
    def set_speed(self, speed: float = 50) -> None:
        self.speed = speed
    
    @typing.overload
    def set_color(self, r: int, g: int, b: int) -> None: ...
    @typing.overload
    def set_color(self, color: ColorValue) -> None: ...
    
    def set_color(self, *args: typing.Any) -> None: 
        if not args:
            raise ValueError("Color required.")

        if len(args) == 1:
            self.color = standardize_color(args[0])
        else:
            self.color = pygame.Color(*args)
    
    def hide(self) -> None:
        self._visible = False
    
    def show(self) -> None:
        self._visible = True
    
    def penup(self) -> None:
        self._pen_down = False
        self._new_path()
    
    def pendown(self) -> None:
        self._pen_down = True

    def _new_path(self) -> None:
        self.path.append([])
    
    def _mark(self) -> None:
        if not self.path:
            self.path.append([])
        self.path[-1].append(Vec2D(*self.position))

class Navigator:
    def __init__(
        self, 
        position: Vec2D, 
        heading: float = 0.0, 
        speed: float = 0.0
    ) -> None:
        self._origin = Vec2D(0, 0)
        self._render_pos = Vec2D(*position)
        self._target_pos = Vec2D(*position)
        self.heading = heading
        self.speed = speed
    
    @property
    def position(self) -> Vec2D:
        return self._render_pos

    def forward(self, distance: float) -> None:
        rad = math.radians(self.heading)
        dx = distance * math.cos(rad)
        dy = -distance * math.sin(rad)
        self._target_pos = Vec2D(self._target_pos[0] + dx, self._target_pos[1] + dy)
    
    @typing.overload
    def goto(self, x: float, y: float) -> None: ...
    @typing.overload
    def goto(self, pos: Vec2D) -> None: ...

    def goto(self, x: typing.Union[Vec2D, float], y: typing.Optional[float] = None) -> None:
        if y is None:
            self._target_pos = Vec2D(*x)
            self.heading = self.towards(*x)
        else:
            self._target_pos = Vec2D(x, y)
            self.heading = self.towards(x, y)
    
    @typing.overload
    def teleport(self, x: float, y: float) -> None: ...
    @typing.overload
    def teleport(self, pos: Vec2D) -> None: ...

    def teleport(self, x: typing.Union[Vec2D, float], y: typing.Optional[float] = None) -> None:
        if y is None:
            self._render_pos = Vec2D(*x)
            self._target_pos = Vec2D(*x)
        else:
            self._render_pos = Vec2D(x, y)
            self._target_pos = Vec2D(x, y)
    
    def left(self, angle: float) -> None:
        self.heading += angle

    def right(self, angle: float) -> None:
        self.heading -= angle
    
    def home(self) -> None:
        self.goto(*self._origin)
    
    def setx(self, x: float) -> None:
        self.goto(x, self.position[1])
    
    def sety(self, y: float) -> None:
        self.goto(self.position[0], y)
    
    def set_heading(self, angle: float) -> None:
        self.heading = angle
    
    @typing.overload
    def head_towards(self, x: float, y: float) -> None: ...
    @typing.overload
    def head_towards(self, pos: typing.Union[Vec2D, Navigator]) -> None: ...

    def head_towards(self, *args: typing.Any) -> None:
        self.heading = self.towards(*args)
    
    @typing.overload
    def distance(self, x: float, y: float) -> Vec2D: ...
    @typing.overload
    def distance(self, pos: typing.Union[Vec2D, Navigator]) -> Vec2D: ...
    
    def distance(self, x: typing.Union[Vec2D, Navigator, float], y: typing.Optional[float] = None) -> Vec2D:
        if y is not None:
            pos = Vec2D(x, y)
        elif isinstance(x, Vec2D):
            pos = x
        elif isinstance(x, typing.Sequence):
            pos = Vec2D(*x)
        elif isinstance(x, Navigator):
            pos = x._render_pos
        return abs(pos - self._render_pos)
    
    @typing.overload
    def towards(self, x: float, y: float) -> float: ...
    @typing.overload
    def towards(self, pos: typing.Union[Vec2D, Navigator]) -> float: ...
    
    def towards(self, x: typing.Union[Vec2D, Navigator, float], y: typing.Optional[float] = None) -> float:
        if y is not None:
            pos = Vec2D(x, y)
        elif isinstance(x, Vec2D):
            pos = x
        elif isinstance(x, typing.Sequence):
            pos = Vec2D(*x)
        elif isinstance(x, Navigator):
            pos = x._render_pos
        
        dx, dy = pos - self._render_pos

        # invert dy because pygame Y axis is downward
        angle = math.degrees(math.atan2(-dy, dx)) % 360.0
        return angle
    
    def circle(
        self, 
        queue: deque, 
        radius: int, 
        steps: typing.Optional[int] = None, 
        direction: typing.Literal["left", "right"] = "left"
    ) -> None:
        if steps is None:
            steps = max(12, int(abs(radius) * math.pi / 4))

        circumference = 2 * math.pi * abs(radius)
        step_len = circumference / steps
        turn = 360.0 / steps

        if radius < 0:
            turn = -turn
        
        if not direction in ("left", "right"):
            raise ValueError(f"Cannot rotate a circle '{direction}'")

        rotator = CMD_NAVIGATOR_LEFT if direction == "left" else CMD_NAVIGATOR_RIGHT

        for _ in range(steps):
            queue.append((0, step_len))
            queue.append((rotator, turn))

    def _update(self, dt: float) -> None:
        delta = self._target_pos - self._render_pos
        dist = abs(delta)

        if dist == 0:
            return
        
        step = min(self.speed * dt, dist)

        direction = Vec2D(delta[0] / dist, delta[1] / dist)
        new_pos = Vec2D(
            self._render_pos[0] + direction[0] * step,
            self._render_pos[1] + direction[1] * step,
        )

        self._render_pos = new_pos

_COMMAND_TABLE = [
    Navigator.forward,
    Navigator.goto,
    Navigator.teleport,
    Navigator.left,
    Navigator.right,
    Navigator.home,
    Navigator.setx,
    Navigator.sety,
    Navigator.set_heading,
    Navigator.head_towards,
    Pen.hide,
    Pen.show,
    Pen.penup,
    Pen.pendown,
    Pen.set_size,
    Pen.set_speed,
    Pen.set_color
]

CMD_NAVIGATOR_FORWARD = 0
CMD_NAVIGATOR_GOTO = 1
CMD_NAVIGATOR_TELEPORT = 2
CMD_NAVIGATOR_LEFT = 3
CMD_NAVIGATOR_RIGHT = 4
CMD_NAVIGATOR_HOME = 5
CMD_NAVIGATOR_SETX = 6
CMD_NAVIGATOR_SETY = 7
CMD_NAVIGATOR_SET_HEADING = 8
CMD_NAVIGATOR_HEAD_TOWARDS = 9
CMD_PEN_HIDE = 10
CMD_PEN_SHOW = 11
CMD_PEN_PENUP = 12
CMD_PEN_PENDOWN = 13
CMD_PEN_SET_SIZE = 14
CMD_PEN_SET_SPEED = 15
CMD_PEN_SET_COLOR = 16

class Screen:
    """Turtle screen to render upon."""

    __slots__ = ("surface", "clock", "dt", "target_fps", "_bg_color", "_bg_surface", "_turtles")

    def __init__(
        self, 
        width: int, 
        height: int, 
        *, 
        target_fps: float = 60.0
    ) -> None:
        self.surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.dt = 0.0

        self.target_fps = target_fps
        self._bg_color = pygame.Color(255, 255, 255)
        self._bg_surface = None

        self._turtles = list()

        self.set_caption("pygame turtle window")

        Turtle.screen = self
    
    @staticmethod
    def set_caption(title: str) -> None:
        pygame.display.set_caption(title)
    
    @staticmethod
    def set_icon(surface: pygame.Surface) -> None:
        pygame.display.set_icon(surface)
    
    @staticmethod
    def flip() -> None:
        pygame.display.flip()
    
    @typing.overload
    def set_background(self, r: int, g: int, b: int) -> None: ...
    @typing.overload
    def set_background(self, color: ColorValue) -> None: ...
    @typing.overload
    def set_background(self, image: pygame.Surface) -> None: ...

    def set_background(self, *args: typing.Any) -> None:
        if not args:
            raise ValueError("You must provide at least on argument when you set background for a screen.")
        if isinstance(args[0], pygame.Surface):
            self._bg_surface = pygame.transform.smoothscale(args[0], self.surface.get_size())
        elif isinstance(args[0], (typing.Sequence, pygame.Color)):
            self._bg_color = pygame.Color(*args[0])
        else:
            self._bg_color = pygame.Color(*args)
    
    def tick(self) -> None:
        self.dt = self.clock.tick(self.target_fps)
    
    def clear(self) -> None:
        if self._bg_surface is not None:
            self.surface.blit(self._bg_surface, (0, 0))
        else:
            self.surface.fill(self._bg_color)
    
    def update(self) -> None:
        for turtle in self._turtles:
            turtle._update()
            turtle._render()
    
    def mainloop(self) -> None:
        active = True
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    break
            self.tick()
            self.clear()

            self.update()
            self.flip()

class _QueuedArgument(typing.Generic[P, T2]):
    __slots__ = ("func", "args", "kwargs")

    def __new__(cls, func: typing.Callable[P, T2], *args: P.args, **kwargs: P.kwargs) -> _QueuedArgument[P, T2]:
        inst = object.__new__(cls)
        inst.func = func
        inst.args = args
        inst.kwargs = kwargs
        return inst
    
    def __call__(self) -> T2:
        return self.func(*self.args, **self.kwargs)

class Turtle(Pen, Navigator):
    """The turtle itself."""

    __slots__ = (
        "heading", "speed", "color", 
        "size", "figure", "path", 
        "undo_stack", "redo_path", 
        "redo_command", 

        "_canvas", "_target_pos", "_render_pos", 
        "_origin", "_pen_down", "_visible",

        "_original_figure", "_rotation_cache",

        "_command_queue", "_current_command"
    )

    screen: typing.ClassVar[Screen] = None

    def __init__(
        self, 
        figure: typing.Optional[pygame.Surface] = None, 
        undo_stack: int = 20, 
        visible: bool = True
    ) -> None:
        if undo_stack < 0:
            raise ValueError("Undo stack must be a non-negative integer.")

        w, h = self.screen.surface.get_size()
        start = Vec2D(w/2, h/2)
        self._origin = start
        self._target_pos = Vec2D(*start)
        self._render_pos = Vec2D(*start)
        self.heading = 0.0
        self.speed = 50.0
        self.color = pygame.Color(0, 0, 0)
        self.size = 2
        self.figure = figure.convert_alpha() if figure is not None else None
        self.path = [list()]
        self.undo_stack = undo_stack

        self.redo_path = list()
        self.redo_command = list()

        self._canvas = pygame.Surface((w, h), pygame.SRCALPHA)
        self._pen_down = True
        self._visible = visible

        self._original_figure = self.figure.copy() if figure is not None else None
        self._rotation_cache = {}

        self._command_queue = deque()
        self._current_command = None

        self.screen._turtles.append(self)
    
    @property
    def position(self) -> Vec2D:
        return self._render_pos
    
    def reset(self) -> None:
        w, h = self.screen.surface.get_size()
        start = Vec2D(w/2, h/2)
        self._origin = start
        self._target_pos = Vec2D(*start)
        self._render_pos = Vec2D(*start)
        self._command_queue.clear()
        self._clear()
    
    def set_figure(self, surface: pygame.Surface) -> None:
        self._original_figure = surface.copy()
        self._rotation_cache.clear()
        self.figure = surface
    
    def set_size(self, size: int = 2) -> None:
        self._command_queue.append((CMD_PEN_SET_SIZE, size))
    
    def set_speed(self, speed: float = 50) -> None:
        self._command_queue.append((CMD_PEN_SET_SPEED, speed))

    def set_color(self, *args: typing.Any) -> None: 
        self._command_queue.append((CMD_PEN_SET_COLOR, *args))
    
    def clear(self) -> None:
        self._command_queue.append((Turtle._clear,))

    def _clear(self) -> None:
        self._canvas.fill((0, 0, 0, 0))
        self.path.clear()
    
    def undo(self) -> None:
        if not self.path or not any(self.path):
            if self._command_queue:
                self.redo_command.append(self._command_queue.pop())
            return
        if len(self.redo_path) >= self.undo_stack:
            self.redo_path.pop(0)
        self.redo_path.append(self.path[-1].pop())
    
    def redo(self) -> None:
        if not self.redo_path or not self.path:
            if self.redo_command:
                self._command_queue.append(self.redo_command.pop())
            return
        self.path[-1].append(self.redo_path.pop())
    
    def hide(self) -> None:
        self._command_queue.append((CMD_PEN_HIDE,))
    
    def show(self) -> None:
        self._command_queue.append((CMD_PEN_SHOW,))
    
    def penup(self) -> None:
        self._command_queue.append((CMD_PEN_PENUP,))
    
    def pendown(self) -> None:
        self._command_queue.append((CMD_PEN_PENDOWN,))
    
    def forward(self, distance: float) -> None:
        self._command_queue.append((CMD_NAVIGATOR_FORWARD, distance))

    def goto(self, x: typing.Union[Vec2D, float], y: typing.Optional[float] = None) -> None:
        self._command_queue.append((CMD_NAVIGATOR_GOTO, x, y))

    def teleport(self, x: typing.Union[Vec2D, float], y: typing.Optional[float] = None) -> None:
        self._command_queue.append((CMD_NAVIGATOR_TELEPORT, x, y))

    def left(self, angle: float) -> None:
        self._command_queue.append((CMD_NAVIGATOR_LEFT, angle))

    def right(self, angle: float) -> None:
        self._command_queue.append((CMD_NAVIGATOR_RIGHT, angle))
    
    def home(self) -> None:
        self._command_queue.append((CMD_NAVIGATOR_HOME,))
    
    def setx(self, x: float) -> None:
        self._command_queue.append((CMD_NAVIGATOR_SETX, x))
    
    def sety(self, y: float) -> None:
        self._command_queue.append((CMD_NAVIGATOR_SETY, y))
    
    def set_heading(self, angle: float) -> None:
        self._command_queue.append((CMD_NAVIGATOR_SET_HEADING, angle))
    
    def head_towards(self, *args: typing.Any) -> None:
        self._command_queue.append((CMD_NAVIGATOR_HEAD_TOWARDS, *args))
    
    def dot(self) -> None:
        self._command_queue.append((Turtle._dot,))
    
    def _dot(self) -> None:
        pygame.draw.rect(self._canvas, self.color, pygame.Rect(*self.position, 1, 1))
    
    def circle(
        self, 
        radius: int, 
        steps: typing.Optional[int] = None, 
        direction: typing.Literal["left", "right"] = "left"
    ) -> None:
        Navigator.circle(self, self._command_queue, radius, steps, direction)

    def custom_command(
        self, 
        id_or_func: typing.Union[typing.Callable, int], 
        *args: typing.Any
    ) -> None:
        self._command_queue.append((id_or_func, *args))
    
    def _new_path(self) -> None:
        self._commit(self._canvas, using_undo_stack=True)
        Pen._new_path(self)
    
    def _mark(self) -> None:
        self.redo_path.clear()
        Pen._mark(self)
    
    def _start_command(self, spec: typing.Tuple[typing.Callable, ...]) -> None:
        func_id, *args = spec

        # Only in some special cases will there be functions referenced within the Turtle class itself
        func = func_id if callable(func_id) else _COMMAND_TABLE[func_id]
        resolved_args = [arg() if isinstance(arg, _QueuedArgument) else arg for arg in args]

        func(self, *resolved_args)

        if self.figure is not None and func_id in (
            CMD_NAVIGATOR_LEFT, 
            CMD_NAVIGATOR_RIGHT, 
            CMD_NAVIGATOR_GOTO, 
            CMD_NAVIGATOR_SET_HEADING,
            CMD_NAVIGATOR_HEAD_TOWARDS
        ):
            if self._original_figure is None:
                self._original_figure = self.figure.copy()
            
            self.figure = self._rotation_cache.setdefault(
                int(self.heading) % 360,
                pygame.transform.rotate(
                    self._original_figure,
                    self.heading
                ).convert_alpha()
            )
    
    def _command_done(self) -> bool:
        if self._current_command and self._current_command[0] in (
            CMD_NAVIGATOR_FORWARD, CMD_NAVIGATOR_GOTO
        ):
            return math.dist(self._render_pos, self._target_pos) <= max(0.1, self.speed * 0.02)
        return True
    
    def _update(self) -> None:
        if self.path and len(self.path[-1]) > self.undo_stack:
            self._commit(self._canvas, permanent=True)
        
        if self._current_command is None and self._command_queue:
            self._current_command = self._command_queue.popleft()
            self._start_command(self._current_command)
        
        Navigator._update(self, self.screen.dt / 1000)

        if self._command_done():
            self._current_command = None

        if self._pen_down and self._render_pos != self._target_pos:
            self._mark()
    
    def _commit(self, surface: pygame.Surface, *, using_undo_stack: bool = False, permanent: bool = False) -> None:
        last_segment = len(self.path) - 1 # Cache some math
        for i, segment in enumerate(self.path if permanent else self.path.copy()):
            if not permanent and not i == last_segment:
                self.path.pop(i)
            
            if len(segment) < 2:
                continue

            path = segment if using_undo_stack or not i == last_segment else segment[:-self.undo_stack]
            path_length = len(path)

            if len(path) < 3:
                continue

            lines = []
            for j, pos in enumerate(path.copy()):
                if permanent and i == last_segment and j < path_length - 2: 
                    del self.path[i][j]
                lines.append(pos)
            
            pygame.draw.lines(surface, self.color, False, lines, width=self.size)
    
    def _render(self) -> None:
        self.screen.surface.blit(self._canvas, (0, 0))
        self._commit(self.screen.surface, using_undo_stack=True)
        if self._visible and self.figure is not None:
            self.screen.surface.blit(self.figure, self.figure.get_rect(center=self.position))

def queue(func: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> _QueuedArgument[P, T]:
    """The process enters the queue by being passed as an argument to an existing queued method, thereby sharing its execution slot."""

    # Someone might want to use turtle.head_towards(x, queue(lambda: turtle.position[1])) instead of just set_heading(0) f.e

    return _QueuedArgument(func, *args, **kwargs)

def init() -> None:
    pygame.init()

def exit(status: _ExitCode = None) -> typing.NoReturn:
    pygame.quit()
    sys.exit(status)