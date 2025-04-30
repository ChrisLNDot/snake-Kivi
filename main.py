
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from random import randint

Window.size = (800, 480)  # Modo horizontal

CELL_SIZE = 20

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = [[5, 5]]
        self.food = [randint(0, 39), randint(0, 23)]
        self.direction = "RIGHT"
        self.running = False

        self.grid_width = int(self.width / CELL_SIZE)
        self.grid_height = int(self.height / CELL_SIZE)

        Clock.schedule_interval(self.update, 0.2)

    def on_size(self, *args):
        self.grid_width = int(self.width / CELL_SIZE)
        self.grid_height = int(self.height / CELL_SIZE)

    def start_game(self):
        self.snake = [[5, 5]]
        self.food = [randint(0, 39), randint(0, 23)]
        self.direction = "RIGHT"
        self.running = True

    def change_direction(self, new_dir):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if self.direction != opposites.get(new_dir):
            self.direction = new_dir

    def update(self, dt):
        if not self.running:
            return

        head = self.snake[-1][:]
        if self.direction == "UP": head[1] += 1
        if self.direction == "DOWN": head[1] -= 1
        if self.direction == "LEFT": head[0] -= 1
        if self.direction == "RIGHT": head[0] += 1

        if head in self.snake or head[0] < 0 or head[1] < 0 or head[0] >= 40 or head[1] >= 24:
            self.running = False
            return

        self.snake.append(head)
        if head == self.food:
            self.food = [randint(0, 39), randint(0, 23)]
        else:
            self.snake.pop(0)

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            from kivy.graphics import Color, Rectangle

            Color(0, 1, 0)
            for x, y in self.snake:
                Rectangle(pos=(x * CELL_SIZE, y * CELL_SIZE), size=(CELL_SIZE, CELL_SIZE))

            Color(1, 0, 0)
            fx, fy = self.food
            Rectangle(pos=(fx * CELL_SIZE, fy * CELL_SIZE), size=(CELL_SIZE, CELL_SIZE))

class SnakeApp(App):
    def build(self):
        root = BoxLayout(orientation='horizontal')
        self.game = SnakeGame()

        controls = BoxLayout(orientation='vertical', size_hint=(0.2, 1))
        btn_up = Button(text="Arriba")
        btn_down = Button(text="Abajo")
        btn_left = Button(text="Izquierda")
        btn_right = Button(text="Derecha")
        btn_start = Button(text="Jugar")

        btn_up.bind(on_press=lambda x: self.game.change_direction("UP"))
        btn_down.bind(on_press=lambda x: self.game.change_direction("DOWN"))
        btn_left.bind(on_press=lambda x: self.game.change_direction("LEFT"))
        btn_right.bind(on_press=lambda x: self.game.change_direction("RIGHT"))
        btn_start.bind(on_press=lambda x: self.game.start_game())

        for b in [btn_up, btn_down, btn_left, btn_right, btn_start]:
            controls.add_widget(b)

        root.add_widget(self.game)
        root.add_widget(controls)
        return root

if __name__ == '__main__':
    SnakeApp().run()
