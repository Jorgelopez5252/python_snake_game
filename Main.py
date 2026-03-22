from tkinter import *
import random
import os

# CONSTANTS
GAME_WIDTH = 700
GAME_HEIGHT = 500
SPACE_SIZE = 20  # 🔥 smaller = smoother
BODY_PARTS = 3
BASE_SPEED = 80  # 🔥 faster updates

SNAKE_COLOR = "#39FF14"
FOOD_COLOR = "#FF3131"
BACKGROUND_COLOR = "#000000"

HIGH_SCORE_FILE = "highscore.txt"


def play_beep():
    try:
        import winsound
        winsound.Beep(800, 100)
    except:
        print("\a")


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    return 0


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))


class Snake:

    def __init__(self):
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append((0, 0))

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR,
                outline="#00FFAA",
                width=1,
                tag="snake"
            )
            self.squares.append(square)


class Food:

    def __init__(self):
        while True:
            x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

            if (x, y) not in snake.coordinates:
                break

        self.coordinates = (x, y)

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR,
            outline="#FFAAAA",
            width=1,
            tag="food"
        )


def next_turn(snake, food):

    global score, speed

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill=SNAKE_COLOR,
        outline="#00FFAA",
        width=1,
        tag="snake"
    )
    snake.squares.insert(0, square)

    if snake.coordinates[0] == food.coordinates:

        play_beep()

        score += 1
        label.config(text=f"Score:{score}  High:{high_score}")

        # 🔥 smoother speed scaling
        speed = max(30, BASE_SPEED - (score * 2))

        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if (x, y) == body_part:
            return True

    return False


def game_over():
    global high_score

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    canvas.delete(ALL)

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 - 40,
        font=("Arial", 40),
        text="GAME OVER",
        fill="red"
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2,
        font=("Arial", 20),
        text=f"Score: {score}  High: {high_score}",
        fill="white"
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 40,
        font=("Arial", 20),
        text="Press R to Restart",
        fill="white"
    )


def restart_game(event=None):
    global snake, food, score, direction, speed

    canvas.delete(ALL)

    score = 0
    direction = "down"
    speed = BASE_SPEED

    label.config(text=f"Score:{score}  High:{high_score}")

    snake = Snake()
    food = Food()

    next_turn(snake, food)


# 🎨 Animated background
grid_offset = 0

def animate_background():
    global grid_offset

    canvas.delete("grid")

    grid_offset = (grid_offset + 1) % SPACE_SIZE  # slower scroll

    for i in range(0, GAME_WIDTH, SPACE_SIZE):
        canvas.create_line(
            i + grid_offset, 0,
            i + grid_offset, GAME_HEIGHT,
            fill="#0a0a0a",
            tag="grid"
        )

    for i in range(0, GAME_HEIGHT, SPACE_SIZE):
        canvas.create_line(
            0, i + grid_offset,
            GAME_WIDTH, i + grid_offset,
            fill="#0a0a0a",
            tag="grid"
        )

    canvas.tag_lower("grid")

    window.after(30, animate_background)


# WINDOW SETUP
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
speed = BASE_SPEED
direction = "down"
high_score = load_high_score()

label = Label(window, text=f"Score:0  High:{high_score}", font=("Arial", 25))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR,
                height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center window
x = int((window.winfo_screenwidth()/2) - (window.winfo_width()/2))
y = int((window.winfo_screenheight()/2) - (window.winfo_height()/2))
window.geometry(f"+{x}+{y}")

# Controls
window.bind("<Left>", lambda e: change_direction("left"))
window.bind("<Right>", lambda e: change_direction("right"))
window.bind("<Up>", lambda e: change_direction("up"))
window.bind("<Down>", lambda e: change_direction("down"))
window.bind("r", restart_game)
window.bind("R", restart_game)

# Start
snake = Snake()
food = Food()

animate_background()
next_turn(snake, food)

window.mainloop()