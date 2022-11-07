from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
import random
from functions import in_contact


class Monster(Widget):

    def __init__(self, game, x, y, **kwargs):
        super().__init__(**kwargs)
        self.death_animation_interval = None
        self.unskip_interval = None
        self.monster = None
        self.game = game
        self.sensitive = 15
        self.x, self.y = x, y
        self.w, self.h = self.game.cell_width, self.game.cell_height
        monster_type = random.randint(1, 4)
        match monster_type:
            case 1:
                self.source = "images/monsters/shit1.png"
            case 2:
                self.source = "images/monsters/hagivagi.png"
            case 3:
                self.source = "images/monsters/sirenhead.png"
            case 4:
                self.source = "images/monsters/train.png"
        self.current_direction = None
        self.distance_passed = 0
        self.x_pos = self.game.get_position_by_xy(self.x + self.w / 2,
                                                  self.y + self.h / 2)[0]
        self.y_pos = self.game.get_position_by_xy(self.x + self.w / 2,
                                                  self.y + self.h / 2)[1]
        self.monster_move_interval = None
        self.refresh_per_cell = .01
        self.speed = 20
        self.unkillable = True
        self.draw_monster()
        Clock.schedule_once(self.to_killable, 1)

    def to_killable(self, dt):
        self.unkillable = False
        self.change_direction()

    def draw_monster(self):
        with self.canvas:
            self.monster = Rectangle(pos=(self.x, self.y),
                                     size=(self.game.cell_width,
                                           self.game.cell_height),
                                     source=self.source)

    def change_direction(self):
        self.distance_passed = 0
        available_directions = self.get_available_directions()
        if self.current_direction in available_directions:
            if self.current_direction == 'left' and 'right' in available_directions:
                available_directions.remove('right')
            if self.current_direction == 'right' and 'left' in available_directions:
                available_directions.remove('left')
            if self.current_direction == 'up' and 'down' in available_directions:
                available_directions.remove('down')
            if self.current_direction == 'down' and 'up' in available_directions:
                available_directions.remove('up')
        if len(available_directions) != 0:
            result = available_directions[random.randint(0, len(available_directions) - 1)]
        else:
            result = 'skip'
        self.current_direction = result
        if self.current_direction != 'skip':
            self.monster_move_interval = Clock.schedule_interval(self.monster_move, self.refresh_per_cell)
        else:
            self.unskip_interval = Clock.schedule_interval(self.unskip, self.refresh_per_cell)

    def unskip(self, dt):
        available_directions = self.get_available_directions()
        if len(available_directions) != 0:
            self.unskip_interval.cancel()
            Clock.schedule_once(self.unskip_delay, 1)

    def unskip_delay(self, dt):
        self.change_direction()

    def get_available_directions(self):
        available_directions = []
        if self.game.level[self.y_pos - 1][self.x_pos - 1 - 1] not in {1, 3, 4}:
            available_directions.append('left')
        if self.game.level[self.y_pos - 1][self.x_pos - 1 + 1] not in {1, 3, 4}:
            available_directions.append('right')
        if self.game.level[self.y_pos - 1 + 1][self.x_pos - 1] not in {1, 3, 4}:
            available_directions.append('up')
        if self.game.level[self.y_pos - 1 - 1][self.x_pos - 1] not in {1, 3, 4}:
            available_directions.append('down')
        return available_directions

    def monster_move(self, dt):
        self.monster_step(self.current_direction)

    def monster_step(self, direction):
        if direction == 'skip':
            pass
        else:
            if direction == 'left':
                step = self.w / ((10 / self.speed) / self.refresh_per_cell)
                self.distance_passed += step
                if self.distance_passed >= self.w:
                    step = self.w - (self.distance_passed - step)
                    self.x -= step
                    self.x_pos -= 1
                    self.monster_move_interval.cancel()
                    self.change_direction()
                else:
                    self.x -= step
            elif direction == 'right':
                step = self.w / ((10 / self.speed) / self.refresh_per_cell)
                self.distance_passed += step
                if self.distance_passed >= self.w:
                    step = self.w - (self.distance_passed - step)
                    self.x += step
                    self.x_pos += 1
                    self.monster_move_interval.cancel()
                    self.change_direction()
                else:
                    self.x += step
            elif direction == 'up':
                step = self.h / ((10 / self.speed) / self.refresh_per_cell)
                self.distance_passed += step
                if self.distance_passed >= self.h:
                    step = self.h - (self.distance_passed - step)
                    self.y += step
                    self.y_pos += 1
                    self.monster_move_interval.cancel()
                    self.change_direction()
                else:
                    self.y += step
            elif direction == 'down':
                step = self.h / ((10 / self.speed) / self.refresh_per_cell)
                self.distance_passed += step
                if self.distance_passed >= self.h:
                    step = self.h - (self.distance_passed - step)
                    self.y -= step
                    self.y_pos -= 1
                    self.monster_move_interval.cancel()
                    self.change_direction()
                else:
                    self.y -= step
            self.monster.pos = (self.x, self.y)

            bx, by = self.game.bomberman.x, self.game.bomberman.y
            bw, bh = self.game.bomberman.get_size()

            if (self.game.bomberman.status == 'alive' and
                    in_contact(self.x, self.y, self.w, self.h, bx, by, bw, bh, self.sensitive)):
                self.game.bomberman.die()

    def die(self):
        if self.monster_move_interval is not None:
            self.monster_move_interval.cancel()
        self.death_animation_interval = Clock.schedule_interval(self.death_animate, 0.1)

    def death_animate(self, dt):
        self.opacity -= 0.1
        if self.opacity <= 0:
            self.death_animation_interval.cancel()
            self.canvas.clear()
            self.game.remove_widget(self)
            del self
