import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_asset(filename):
    return os.path.join(BASE_DIR, filename)
# For testing on desktop, simulate a mobile screen
Window.size = (360, 640)

class GlassTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0, 0, 0, 0)
        self.cursor_color = get_color_from_hex('#333333')
        # Цвет подсказки делаем тёмно-серым для лучшей читаемости
        self.hint_text_color = get_color_from_hex('#555555') 
        with self.canvas.before:
            # Делаем стекло менее прозрачным (0.8 вместо 0.4)
            Color(1, 1, 1, 0.8)
            self.rect = RoundedRectangle(radius=[10])
            # Делаем рамку более яркой
            Color(1, 1, 1, 0.9)
            self.line = Line(rounded_rectangle=[0, 0, 0, 0, 10], width=1.2)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.line.rounded_rectangle = [self.x, self.y, self.width, self.height, 10]

class GlassPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 30, 20, 30]
        self.spacing = 20
        self.size_hint = (0.85, None)
        self.height = 380
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        with self.canvas.before:
            Color(1, 1, 1, 0.25)
            self.rect = RoundedRectangle(radius=[20])
            Color(1, 1, 1, 0.5)
            self.line = Line(rounded_rectangle=[0, 0, 0, 0, 20], width=1.2)
            
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
        # Sign In Title
        title = Label(
            text="Sign In", 
            font_size='32sp', 
            bold=True, 
            color=get_color_from_hex('#8f2c24'), 
            size_hint_y=None, 
            height=50
        )
        self.add_widget(title)
        
        # Username Input
        self.username = GlassTextInput(
            hint_text="Username", 
            multiline=False, 
            size_hint_y=None, 
            height=50, 
            foreground_color=get_color_from_hex('#333333'),
            padding_y=[15, 15],
            font_size='16sp'
        )
        self.add_widget(self.username)
        
        # Password Input
        self.password = GlassTextInput(
            hint_text="Password", 
            password=True, 
            multiline=False, 
            size_hint_y=None, 
            height=50,
            foreground_color=get_color_from_hex('#333333'),
            padding_y=[15, 15],
            font_size='16sp'
        )
        self.add_widget(self.password)
        
        # Login Button
        self.btn = Button(
            text="Login", 
            size_hint_y=None, 
            height=50, 
            background_normal='', 
            background_color=get_color_from_hex('#8f2c24'), 
            color=(1, 1, 1, 1), 
            bold=True,
            font_size='18sp'
        )
        self.add_widget(self.btn)
        
        # Links
        links_layout = BoxLayout(size_hint_y=None, height=30)
        forget_link = Label(
            text="[ref=forget]Forget Password[/ref]", 
            markup=True, 
            color=get_color_from_hex('#8f2c24'),
            font_size='14sp'
        )
        signup_link = Label(
            text="[ref=signup][u]Signup[/u][/ref]", 
            markup=True, 
            color=get_color_from_hex('#8f2c24'),
            font_size='14sp'
        )
        links_layout.add_widget(forget_link)
        links_layout.add_widget(signup_link)
        self.add_widget(links_layout)

    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.line.rounded_rectangle = [self.x, self.y, self.width, self.height, 20]

class AnimatedGirl(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = get_asset('girl.png')
        self.size_hint = (None, None)
        self.size = (150, 150)
        self.allow_stretch = True
        self.pos = (Window.width, 100)
        Clock.schedule_once(self.start_anim, 1)

    def start_anim(self, dt):
        self.pos = (Window.width, 100)
        anim = Animation(x=-self.width, duration=8)
        anim.bind(on_complete=self.reset_anim)
        anim.start(self)
        
    def reset_anim(self, *args):
        self.pos = (Window.width, 100)
        self.start_anim(0)

class Leaf(Image):
    def __init__(self, leaf_src, start_x, duration, **kwargs):
        super().__init__(**kwargs)
        self.source = get_asset(leaf_src)
        self.size_hint = (None, None)
        self.size = (30, 30)
        self.allow_stretch = True
        self.start_x_val = start_x
        self.duration_val = duration
        self.reset_leaf()

    def reset_leaf(self, *args):
        self.y = Window.height + 50
        self.x = Window.width * self.start_x_val
        self.opacity = 0
        Clock.schedule_once(self.animate_leaf, random.uniform(0, 5))

    def animate_leaf(self, dt):
        self.opacity = 1
        anim = Animation(y=-50, x=self.x + random.choice([-80, 80]), duration=self.duration_val)
        anim.bind(on_complete=self.reset_leaf)
        anim.start(self)

class LoginApp(App):
    def build(self):
        root = FloatLayout()
        
        # 1. Background
        bg = Image(source=get_asset('bg.jpg'), allow_stretch=True, keep_ratio=False)
        root.add_widget(bg)
        
        # 2. Leaves layer
        leaf_configs = [
            ('leaf_01.png', 0.2, 10),
            ('leaf_02.png', 0.5, 7),
            ('leaf_03.png', 0.7, 6),
            ('leaf_04.png', 0.05, 7.5),
            ('leaf_01.png', 0.85, 9),
            ('leaf_02.png', 0.9, 6),
            ('leaf_03.png', 0.15, 7),
            ('leaf_04.png', 0.6, 7.5)
        ]
        
        for src, x, dur in leaf_configs:
            root.add_widget(Leaf(src, x, dur))
            
        # 3. Animated Girl
        girl = AnimatedGirl()
        root.add_widget(girl)
        
        # 4. Trees
        trees = Image(source=get_asset('trees.png'), allow_stretch=True, keep_ratio=False)
        root.add_widget(trees)
        
        # 5. Login Panel
        panel = GlassPanel()
        root.add_widget(panel)
        
        return root

if __name__ == '__main__':
    LoginApp().run()