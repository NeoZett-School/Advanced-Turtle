# 🐢 Advanced-Turtle
A modern, command-driven turtle graphics engine built on top of **pygame**.

This project reimagines Python’s classic turtle module with:

- A command-queue–based execution model

- Time-based interpolation (frame-rate independent movement)

- Surface-backed rendering

- Rotation caching

- Undo/redo support

- Extensible opcode-style dispatch system

It is designed as a learning-focused but architecturally serious implementation.

## ✨ Features

- 🎯 Command queue with opcode dispatch

- ⏱ Time-based animation (dt driven)

- 🧭 Logical vs render position separation

- 🖌 Persistent drawing surface (retained mode rendering)

- ↩ Undo / redo support

- 🔄 Rotation caching for turtle sprite

- 🎨 Flexible color handling

- 🧱 Minimal VM-style instruction system

- 🧩 Custom command injection

## 🧠 Architecture Overview

Unlike the standard turtle module, this implementation:

- Uses a **command queue** instead of immediate execution

- Separates:

    - _target_pos (logical destination)

    - _render_pos (interpolated visual position)

- Executes movement incrementally using delta time (dt)

- Uses an opcode table for fast dispatch

### Execution Flow

```
User calls forward()
→ Instruction enqueued
→ Update loop fetches opcode
→ Navigator updates target state
→ Interpolator moves render position
→ Pen marks path
→ Canvas commits lines
→ Screen renders final result
```

This resembles a minimal retained-mode rendering engine.

## 📦 Installation

Requirements:

- Python 3.10+

- pygame

Install pygame:

```batch
pip install pygame
```

Clone the repository:

```batch
git clone https://github.com/yourname/pygame-turtle.git
cd pygame-turtle
```

## 🚀 Quick Example

```python
import pygame
from turtle_engine import Screen, Turtle  # adjust import as needed

pygame.init()

screen = Screen(800, 600)

t = Turtle()
t.speed = 200

t.forward(150)
t.left(90)
t.forward(150)
t.circle(50)

screen.mainloop()
```

## 🧭 Core Components

`Navigator`

Handles movement logic:

- `forward(distance)`

- `goto(x, y)`

- `teleport(x, y)`

- `left(angle)`

- `right(angle)`

- `set_heading(angle)`

- `towards(x, y)`

- `circle(radius, steps, direction)`

Maintains:

- `_target_pos`

- `_render_pos`

- `heading`

- `speed`

---

`Pen`

Responsible for:

- Drawing state

- Visibility

- Path segmentation

- Stroke accumulation

---

`Turtle`

Combines `Pen` and `Navigator`.

Adds:

- Command queue

- Undo/redo

- Rotation cache

- Surface-backed canvas

- Sprite rendering

- Custom command support

---

`Screen`

Manages:

- Pygame surface

- Frame timing

- Background

- Update loop

- Multiple turtles

## 🧾 Command System

Instructions are stored as tuples:

```python
(CMD_OPCODE, arg1, arg2, ...)
```

Dispatch occurs via a global opcode table:

```python
_COMMAND_TABLE = [
    Navigator.forward,
    Navigator.goto,
    ...
]
```

This design:

- Avoids string lookups

- Avoids getattr

- Enables fast numeric dispatch

- Allows low-level extensibility

## 🎬 Animation Model

Movement is not instantaneous.

Each frame:

```python
delta = target - render_position
step = min(speed * dt, distance)
render_position += normalized(delta) * step
```

This ensures:

- Smooth animation

- Frame-rate independence

- Deterministic motion

## 🎨 Drawing Model

- Lines are stored in segments.

- Segments are committed to an off-screen surface.

- Static drawing lives on _canvas.

- Active segments are drawn during render.

- Sprite (figure) is rotated and cached.

## ↩ Undo / Redo

Supports:

- Undoing path segments

- Redoing segments

- Undoing queued commands (when applicable)

Undo depth is configurable.

## 🔄 Rotation Caching

To avoid repeated expensive transforms:

```python
self._rotation_cache[angle] = rotated_surface
```

Angles are cached to prevent redundant pygame.transform.rotate calls.

## 🧩 Custom Commands

You can inject custom instructions:

```python
t.custom_command(callable_or_opcode, *args)
```

Advanced users can extend the opcode table for new behaviors.

## 🎯 Design Goals

- Educational clarity

- Engine-style architecture

- Clean state separation

- Explicit command execution

- Minimal dynamic lookup

- Deterministic update cycle

## ⚠ Differences from Python's turtle

This implementation:

- Does not use Tkinter

- Does not execute commands immediately

- Is frame-driven, not call-driven

- Is built entirely on pygame

- Is more engine-oriented than teaching-oriented

## 📈 Performance Notes

The primary runtime cost comes from:

- pygame.draw.lines

- Surface blitting

- Surface rotation (cached)

Command dispatch overhead is minimal compared to rendering.

## 🛠 Future Improvements

Potential directions:

- Enum-based opcodes

- Bytecode-style instruction packing

- Batch mode (disable interpolation)

- Event hooks

- Timeline scheduling

- GPU-accelerated backend

- Multi-turtle synchronization

## 📄 License

MIT License

## 👨‍💻 Why This Exists

This project is an exploration of:

- Command interpreters

- Retained-mode rendering

- Engine-like architecture

- Clean state management

- Performance-aware Python design

It is both a learning project and a foundation for experimentation.