from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import os
from kivy import Config
Config.set('graphics', 'multisamples', '0')
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_user(self):
        username = self.ids.username_field.text
        pwd = self.ids.pwd_field.text
        info = self.ids.info
        if username == "" or pwd == "":
            info.text = "[color=#FF0000]Username and/ or password required![/color]"
            print("Username and/ or password required!")
        else:
            if username == "admin" and pwd == "admin":
                info.text = "[color=#00FF00]Logged in succesfully![/color]"

                print("Logged in succesfully!")
            else:
                info.text = "[color=#FF0000]Invalid username or password![/color]"


class SigninApp(App):
    def build(self):
        return SigninWindow()


if __name__ == "__main__":
    sa = SigninApp()
    sa.run()
