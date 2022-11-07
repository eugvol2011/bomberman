from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from functions import in_contact


class Door(Widget):

    def __init__(self, game, x, y, **kwargs):
        super().__init__(**kwargs)
        self.door = None
        self.game = game
        self.x, self.y = x, y
        self.w, self.h = self.game.cell_width, self.game.cell_height
        self.source = "images/door.png"
        self.check_contact_interval = Clock.schedule_interval(self.contact, .1)
        self.sensitive = 15
        self.draw_door()

    def draw_door(self):
        with self.canvas:
            self.door = Rectangle(pos=(self.x, self.y),
                                  size=(self.game.cell_width,
                                        self.game.cell_height),
                                  source=self.source)

    def contact(self, dt):
        bx, by = self.game.bomberman.x, self.game.bomberman.y
        bw, bh = self.game.bomberman.get_size()
        if (self.game.bomberman.status == 'alive' and
                in_contact(self.x, self.y, self.w, self.h, bx, by, bw, bh, self.sensitive) and
                self.game.bomberman.has_key):
            self.check_contact_interval.cancel()
            self.game.bomberman.status = 'dead'
            with self.canvas:
                w, h = self.game.width / 4, self.game.height / 3
                Rectangle(pos=(self.game.width / 2 - w, self.game.height / 2 - h / 2),
                          size=(w, h),
                          source='images/win1.png')
                Rectangle(pos=(self.game.width / 2, self.game.height / 2 - h / 2),
                          size=(w, h),
                          source='images/win2.png')
