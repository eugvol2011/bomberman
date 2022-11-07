from levels import field

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle


class Field(Widget):

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        field.reverse()
        self.draw_field()

    def draw_field(self):
        with self.canvas:
            x = 0
            y = 0
            for row in range(0, len(field)):
                for col in range(0, len(field[row])):
                    if field[row][col] == 1:
                        Rectangle(pos=(x, y),
                                  size=(self.game.cell_width, self.game.cell_height),
                                  source="images/solid_wall.png")
                    elif field[row][col] in (0, 2, 3, 4, 5):
                        Rectangle(pos=(x, y),
                                  size=(self.game.cell_width, self.game.cell_height),
                                  source="images/no_wall.png")
                    x = x + self.game.cell_width
                y = y + self.game.cell_height
                x = 0
