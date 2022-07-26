import kivy
from kivy.uix.image import Image

kivy.require('1.11.1')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy_garden.graph import Graph, LinePlot
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from database import DataBase
import numpy as np
import matplotlib.pyplot as plt
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import pandas as pd



class MatplotExample(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = self.ids.box
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def save_it(self):
        pass



class CreateAccountWindow(Screen):

    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)
                self.reset()
                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""



class LoginWindow(Screen):

    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""



class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    sample = 512
    lineColor = ListProperty([1,0,0,1])
    blackColor = ListProperty([0, 0, 0, 1])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sample = 512
        self.x_plot = np.linspace(0, 1, self.sample)
        self.y_plot = np.sin(2*np.pi*2*self.x_plot)

        #On cree lobjet de ligne et on associe X et Y
        self.plot = LinePlot(color=self.lineColor, line_width=1.5)
        self.plot.points = [(i, self.y_plot[i]) for i in range(self.sample)]

        #on insere notre Line plot dans le Graph du fichier kv don l'id est graph
        self.ids.graph.add_plot(self.plot)
        """box = self.ids.graph1
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))"""

    def add_plot(self):
        """box = self.ids.graph1"""
        #roott = self.ids.graph1
        #box = BoxLayout()
        #roott.add_widget(box)
        #box.add_widget(FigureCanvasKivyAgg(plt.gcf())
        #box.add_widget())
        pass

    def remove_plot(self):
        root = self.ids.graph1
        for child in root.children:
            print(child)
        #box = self.ids.graph1
        root.clear_widgets()

    def update_plot(self, freq):
        self.y_plot = np.sin(2 * np.pi * freq * self.x_plot)
        self.plot.points = [(i, self.y_plot[i]) for i in range(self.sample)]

    def change_color(self, wid):
        if wid.value < 25 :
            self.lineColor = [1,0,1,1]
        elif wid.value >= 25 and wid.value < 50 :
            self.lineColor = [.5, .1, .7, 1]
        elif wid.value >= 50 and wid.value < 75 :
            self.lineColor = [.3, .5, .1, 1]
        else :
            self.lineColor = [.5, 1, .7, 1]




    def logOut(self):
        sm.current = "login"

    """def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created"""



class ChartWindow(Screen):
    count = 1
    count_enabled = BooleanProperty(False)
    my_text = StringProperty("1")
    my_slider_content = StringProperty("5")
    switch_value = BooleanProperty(False)
    text_val_str = StringProperty("Hermann")

    def on_button_click(self):
        if self.count_enabled:
            self.count += 1
            self.my_text = str(self.count)

    def click_myself(selfself):
        print('on vient de cliquer sur le boutton')

    def on_toggle_state(self, widget):
        print('toggle state : '+widget.state)
        if widget.state == 'normal' :
            widget.text = 'OFF'
            self.count_enabled = False

        elif widget.state == 'down':
            widget.text = 'ON'
            self.count_enabled = True

    def on_switch_state(self, widget):
        print("switch active ? "+ str(widget.active))

    def on_slider_value(self, widget):
        print('slider value: '+str(int(widget.value)))
        self.my_slider_content = str(int(widget.value))
        if widget.value > 5 and widget.value != 10 :
            self.switch_value = True
        elif widget.value <= 5 :
            self.switch_value = False
        elif widget.value == 10:
            sm.current = 'login'

    def on_text_validate(self, widget):
        self.text_val_str = widget.text



class ImageExample(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        stack = self.ids.stack1
        im1 = Image(source="Z_Autres/50.png")
        stack.add_widget(im1)

        for child in stack.children:
            print(child)




class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()



kv = Builder.load_file("Textilus.kv")
sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"),
           CreateAccountWindow(name="create"),
           MainWindow(name="main"),
           ChartWindow(name="chart"),
           ImageExample(name="image"),
           MatplotExample(name="mat"),

           ]
for screen in screens:
    sm.add_widget(screen)

#sm.current = "login"
#sm.current = "chart"
sm.current = "image"



class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()




# database.py



