# 🐢 Advanced Turtle

**Advanced Turtle** is a modern, command-driven turtle graphics engine built on top of **pygame**.  
It reimagines Python’s classic `turtle` module with a focus on performance, extensibility, and modern design.

Inspired by the original CPython implementation, this project introduces a queue-based execution model, VM-style command dispatch, animation interpolation, and retained-mode rendering.

## ✨ Features

- 🧠 **Opcode-driven Command Queue** — Efficient, numeric dispatch instead of dynamic lookup  
- ⏱ **Frame-rate Independent Motion** — Movement interpolates with `dt` for smooth animation  
- 📌 **Logical vs Render Position** — Separation between internal state and visual rendering  
- ✍️ **Persistent Drawing Surface** — Path segments commit to an off-screen canvas  
- ↩️ **Undo / Redo Support**  
- 🔄 **Rotation Caching** — Efficient sprite rotation with caching  
- 🧩 **Minimal VM-style Instruction System** — Compact and extensible  
- 🏷 **Custom Commands & Injection** — Extendable beyond built-ins

## 🚀 Installation

Requirements:

- Python 3.10 or above  
- `pygame`

Install `pygame`:

```bash
pip install pygame
```

Clone the repository:

```batch
git clone https://github.com/NeoZett-School/Advanced-Turtle
cd Advanced-Turtle
```

## 🔧 Quick Start

Here's a simple example:

```python
import pygame
from pygame_turtle import Screen, Turtle

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

This code opens a window, creates a turtle, and draws a rectangle with a circle.

## 📐 Core Concepts

### 🐍 Navigator

Handles movement and orientation:

- `forward(distance)`
- `goto(x, y)`
- `teleport(x, y)`
- `left(angle)`, `right(angle)`
- `set_heading(angle)`
- `head_towards(x, y)`
- `distance(...)`
- `towards(...)`
- `circle(radius, steps, direction)`

Internally manages:

- `_target_pos`: next logical position
- `_render_pos`: interpolated current position
- `position`: alias to `_render_pos`
- `heading`
- `speed`

### ✏️ Pen

Tracks drawing state:

- Pen up / down
- Visibility
- Path segmentation
- Drawing accumulation on a canvas surface

---

### 🐢 Turtle

Combines Navigator and Pen into a command-driven actor.

Features:

- Command queue (deque)
- Undo / redo support
- Rotation cache for figures
- Persistent drawing (off-screen canvas)
- Custom command injection
- API similar to Python’s turtle (but frame-driven)

### 🖥 Screen

Wraps the `pygame` window:

Manages:

- Surface
- Timing (dt, FPS)
- Background
- Update loop
- Renders all active turtles

## 🧠 Command System

Suffix commands are enqueued as tuples:

```python
(self._command_queue.append((CMD_OPCODE, *args)))
```

Opcode values come from a global table:

```python
_COMMAND_TABLE = [
    Navigator.forward,
    Navigator.goto,
    ...
]
```

This design:

- avoids string lookups
- avoids getattr overhead
- allows fast dispatch
- supports extensibility

## ⏱ Animation Model

Movement is not instantaneous. Each frame:

```python
delta = target - render_position
step  = min(speed * dt, distance)
render_pos += normalized(delta) * step
```

This yields:

- smooth motion
- frame-rate independent animation
- deterministic simulation

## 📏 Drawing Model

- Path is stored in segments
- Static segments commit to the canvas
- Active drawing is rendered every frame
- Turtle figure (sprite) rotates smoothly
- Rotation cache is used to avoid repeated transforms

## ↩ Undo / Redo

Undo behavior supports:

- Path segment removal
- Redo path insertion
- Command stack rollback (when appropriate)

## 🚀 Extending the Engine

You can inject custom commands:

```python
t.custom_command(my_opcode, arg1, arg2, ...)
```

Where `my_opcode` can be either:

- a numeric opcode in _COMMAND_TABLE, or
- a callable (direct method)

## 🛠 Design Goals

- Educational clarity
- Clean execution model
- Minimal dynamic lookup
- Extensible command dispatch
- Smooth animation via interpolation

This isn’t a drop-in replacement for the default `turtle` — it’s an engine with its own execution style.

## 📈 Performance Notes

The largest costs during runtime are:

- pygame.draw.lines
- Surface blitting
- Sprite rotation (cached)

Command dispatch itself is low overhead compared to rendering workload.

## 📄 License

This project is licensed under the MIT License.

## 💡 Why This Exists

Advanced Turtle is an exploration in:

- Command scheduling
- Engine-style rendering
- Deterministic motion
- VM-style dispatch

It blends educational graphics with performance-aware Python design.