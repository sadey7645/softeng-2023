import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("간단한 지렁이 게임")

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="black")
        self.canvas.pack()

        self.snake = [[100, 100], [90, 100], [80, 100]]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0

        self.master.bind("<Key>", self.change_direction)

        self.score_label = tk.Label(self.master, text="점수: 0", font=("Helvetica", 12), fg="white")
        self.score_label.pack()

        self.game_loop()

    def create_food(self):
        x = random.randrange(1, 39) * 10
        y = random.randrange(1, 39) * 10
        self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red", tags="food")
        return [x, y]

    def change_direction(self, event):
        key = event.keysym
        if key == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif key == "Down" and not self.direction == "Up":
            self.direction = "Down"
        elif key == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif key == "Right" and not self.direction == "Left":
            self.direction = "Right"

    def move_snake(self):
        head = list(self.snake[0])
        if self.direction == "Up":
            head[1] -= 10
        elif self.direction == "Down":
            head[1] += 10
        elif self.direction == "Left":
            head[0] -= 10
        elif self.direction == "Right":
            head[0] += 10
        self.snake.insert(0, head)

    def check_collision(self):
        head = self.snake[0]
        if (
            head[0] < 0 or head[0] >= 400 or
            head[1] < 0 or head[1] >= 400 or
            head in self.snake[1:]
        ):
            return True
        return False

    def check_food_collision(self):
        head = self.snake[0]
        if head == self.food:
            self.score += 1
            self.score_label.config(text=f"점수: {self.score}")
            return True
        return False

    def update_canvas(self):
        self.canvas.delete("all")
        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green", tags="snake"
            )
        self.canvas.create_rectangle(
            self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red", tags="food"
        )

    def game_loop(self):
        if not self.check_collision():
            self.move_snake()
            if self.check_food_collision():
                self.food = self.create_food()
            else:
                self.snake.pop()
            self.update_canvas()
            self.master.after(100, self.game_loop)
        else:
            self.canvas.create_text(
                200, 200, text=f"게임 종료, 최종 점수: {self.score}", font=("Helvetica", 20), fill="white", tags="game_over"
            )

# 메인 윈도우 생성
root = tk.Tk()
root.title("게임 시작 창")

# "게임 시작" 버튼 추가
start_button = tk.Button(root, text="게임 시작", command=lambda: SnakeGame(tk.Toplevel(root)))
start_button.pack(pady=20)

# 메인 루프 시작
root.mainloop()
