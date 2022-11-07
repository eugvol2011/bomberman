from kivy.clock import Clock

from woodenbox import Secret
from door import Door
from monster import Monster

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

from functions import in_contact


class Fire(Widget):
    def __init__(self, game, fire_type: str, direction: str, x, y, bomb, **kwargs):
        super().__init__(**kwargs)
        self.source = None
        self.game = game
        self.bomb = bomb
        self.fire = None
        self.size_ratio = 1
        self.x = x
        self.y = y
        self.w, self.h = self.game.cell_width * self.size_ratio, self.game.cell_height * self.size_ratio
        self.direction = direction
        self.type = fire_type
        self.animation_frame = 2
        self.sensitive = 15  # the more the value is the less sensitive
        self.draw_fire()
        self.fire_animation_interval = Clock.schedule_interval(self.fire_animate, 1 / 7)

    def draw_fire(self, source=None):
        if source is None:
            self.source = 'images/explosion/' + self.type + '-1-' + self.direction + '.png'
        else:
            self.source = source
        with self.canvas:
            self.fire = Rectangle(pos=(self.x, self.y),
                                  size=(self.game.cell_width * self.size_ratio,
                                        self.game.cell_height * self.size_ratio),
                                  source=self.source)

    def fire_animate(self, dt):
        self.canvas.clear()
        self.draw_fire('images/explosion/' + self.type + '-' +
                       str(self.animation_frame) + '-' + self.direction + '.png')
        self.animation_frame += 1
        # --- destroy a wooden box / trigger another bomb
        if self.animation_frame == 6:
            fire_xy_pos = self.game.get_position_by_xy(self.x + 1, self.y + 1)
            if fire_xy_pos[2] == 4:
                for woodenbox in self.game.wooden_boxes:
                    if woodenbox.xy_pos == fire_xy_pos[0:2]:
                        woodenbox.canvas.clear()
                        self.game.remove_widget(woodenbox)
                        self.game.wooden_boxes.remove(woodenbox)
                        if woodenbox.secret == 'key':
                            secret = Secret(self.game, self.x, self.y, 'key')
                            self.game.add_widget(secret)
                        elif woodenbox.secret == 'heart':
                            secret = Secret(self.game, self.x, self.y, 'heart')
                            self.game.add_widget(secret)
                        elif woodenbox.secret == 'power':
                            secret = Secret(self.game, self.x, self.y, 'power')
                            self.game.add_widget(secret)
                        elif woodenbox.secret == 'bomb':
                            secret = Secret(self.game, self.x, self.y, 'bomb')
                            self.game.add_widget(secret)
                        elif woodenbox.secret == 'door':
                            self.game.door = Door(self.game, self.x, self.y)
                            self.game.add_widget(self.game.door)
                        del woodenbox
                        self.game.level[fire_xy_pos[1] - 1][fire_xy_pos[0] - 1] = 0
                        break
            # -- trigger bombs in nearby
            if fire_xy_pos[2] == 3:
                for bomb in self.game.bomberman.bombs:
                    if bomb.xy_pos == fire_xy_pos[0:2]:
                        bomb.trigger_interval.cancel()
                        bomb.explode(0)
                        break
            # ---
        # -- kill secret
        if self.animation_frame == 5:
            copy_of_list_of_secrets = self.game.list_of_secrets.copy()
            for secret in copy_of_list_of_secrets:
                bx, by = secret.x, secret.y
                bw, bh = secret.w, secret.h
                if in_contact(self.x, self.y, self.w, self.h, bx, by, bw, bh, self.sensitive):
                    secret.die()
            del copy_of_list_of_secrets

            if self.game.door is not None and in_contact(self.x, self.y, self.w, self.h,
                                                         self.game.door.x, self.game.door.y,
                                                         self.game.door.w, self.game.door.h, self.sensitive):
                monster = Monster(self.game, self.x, self.y)
                self.game.add_widget(monster)
                self.game.monsters.append(monster)
        # ---
        # --- kill bomberman
        bx, by = self.game.bomberman.x, self.game.bomberman.y
        bw, bh = self.game.bomberman.get_size()
        if self.game.bomberman.status == 'alive' and in_contact(self.x, self.y, self.w, self.h, bx, by, bw, bh,
                                                                self.sensitive):
            self.game.bomberman.die()
        # ---
        # -- kill monster
        for monster in self.game.monsters:
            bx, by = monster.x, monster.y
            bw, bh = monster.w, monster.h
            if not monster.unkillable and in_contact(self.x, self.y, self.w, self.h, bx, by, bw, bh, self.sensitive):
                monster.die()
        # ---

        if self.animation_frame == 8:
            self.fire_animation_interval.cancel()
            self.game.remove_widget(self.bomb)
            self.game.bomberman.bombs.discard(self.bomb)
            del self.bomb
            self.game.remove_widget(self)
            if self.game.bomberman.wait_out_of_bomb_interval is not None and self.type == 'center':
                self.game.bomberman.wait_out_of_bomb_interval.cancel()
                self.game.bomberman.wait_out_of_bomb_interval = None
            del self


class Bomb(Widget):
    def __init__(self, game, delay, power, x, y, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.center_pos = None
        self.explosion_animation_interval = None
        self.x = x
        self.y = y
        self.xy_pos = self.game.get_position_by_xy(self.x + 1, self.y + 1)[0:2]
        self.bomb = None
        self.size_ratio = 1
        self.delay = delay
        self.power = power
        self.pic = "images/bomb/bomb1.png"
        self.draw_bomb(self.pic)
        self.trigger_interval = Clock.schedule_once(self.explode, self.delay)
        self.tick_animation_interval = Clock.schedule_interval(self.tick_animate, 0.5)

    def draw_bomb(self, source: str):
        with self.canvas:
            self.bomb = Rectangle(pos=(self.x, self.y),
                                  size=(self.game.cell_width * self.size_ratio,
                                        self.game.cell_height * self.size_ratio),
                                  source=source)
        self.pic = source

    def explode(self, dt):
        center_x = self.bomb.pos[0] + self.bomb.size[0] / 2
        center_y = self.bomb.pos[1] + self.bomb.size[1] / 2
        self.center_pos = self.game.get_position_by_xy(center_x, center_y)
        self.game.level[self.center_pos[1] - 1][self.center_pos[0] - 1] = 0
        self.tick_animation_interval.cancel()
        explode_directions = self.get_explode_directions()
        # left
        for i in range(1, explode_directions[0] + 1):
            fire_x = self.game.get_xy_by_position(self.center_pos[0] - i, self.center_pos[1])[0]
            fire_y = self.game.get_xy_by_position(self.center_pos[0] - i, self.center_pos[1])[1]
            if explode_directions[0] + 1 - i == 1:
                fire_type = 'end'
            else:
                fire_type = 'line'
            fire = Fire(self.game, fire_type, 'left', fire_x, fire_y, self)
            self.game.add_widget(fire)

        # right
        for i in range(1, explode_directions[1] + 1):
            fire_x = self.game.get_xy_by_position(self.center_pos[0] + i, self.center_pos[1])[0]
            fire_y = self.game.get_xy_by_position(self.center_pos[0] + i, self.center_pos[1])[1]
            if explode_directions[1] + 1 - i == 1:
                fire_type = 'end'
            else:
                fire_type = 'line'
            fire = Fire(self.game, fire_type, 'right', fire_x, fire_y, self)
            self.game.add_widget(fire)

        # up
        for i in range(1, explode_directions[2] + 1):
            fire_x = self.game.get_xy_by_position(self.center_pos[0], self.center_pos[1] + i)[0]
            fire_y = self.game.get_xy_by_position(self.center_pos[0], self.center_pos[1] + i)[1]
            if explode_directions[2] + 1 - i == 1:
                fire_type = 'end'
            else:
                fire_type = 'line'
            fire = Fire(self.game, fire_type, 'up', fire_x, fire_y, self)
            self.game.add_widget(fire)

        # down
        for i in range(1, explode_directions[3] + 1):
            fire_x = self.game.get_xy_by_position(self.center_pos[0], self.center_pos[1] - i)[0]
            fire_y = self.game.get_xy_by_position(self.center_pos[0], self.center_pos[1] - i)[1]
            if explode_directions[3] + 1 - i == 1:
                fire_type = 'end'
            else:
                fire_type = 'line'
            fire = Fire(self.game, fire_type, 'down', fire_x, fire_y, self)
            self.game.add_widget(fire)

        # center
        fire_x = self.game.get_xy_by_position(self.center_pos[0], self.center_pos[1])[0]
        fire_y = self.game.get_xy_by_position(self.center_pos[0], self.center_pos[1])[1]
        fire = Fire(self.game, 'center', 'center', fire_x, fire_y, self)
        self.game.add_widget(fire)

    def set_xy(self, x, y):
        self.bomb.pos = (x, y)

    def tick_animate(self, dt):
        if self.pic == "images/bomb/bomb1.png":
            self.canvas.clear()
            self.draw_bomb("images/bomb/bomb2.png")
        elif self.pic == "images/bomb/bomb2.png":
            self.canvas.clear()
            self.draw_bomb("images/bomb/bomb1.png")

    def get_explode_directions(self):
        left = 0
        x = self.center_pos[0] - 1
        while self.game.level[self.center_pos[1] - 1][x - 1] != 1:
            left += 1
            if self.game.level[self.center_pos[1] - 1][x - 1] in {3, 4}:
                break
            x -= 1
        if left > (self.power - 1):
            left = self.power - 1

        right = 0
        x = self.center_pos[0]
        while self.game.level[self.center_pos[1] - 1][x] != 1:
            right += 1
            if self.game.level[self.center_pos[1] - 1][x] in {4}:
                break
            x += 1
        if right > (self.power - 1):
            right = self.power - 1

        up = 0
        y = self.center_pos[1]
        while self.game.level[y][self.center_pos[0] - 1] != 1:
            up += 1
            if self.game.level[y][self.center_pos[0] - 1] in {4}:
                break
            y += 1
        if up > (self.power - 1):
            up = self.power - 1

        down = 0
        y = self.center_pos[1] - 1
        while self.game.level[y - 1][self.center_pos[0] - 1] != 1:
            down += 1
            if self.game.level[y - 1][self.center_pos[0] - 1] in {4}:
                break
            y -= 1
        if down > (self.power - 1):
            down = self.power - 1

        return left, right, up, down
