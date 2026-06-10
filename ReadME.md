# 🐍 Snake Game

A classic Snake game built from scratch in Python using the `tkinter` library — no game engines, no external dependencies, just pure Python.

---

## About the Project

Snake is one of those timeless games that almost every programmer ends up building at some point, and for good reason. It touches on a surprising number of fundamental concepts — game loops, collision detection, dynamic data structures, real-time input handling, and rendering — all wrapped up in something genuinely fun to play.

This project started as a bare-bones skeleton and was built up piece by piece: first the window, then the snake, then movement, food, scoring, and finally collision detection and a game-over screen. Every part of the game logic is hand-written, which makes it a great read if you want to understand how a simple game actually ticks under the hood.

The final version features a custom visual design with a navy-gray and light blue color scheme, rounded snake segments, a glowing food dot, a score panel, and a polished game-over screen — all drawn using `tkinter`'s canvas primitives.

---

## Features

- Smooth, rounded snake rendering with a distinct head color
- Glowing food with an inner highlight
- Real-time score display in a clean top panel
- Wall and self-collision detection
- Reverse-direction prevention (no accidental 180° turns)
- Centered window on any screen resolution
- Subtle background grid for depth
- Polished game-over screen with final score

---

## Getting Started

### Prerequisites

Python 3.x is all you need. `tkinter` ships with the standard library on most systems.

To verify you have it:

```bash
python3 -c "import tkinter; print('tkinter OK')"
```

If you're on Linux and it's missing:

```bash
sudo apt-get install python3-tk
```

### Running the Game

```bash
python3 SnakeGame.py
```

---

## How to Play

| Key     | Action     |
| ------- | ---------- |
| ↑ Arrow | Move up    |
| ↓ Arrow | Move down  |
| ← Arrow | Move left  |
| → Arrow | Move right |

Eat the glowing food dots to grow and increase your score. Don't hit the walls or your own tail — one collision ends the run.

---

## Project Structure

```
SnakeGame.py   # Main game file — everything lives here
README.md
```

The game is intentionally kept as a single file. It's easy to read top to bottom: constants → classes → game logic → window setup.

---

## Customization

All the key settings live at the top of the file as constants:

```python
SPEED       = 85     # Lower = faster snake (milliseconds per frame)
SPACE_SIZE  = 35     # Grid cell size in pixels
BODY_PARTS  = 3      # Starting snake length
GAME_WIDTH  = 700    # Canvas width
GAME_HEIGHT = 700    # Canvas height
```

The full color palette is also defined there if you want to swap out the scheme.

---

## What I Learned

Building this from scratch — rather than dropping in a library — meant solving some genuinely interesting problems:

- **Game loop without threads:** `window.after()` drives the loop by scheduling the next frame on tkinter's own event queue, keeping everything on one thread.
- **Rounded shapes in tkinter:** tkinter has no native rounded-rectangle primitive. Each snake segment is actually three overlapping shapes (two rectangles + one oval) composited together.
- **Coordinate-based collision:** the grid snapping (all positions are multiples of `SPACE_SIZE`) makes collision checks simple integer comparisons rather than bounding-box math.

---

## License

MIT — do whatever you like with it.
