from kivy.clock import Clock

from bomb import Bomb
from woodenbox import Secret

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle


class Bomberman(Widget):

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.x = 0
        self.y = 0
        self.initial_x, self.initial_y = None, None
        self.source = "images/bomberman/bomberman-right-1.png"
        self.new_bomb_pos = None
        self.wait_out_of_bomb_interval = None
        self.death_animation_interval = None
        self.bomber = None
        self.game = game
        self.speed = 300
        self.initial_size_ratio = .8
        self.size_ratio = self.initial_size_ratio
        self.max_bombs = 1
        self.power = 2
        self.bomb_delay = 3
        self.bombs = set()
        self.step_frame = 1
        self.distance = 0
        self.lives = 3
        self.has_key = False
        self.status = 'alive'
        self.draw_bomberman()

    def draw_bomberman(self, source=None):
        if source is None:
            for row in range(0, len(self.game.level)):
                for col in range(0, len(self.game.level[row])):
                    if self.game.level[row][col] == 2:
                        self.x = self.game.get_xy_by_position(col + 1, row + 1)[0]
                        self.y = self.game.get_xy_by_position(col + 1, row + 1)[1]
                        self.initial_x, self.initial_y = self.x, self.y
        else:
            self.source = source
        with self.canvas:
            self.bomber = Rectangle(pos=(self.x, self.y),
                                    size=(self.game.cell_width * self.size_ratio,
                                          self.game.cell_height * self.size_ratio),
                                    source=self.source)

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def get_xy(self):
        return self.bomber.pos

    def get_size(self):
        return self.bomber.size

    def put_bomb(self, delay, power):
        if len(self.bombs) < self.max_bombs and self.wait_out_of_bomb_interval is None:
            bomber_center_x = self.get_xy()[0] + self.get_size()[0] / 2
            bomber_center_y = self.get_xy()[1] + self.get_size()[1] / 2
            bomber_center_pos = self.game.get_position_by_xy(bomber_center_x, bomber_center_y)
            if bomber_center_pos[2] != 3:
                new_bomb_xy = self.game.get_xy_by_position(bomber_center_pos[0], bomber_center_pos[1])
                self.new_bomb_pos = bomber_center_pos
                new_bomb = Bomb(self.game, delay, power, new_bomb_xy[0], new_bomb_xy[1])
                self.game.remove_widget(self)
                self.game.add_widget(new_bomb)
                self.game.add_widget(self)
                self.bombs.add(new_bomb)
                self.wait_out_of_bomb_interval = Clock.schedule_interval(self.wait_out_of_bomb, 0)

    def wait_out_of_bomb(self, dt):
        bomber_center_x = self.get_xy()[0] + self.get_size()[0] / 2
        bomber_center_y = self.get_xy()[1] + self.get_size()[1] / 2
        bomber_center_pos = self.game.get_position_by_xy(bomber_center_x, bomber_center_y)
        if self.new_bomb_pos[0] != bomber_center_pos[0] or self.new_bomb_pos[1] != bomber_center_pos[1]:
            self.game.level[self.new_bomb_pos[1] - 1][self.new_bomb_pos[0] - 1] = 3
            self.wait_out_of_bomb_interval.cancel()
            self.wait_out_of_bomb_interval = None

    def die(self):
        self.status = 'dead'
        self.canvas.clear()
        self.size_ratio = 1
        grave_xy = self.game.get_xy_by_position(
            self.game.get_position_by_xy(self.x + (self.game.cell_width * self.size_ratio / 2),
                                         self.y + (self.game.cell_height * self.size_ratio / 2))[0],
            self.game.get_position_by_xy(self.x + (self.game.cell_width * self.size_ratio / 2),
                                         self.y + (self.game.cell_height * self.size_ratio / 2))[1])
        self.x, self.y = grave_xy[0], grave_xy[1]
        self.draw_bomberman("images/grave.png")
        self.death_animation_interval = Clock.schedule_interval(self.death_animate, 0.1)

    def death_animate(self, dt):
        self.opacity -= 0.1
        if self.opacity <= 0:
            self.death_animation_interval.cancel()
            self.canvas.clear()
            self.lives -= 1
            if self.lives == 0:
                with self.canvas:
                    w, h = self.game.width / 3, self.game.height / 3
                    x, y = self.game.width / 2 - w / 2, self.game.height / 2 - h / 2
                    Rectangle(pos=(x, y),
                              size=(w, h),
                              source='images/gameover.png')
                self.opacity = 1
            else:
                if self.has_key:
                    self.has_key = False
                    secret = Secret(self.game, self.x, self.y, 'key')
                    self.game.add_widget(secret)
                self.size_ratio = self.initial_size_ratio
                self.x, self.y = self.initial_x, self.initial_y
                self.draw_bomberman("images/bomberman/bomberman-right-1.png")
                self.opacity = 1
                self.status = 'alive'
