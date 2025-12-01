from tkinter import *
import random


GAME_WIDTH = 800
GAME_HEIGHT = 800
NUM_PARTS = 3
SQUARE_SIZE = 50
SNAKE_COLOR = "#3483eb"
FOOD_COLOR = "#eb343d"
BACKGROUND_COLOR = "#ffffff"
SPEED = 50


class Snake:
    def __init__(self):
        self.body_size = NUM_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, NUM_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SQUARE_SIZE, y + SQUARE_SIZE,
                fill=SNAKE_COLOR, tag='snake'
            )
            self.squares.append(square)


class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SQUARE_SIZE) - 1) * SQUARE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SQUARE_SIZE) - 1) * SQUARE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(
            x, y, x + SQUARE_SIZE, y + SQUARE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )


def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SQUARE_SIZE

    elif direction == 'down':
        y += SQUARE_SIZE

    elif direction == 'left':
        x -= SQUARE_SIZE

    elif direction == 'right':
        x += SQUARE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SQUARE_SIZE, y + SQUARE_SIZE,
        fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text='Score:{}'.format(score))

        canvas.delete("food")
        food = Food()

    else:

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        death()
    else:
        window.after(SPEED, next_turn, snake, food)


def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


# -----------------------------
# NEW FUNCTION: RESTART GAME
# -----------------------------
def restart_game():
    global snake, food, direction, score

    # Reset everything
    canvas.delete(ALL)
    score = 0
    direction = 'down'

    label.config(text=f"Score: {score}")

    # Create new snake/food
    snake = Snake()
    food = Food()

    # Start game loop
    next_turn(snake, food)


# -----------------------------
# UPDATED DEATH FUNCTION
# -----------------------------
def death():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 - 40,
        font=('consolas', 70),
        text="You Died",
        fill='red',
        tag='dead'
    )

    # ADD REPLAY BUTTON
    replay_button = Button(
        window, text="Play Again", font=('consolas', 30),
        command=restart_game
    )
    canvas.create_window(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 40,
        window=replay_button
    )


# -----------------------------
# WINDOW SETUP
# -----------------------------
window = Tk()
window.title('squirmy')
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text='Score:{}'.format(score), font=('ariel', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR,
                height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f'{window_width}x{window_height}+{x}+{y}')

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# START THE GAME
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
