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
        for bomberman in self.game.bombermans:
            bx, by = bomberman.x, bomberman.y
            bw, bh = bomberman.get_size()
            if (bomberman.status == 'alive' and
                    in_contact(self.x, self.y, self.w, self.h, bx, by, bw, bh, self.sensitive) and
                    bomberman.has_key):
                self.check_contact_interval.cancel()
                for all_bombermans in self.game.bombermans:
                    all_bombermans.status = 'dead'
                with self.canvas:
                    w, h = self.game.width / 4, self.game.height / 3
                    if bomberman.player == 0:
                        source1 = 'images/win1.png'
                        source2 = 'images/win2.png'
                    else:
                        source1 = 'images/win2.png'
                        source2 = 'images/win3.png'
                    Rectangle(pos=(self.game.width / 2 - w, self.game.height / 2 - h / 2),
                              size=(w, h),
                              source=source1)
                    Rectangle(pos=(self.game.width / 2, self.game.height / 2 - h / 2),
                              size=(w, h),
                              source=source2)
                self.game.gameover_win_screen = True
