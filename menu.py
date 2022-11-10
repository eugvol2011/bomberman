from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from game import Game


class MenuItem(BoxLayout):
    def __init__(self, text: str, value: str, min_value: int, max_value: int, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.text = text
        self.value = value
        self.text_label = Label(text=f'{self.text} {self.value}')
        self.min_value = min_value
        self.max_value = max_value
        self.add_widget(self.text_label)

    def increase(self):
        if self.text != 'НАЧАТЬ ИГРУ':
            self.value = str(int(self.value) + 1)
            if int(self.value) > self.max_value:
                self.value = str(self.min_value)
            self.text_label.text = f'{self.text} {self.value}'

    def decrease(self):
        if self.text != 'НАЧАТЬ ИГРУ':
            self.value = str(int(self.value) - 1)
            if int(self.value) < self.min_value:
                self.value = str(self.max_value)
            self.text_label.text = f'{self.text} {self.value}'

    def activate(self):
        self.text_label.bold = True
        self.text_label.outline_width = 2
        self.text_label.outline_color = (1, 0, 0, 1)

    def deactivate(self):
        self.text_label.bold = False
        self.text_label.outline_width = 0


class Menu(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        main_menu = Screen(name='main menu')
        bl = BoxLayout(orientation='vertical')
        logo = Image(source='images/logo.png')
        bl.add_widget(logo)

        bomber_pic1 = Image(source='images/win1.png')
        bomber_pic2 = Image(source='images/win3.png')

        self.menu_items = []
        self.players = MenuItem('Количество игроков:', value='1', min_value=1, max_value=2)
        self.menu_items.append(self.players)
        self.max_bombs = MenuItem('Количество бомб:', value='2', min_value=1, max_value=25)
        self.menu_items.append(self.max_bombs)
        self.power = MenuItem('Мощность бомбы:', value='2', min_value=2, max_value=23)
        self.menu_items.append(self.power)
        self.delay = MenuItem('Задержка бомбы, сек:', value='2', min_value=2, max_value=10)
        self.menu_items.append(self.delay)
        self.monsters = MenuItem('Количество монстров:', value='5', min_value=1, max_value=150)
        self.menu_items.append(self.monsters)
        self.monster_speed = MenuItem('Скорость монстров:', value='20', min_value=5, max_value=80)
        self.menu_items.append(self.monster_speed)
        self.lives = MenuItem('Количество жизней:', value='3', min_value=1, max_value=100)
        self.menu_items.append(self.lives)
        self.bomberman_speed = MenuItem('Скорость бомбермэна:', value='300', min_value=100, max_value=800)
        self.menu_items.append(self.bomberman_speed)
        self.woodenboxes = MenuItem('Количество ящиков:', value='10', min_value=10, max_value=150)
        self.menu_items.append(self.woodenboxes)
        self.start = MenuItem('НАЧАТЬ ИГРУ', value='', min_value=0, max_value=0)
        self.menu_items.append(self.start)
        self.start.activate()

        bl_options_list = BoxLayout(orientation='vertical', size_hint=(1, .5))
        for menu_item in self.menu_items:
            bl_options_list.add_widget(menu_item)

        self.active_menu_item = len(self.menu_items) - 1

        bl_middle = BoxLayout(orientation='horizontal')
        bl_middle.add_widget(bomber_pic1)
        al = AnchorLayout(anchor_x='center', anchor_y='top')
        al.add_widget(bl_options_list)
        bl_middle.add_widget(al)
        bl_middle.add_widget(bomber_pic2)
        bl.add_widget(bl_middle)

        main_menu.add_widget(bl)
        self.add_widget(main_menu)
        self.current = 'main menu'

    def keyboard_init(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'down':
            self.menu_items[self.active_menu_item].deactivate()
            self.active_menu_item += 1
            if self.active_menu_item > (len(self.menu_items) - 1):
                self.active_menu_item = 0
            self.menu_items[self.active_menu_item].activate()

        if keycode[1] == 'up':
            self.menu_items[self.active_menu_item].deactivate()
            self.active_menu_item -= 1
            if self.active_menu_item < 0:
                self.active_menu_item = len(self.menu_items) - 1
            self.menu_items[self.active_menu_item].activate()

        if keycode[1] == 'right':
            self.menu_items[self.active_menu_item].increase()

        if keycode[1] == 'left':
            self.menu_items[self.active_menu_item].decrease()

        if keycode[1] == 'enter' and self.active_menu_item == len(self.menu_items) - 1:
            game_screen = Screen(name='game')
            game = Game(self, int(self.players.value), int(self.max_bombs.value), int(self.power.value),
                        int(self.delay.value), int(self.monsters.value), int(self.monster_speed.value),
                        int(self.lives.value), int(self.bomberman_speed.value), int(self.woodenboxes.value))
            game_screen.add_widget(game)
            self.add_widget(game_screen)
            self.current = 'game'

