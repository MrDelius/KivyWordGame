import random
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
import json

kv = Builder.load_file("design.kv")

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def linux():
    with open('Linux.json') as json_file:
        data = json.load(json_file)

    with open("Level.txt", "r") as level_file:
        level = level_file.read()

    buts = data[level][0]
    mean = data[level][1]
    return buts, mean, int(level)


# popup class for winning
class WinPopup(Popup):

    def close_pop(self):
        self.dismiss()

    def new_win(self):
        return linux()

    def leveling(self):
        with open("Level.txt", "r") as lev:
            level = lev.read()
        self.title = "Level: " + str(int(level)+1)
        self.open()


# popup class for loosing
class LoosePopup(Popup):
    def close_pop(self):
        self.dismiss()


# class for designing down buttons
class DownButtons(Button):
    pass


# class for designing up buttons
class UpButtons(Button):
    pass


# class for Label with question
class MeanLabel(ScrollView):
    text = StringProperty('')


# the program logics
class MainWindow(Screen):
    number = NumericProperty(0)
    downButs = ObjectProperty(None)
    upButs = ObjectProperty(None)
    firstLayout = ObjectProperty(None)
    meanLayout = ObjectProperty(None)
    topBar = ObjectProperty(None)

    theList = {
        0: 'Welcome_to_the_History_of_Linux',
        1: 'What_Inspired_Creating_Linux',
        2: 'The_Story_Behind_the_Name_Linux',
        3: 'Torvalds’_Linux_Development',
        4: 'Role_of_GNU_GPL_in_Linux',
        5: 'Linux_Mascot',
        6: 'Linux_Distributions',
        7: '10_Facts_about_Linux',
        8: 'List_of_Linux_Distributions',
        9: 'The_Conclusion',
    }

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.data = linux()
        self.meaning = self.data[1]
        self.word = self.data[0]
        self.level = self.data[2]
        self.check = ""

        self.lab = MeanLabel(text=self.meaning)
        self.ids["task"] = self.lab
        self.meanLayout.add_widget(self.lab)

        self.ran_word = list(self.word) + [random.choice(alphabet) for _ in range(16 - len(self.word))]
        random.shuffle(self.ran_word)
        for el in self.ran_word:
            self.but = DownButtons(text=el)
            self.but.bind(on_release=self.release)
            self.ids[self.number] = self.but
            self.downButs.add_widget(self.but)
            self.number += 1
        self.number = 16

        for i in self.word:
            self.ubut = UpButtons(text="")
            self.ubut.bind(on_release=self.release)
            self.ids[self.number] = self.ubut
            self.upButs.add_widget(self.ubut)
            self.number += 1

        self.upButs.cols = 8

        if self.number - 16 > 8:
            self.upButs.rows = 2
        else:
            self.upButs.rows = 1

        self.new = 16

    def release(self, instance):
        self.check += instance.text
        self.ids[self.new].text = instance.text
        self.new += 1
        if len(self.check) == len(self.word):
            if self.word == self.check:
                self.level += 1
                self.check = ""
                pop = WinPopup()
                if self.level == 89:
                    with open("Level.txt", "w") as newLev:
                        newLev.write("0")
                        self.level = 0
                else:
                    with open("Level.txt", "w") as newLev:
                        newLev.write(str(self.level))

                if self.level % 10 == 0:
                    kl = self.level // 10
                    stp = StoryPopup()
                    stp.info(str(kl-1))

                pop.leveling()

                self.data = pop.new_win()
                self.meaning = self.data[1]
                self.word = self.data[0]

                self.ran_word = list(self.word) + [random.choice(alphabet) for _ in range(16 - len(self.word))]
                random.shuffle(self.ran_word)

                self.ids["task"].text = self.meaning
                for el in enumerate(self.ran_word):
                    self.ids[el[0]].text = el[1]

                self.upButs.clear_widgets()
                self.new = 16
                self.upButs.cols = 20
                for i in self.word:
                    self.ubut = UpButtons(text="")
                    self.ubut.bind(on_release=self.release)
                    self.ids[self.new] = self.ubut
                    self.upButs.add_widget(self.ubut)
                    self.new += 1

                self.upButs.cols = 8

                if self.new - 16 > 8:
                    self.upButs.rows = 2
                    self.upButs.height = self.downButs.height / 1.45
                else:
                    self.upButs.rows = 1
                    self.upButs.height = self.downButs.height / 2
                self.new = 16
            else:
                self.new = 16
                self.check = ""
                print("failed")
                pop = LoosePopup()
                pop.open()
                for el in range(16, 16 + len(self.word)):
                    self.ids[el].text = ""


class StoryButtons(Button):
    pass


# popup widget with information about Linux
class StoryPopup(Popup):
    message = ObjectProperty(None)
    pop_story = ObjectProperty(None)

    def info(self, data):
        with open(f"history.json", "r") as f:
            dd = json.load(f)
        self.title = dd[data][0]
        self.message.text = dd[data][1]
        self.open()


class Topics(Button):
    pass


# Second screen showing all the topics of Linux OS
class Story(Screen):
    theList = {
        'Welcome to the History of Linux': 0,
        'What Inspired Creating Linux': 1,
        'The Story Behind the Name Linux': 2,
        'Torvalds’ Linux Development': 3,
        'Role of GNU GPL in Linux': 4,
        'Linux Mascot': 5,
        'Linux Distributions': 6,
        '10 Facts about Linux': 7,
        'List of Linux Distributions': 8,
        'The Conclusion': 9,
    }
    topBar = ObjectProperty(None)
    boxList = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Story, self).__init__(**kwargs)

    def thereader(self):
        with open("Level.txt", "r") as f:
            d = f.read()
        data = int(d) // 10
        self.boxList.clear_widgets()

        container = BoxLayout(orientation='vertical', size_hint_y=None)
        container.bind(minimum_height=container.setter('height'))

        with open(f"history.json", "r") as f:
            dd = json.load(f)

        for el in range(data + 1):
            bt = Topics(text=dd[str(el)][0])
            self.ids[el] = bt
            bt.bind(on_release=self.release)
            container.add_widget(bt)

        self.boxList.add_widget(container)

    def release(self, instance):
        popper = StoryPopup()
        popper.info(str(self.theList[instance.text]))


class MyGame(App):
    st = Story(name='story')
    mw = MainWindow(name='main')

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(self.mw)
        self.sm.add_widget(self.st)

        return self.sm


if __name__ == '__main__':
    app = MyGame()
    app.run()
