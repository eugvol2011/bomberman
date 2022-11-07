import random

from levels import gen_level
from bomberman import Bomberman
from field import Field
from woodenbox import Woodenbox
from monster import Monster

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', 0)
Config.set('graphics', 'left', 0)
Config.set('graphics', 'fullscreen', True)


class Game(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = gen_level()
        self.field_width_ratio = 1
        self.cell_width = Window.width * self.field_width_ratio / len(self.level[0])
        self.cell_height = Window.height / len(self.level)
        self.keys_pressed = set()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.field = Field(self)
        self.add_widget(self.field)
        self.wooden_boxes = []
        for xy in self.get_list_of_xy_by_value(4):
            woodenbox = Woodenbox(self, xy[0], xy[1])
            self.add_widget(woodenbox)
            self.wooden_boxes.append(woodenbox)
        self.bomberman = Bomberman(self)
        self.add_widget(self.bomberman)
        Clock.schedule_interval(self.bomber_move, 0)
        self.door = None
        self.monsters = []
        for xy in self.get_list_of_xy_by_value(5):
            monster = Monster(self, xy[0], xy[1])
            self.add_widget(monster)
            self.monsters.append(monster)
        secrets = ['heart', 'bomb', 'power', 'key', 'bomb', 'door']
        self.list_of_secrets = set()
        i = 0
        list_of_secret_boxes = []
        for secret in secrets:
            secret_woodenbox = self.wooden_boxes[random.randint(0, len(self.wooden_boxes) - 2 - i)]
            secret_woodenbox.secret = secret
            self.wooden_boxes.remove(secret_woodenbox)
            self.wooden_boxes.append(secret_woodenbox)
            list_of_secret_boxes.append(secret_woodenbox)
            i += 1

    def get_list_of_xy_by_value(self, value: int):
        result_list = []
        for row in range(0, len(self.level)):
            for col in range(0, len(self.level[row])):
                if self.level[row][col] == value:
                    xy = self.get_xy_by_position(col + 1, row + 1)
                    result_list.append(xy)
        return result_list

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keys_pressed:
            self.keys_pressed.remove(text)
        if text == 'spacebar' and self.bomberman.status == 'alive':
            self.bomberman.put_bomb(self.bomberman.bomb_delay, self.bomberman.power)
        self.bomberman.distance = 0

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.keys_pressed.add(keycode[1])

    def bomber_move(self, dt):
        if self.bomberman.status == 'alive':
            move_step = self.bomberman.speed * dt
            self.bomberman.distance += move_step
            animation_change_distance = 60

            if 'right' in self.keys_pressed:
                self.object_move(self.bomberman, 'right', move_step, {1, 3, 4})
                self.bomberman.canvas.clear()
                self.bomberman.draw_bomberman("images/bomberman/bomberman-right-" +
                                              str(self.bomberman.step_frame) + ".png")
                if self.bomberman.distance >= animation_change_distance:
                    self.bomberman.distance = 0
                    self.bomberman.step_frame += 1
                    if self.bomberman.step_frame == 6:
                        self.bomberman.step_frame = 1
            elif 'left' in self.keys_pressed:
                self.object_move(self.bomberman, 'left', move_step, {1, 3, 4})
                self.bomberman.canvas.clear()
                self.bomberman.draw_bomberman("images/bomberman/bomberman-left-" +
                                              str(self.bomberman.step_frame) + ".png")
                if self.bomberman.distance >= animation_change_distance:
                    self.bomberman.distance = 0
                    self.bomberman.step_frame += 1
                    if self.bomberman.step_frame == 6:
                        self.bomberman.step_frame = 1
            elif 'up' in self.keys_pressed:
                self.object_move(self.bomberman, 'up', move_step, {1, 3, 4})
                self.bomberman.canvas.clear()
                self.bomberman.draw_bomberman("images/bomberman/bomberman-up-" +
                                              str(self.bomberman.step_frame) + ".png")
                if self.bomberman.distance >= animation_change_distance:
                    self.bomberman.distance = 0
                    self.bomberman.step_frame += 1
                    if self.bomberman.step_frame == 6:
                        self.bomberman.step_frame = 1
            elif 'down' in self.keys_pressed:
                self.object_move(self.bomberman, 'down', move_step, {1, 3, 4})
                self.bomberman.canvas.clear()
                self.bomberman.draw_bomberman("images/bomberman/bomberman-down-" +
                                              str(self.bomberman.step_frame) + ".png")
                if self.bomberman.distance >= animation_change_distance:
                    self.bomberman.distance = 0
                    self.bomberman.step_frame += 1
                    if self.bomberman.step_frame == 6:
                        self.bomberman.step_frame = 1

    def object_move(self, obj, direction: str, move_step: float, obst: set):
        cur_width, cur_height = obj.get_size()
        clearance = 3
        match direction:
            case 'right':
                x = obj.x + cur_width + move_step - clearance
                y1 = obj.y + cur_height - clearance
                y2 = obj.y + clearance
                if self.get_position_by_xy(x, y1)[2] not in obst and self.get_position_by_xy(x, y2)[2] not in obst:
                    obj.x += move_step
            case 'left':
                x = obj.x - move_step + clearance
                y1 = obj.y + cur_height - clearance
                y2 = obj.y + clearance
                if self.get_position_by_xy(x, y1)[2] not in obst and self.get_position_by_xy(x, y2)[2] not in obst:
                    obj.x -= move_step
            case 'up':
                x1 = obj.x + clearance
                x2 = obj.x + cur_width - clearance
                y = obj.y + cur_height + move_step - clearance
                if self.get_position_by_xy(x1, y)[2] not in obst and self.get_position_by_xy(x2, y)[2] not in obst:
                    obj.y += move_step
            case 'down':
                x1 = obj.x + clearance
                x2 = obj.x + cur_width - clearance
                y = obj.y - move_step + clearance
                if self.get_position_by_xy(x1, y)[2] not in obst and self.get_position_by_xy(x2, y)[2] not in obst:
                    obj.y -= move_step
            case 'skip':
                pass
            case _:
                print('Error occurred: wrong direction in object_move')

    def get_position_by_xy(self, x, y):
        if x % self.cell_width == 0:
            pos_x = int(x / self.cell_width)
        else:
            pos_x = int(x / self.cell_width) + 1
        if y % self.cell_height == 0:
            pos_y = int(y / self.cell_height)
        else:
            pos_y = int(y / self.cell_height) + 1
        pos_value = self.level[pos_y - 1][pos_x - 1]
        return pos_x, pos_y, pos_value

    def get_xy_by_position(self, pos_x, pos_y):
        return self.cell_width * (pos_x - 1), self.cell_height * (pos_y - 1)
