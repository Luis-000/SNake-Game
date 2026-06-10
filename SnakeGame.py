from tkinter import *
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 85
SPACE_SIZE = 100
BODY_PARTS = 3

# Color Scheme — cool gray + light blue palette
BG_COLOR        = "#1A1F2E"   # deep navy-gray background
GRID_COLOR      = "#1E2436"   # subtle grid lines
SNAKE_HEAD      = "#7EC8E3"   # bright light blue for head
SNAKE_BODY      = "#4A90B8"   # mid blue for body
SNAKE_OUTLINE   = "#A8DAEF"   # pale blue outline highlight
FOOD_COLOR      = "#E8F4F8"   # near-white food
FOOD_OUTLINE    = "#7EC8E3"   # light blue food outline
SCORE_COLOR     = "#7EC8E3"   # light blue score text
PANEL_COLOR     = "#141824"   # darker panel at top
TEXT_COLOR      = "#C8E8D6"   # soft gray-blue text
GAMEOVER_COLOR  = "#96E37E"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for idx, (x, y) in enumerate(self.coordinates):
            color   = SNAKE_HEAD if idx == 0 else SNAKE_BODY
            outline = SNAKE_OUTLINE
            r = 6
            square = canvas.create_rectangle(
                x + r, y, x + SPACE_SIZE - r, y + SPACE_SIZE,
                fill=color, outline="", tags="snake"
            )
            square2 = canvas.create_rectangle(
                x, y + r, x + SPACE_SIZE, y + SPACE_SIZE - r,
                fill=color, outline="", tags="snake"
            )
            oval = canvas.create_oval(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=color, outline=outline, width=1, tags="snake"
            )
            self.squares.append((square, square2, oval))


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH  // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        padding = 6
        # outer glow ring
        canvas.create_oval(
            x + padding - 4, y + padding - 4,
            x + SPACE_SIZE - padding + 4, y + SPACE_SIZE - padding + 4,
            fill="", outline=FOOD_OUTLINE, width=1, tags="food"
        )
        # main food dot
        canvas.create_oval(
            x + padding, y + padding,
            x + SPACE_SIZE - padding, y + SPACE_SIZE - padding,
            fill=FOOD_COLOR, outline=FOOD_OUTLINE, width=1, tags="food"
        )
        # small inner highlight
        canvas.create_oval(
            x + padding + 4, y + padding + 2,
            x + padding + 9, y + padding + 7,
            fill="#FFFFFF", outline="", tags="food"
        )


def draw_rounded_rect(canvas, x, y, w, h, r, fill, outline="", width=1, tags=""):
    """Draw a rectangle with rounded corners."""
    pts = [
        x+r, y,   x+w-r, y,
        x+w, y,   x+w, y+r,
        x+w, y+h-r, x+w, y+h,
        x+w-r, y+h, x+r, y+h,
        x, y+h,  x, y+h-r,
        x, y+r,  x, y,
        x+r, y
    ]
    return canvas.create_polygon(pts, smooth=True, fill=fill, outline=outline, width=width, tags=tags)


def draw_snake_segment(x, y, is_head=False):
    color   = SNAKE_HEAD if is_head else SNAKE_BODY
    outline = SNAKE_OUTLINE
    r = 8
    ids = []
    ids.append(canvas.create_rectangle(
        x + r, y, x + SPACE_SIZE - r, y + SPACE_SIZE,
        fill=color, outline="", tags="snake"
    ))
    ids.append(canvas.create_rectangle(
        x, y + r, x + SPACE_SIZE, y + SPACE_SIZE - r,
        fill=color, outline="", tags="snake"
    ))
    ids.append(canvas.create_oval(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill=color, outline=outline, width=1, tags="snake"
    ))
    return tuple(ids)


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    # Draw new head (and recolor old head as body)
    new_head = draw_snake_segment(x, y, is_head=True)
    snake.squares.insert(0, new_head)

    # Recolor the old head to body color
    if len(snake.squares) > 1:
        for part_id in snake.squares[1]:
            try:
                canvas.itemconfig(part_id, fill=SNAKE_BODY)
            except Exception:
                pass

    ate_food = (x == food.coordinates[0] and y == food.coordinates[1])

    if ate_food:
        global score
        score += 1
        score_label.config(text=f"{score}")
        canvas.delete("food")
        food = Food()
    else:
        # Remove tail
        tail = snake.squares[-1]
        for part_id in tail:
            canvas.delete(part_id)
        del snake.squares[-1]
        del snake.coordinates[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    opposites = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
    if new_direction != opposites.get(direction):
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over():
    canvas.delete(ALL)

    cw = canvas.winfo_width()
    ch = canvas.winfo_height()
    cx, cy = cw / 2, ch / 2

    # Dim overlay
    canvas.create_rectangle(0, 0, cw, ch, fill="#0D1017", outline="")

    # Panel background
    panel_w, panel_h = 420, 220
    px, py = cx - panel_w/2, cy - panel_h/2
    draw_rounded_rect(canvas, px, py, panel_w, panel_h, 18,
                      fill="#1A2035", outline=SNAKE_OUTLINE, width=1)

    canvas.create_text(cx, cy - 50,
                       font=("Helvetica", 48, "bold"),
                       text="GAME OVER",
                       fill=GAMEOVER_COLOR)
    canvas.create_text(cx, cy + 20,
                       font=("Helvetica", 18),
                       text=f"Final Score: {score}",
                       fill=TEXT_COLOR)
    canvas.create_text(cx, cy + 60,
                       font=("Helvetica", 13),
                       text="Close the window to exit",
                       fill="#5A6A7A")


# ── Window setup ──────────────────────────────────────────────
window = Tk()
window.title("Snake")
window.resizable(False, False)
window.configure(bg=PANEL_COLOR)

score = 0
direction = "down"

# Top panel
top_panel = Frame(window, bg=PANEL_COLOR, pady=10)
top_panel.pack(fill=X)

Label(top_panel, text="SCORE", font=("Helvetica", 11, "bold"),
      bg=PANEL_COLOR, fg="#4A6A7A").pack()
score_label = Label(top_panel, text="0", font=("Helvetica", 36, "bold"),
                    bg=PANEL_COLOR, fg=SCORE_COLOR)
score_label.pack()

# Thin separator line
sep = Frame(window, height=1, bg="#2A3550")
sep.pack(fill=X)

canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT,
                width=GAME_WIDTH, highlightthickness=0)
canvas.pack()

# Draw subtle grid
for gx in range(0, GAME_WIDTH, SPACE_SIZE):
    canvas.create_line(gx, 0, gx, GAME_HEIGHT, fill=GRID_COLOR, width=1)
for gy in range(0, GAME_HEIGHT, SPACE_SIZE):
    canvas.create_line(0, gy, GAME_WIDTH, gy, fill=GRID_COLOR, width=1)

window.update()
ww = window.winfo_width()
wh = window.winfo_height()
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
x = int(sw / 2 - ww / 2)
y = int(sh / 2 - wh / 2)
window.geometry(f"{ww}x{wh}+{x}+{y}")

window.bind("<Left>",  lambda e: change_direction("left"))
window.bind("<Right>", lambda e: change_direction("right"))
window.bind("<Up>",    lambda e: change_direction("up"))
window.bind("<Down>",  lambda e: change_direction("down"))

snake = Snake()
food  = Food()

next_turn(snake, food)
window.mainloop()