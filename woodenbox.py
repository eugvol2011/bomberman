from kivy.clock import Clock

from functions import in_contact

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle


class Secret(Widget):

    def __init__(self, game, x, y, secret_type, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.secret = None
        self.size_ratio = 1
        self.x, self.y = x, y
        self.w, self.h = self.game.cell_width, self.game.cell_height
        self.source = None
        self.secret_type = secret_type
        self.sensitive = 15
        self.first_contact = False
        self.game.list_of_secrets.add(self)
        self.check_contact_interval = Clock.schedule_interval(self.contact, .1)
        self.draw_secret(self.secret_type)

    def draw_secret(self, secret_type):
        match secret_type:
            case 'key':
                self.source = 'images/key.png'
            case 'heart':
                self.source = 'images/heart.png'
            case 'bomb':
                self.source = 'images/golden_bomb.png'
            case 'power':
                self.source = 'images/power.png'
        with self.canvas:
            self.secret = Rectangle(pos=(self.x, self.y),
                                    size=(self.game.cell_width,
                                          self.game.cell_height),
                                    source=self.source)

    def contact(self, dt):
        bx, by = self.game.bomberman.x, self.game.bomberman.y
        bw, bh = self.game.bomberman.get_size()
        if (self.first_contact and
                not in_contact(self.x, self.y, self.w, self.h, bx, by, bw, bh, self.sensitive)):
            self.first_contact = False
        if (self.game.bomberman.status == 'alive' and
                not self.first_contact and
                in_contact(self.x, self.y, self.w, self.h, bx, by, bw, bh, self.sensitive)):
            self.first_contact = True
            self.canvas.clear()
            self.game.remove_widget(self)
            self.game.list_of_secrets.discard(self)
            if self.secret_type == 'key':
                self.game.bomberman.has_key = True
            elif self.secret_type == 'heart':
                self.game.bomberman.lives += 1
            elif self.secret_type == 'bomb':
                self.game.bomberman.max_bombs += 1
            elif self.secret_type == 'power':
                self.game.bomberman.power += 1
            self.check_contact_interval.cancel()
            del self

    def die(self):
        if self.secret_type != 'key':
            self.canvas.clear()
            self.game.remove_widget(self)
            self.game.list_of_secrets.discard(self)
            self.check_contact_interval.cancel()
            del self


class Woodenbox(Widget):

    def __init__(self, game, x, y, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.woodenbox = None
        self.size_ratio = 1
        self.x, self.y = x, y
        self.w, self.h = self.game.cell_width, self.game.cell_height
        self.source = "images/wooden-box.png"
        self.xy_pos = self.game.get_position_by_xy(self.x + 1, self.y + 1)[0:2]
        self.secret = None
        self.draw_woodenbox()

    def draw_woodenbox(self):
        with self.canvas:
            self.woodenbox = Rectangle(pos=(self.x, self.y),
                                       size=(self.game.cell_width,
                                             self.game.cell_height),
                                       source=self.source)

    def get_size(self):
        return self.woodenbox.size
