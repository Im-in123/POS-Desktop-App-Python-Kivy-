import hashlib
from pymongo import MongoClient
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import os
from kivy import Config
Config.set('graphics', 'multisamples', '0')
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

Builder.load_file('signin/signin.kv')


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        db = client.travpos
        self.users = db.users

    def validate_user(self):

        username = self.ids.username_field.text
        pwd = self.ids.pwd_field.text
        info = self.ids.info

        if username == "" or pwd == "":
            info.text = "[color=#FF0000]Username and/ or password required![/color]"
            print("Username and/ or password required!")
        else:

            user = self.users.find_one({'user_name': username})
            if user == None:
                info.text = "[color=#FF0000]Invalid username or password![/color]"
            else:
                pwd = hashlib.sha256(pwd.encode()).hexdigest()

                if pwd == user['password']:
                    des = user['designation']
                    print("Logged in succesfully!", des)
                    # info.text = "[color=#00FF00]Logged in succesfully![/color]"
                    self.parent.parent.parent.ids.scrn_op.children[0].ids.loggedin_user.text = username
                    self.ids.username_field.text = ""
                    self.ids.pwd_field.text = ""
                    info.text = ""
                    if des == 'Administrator':
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        self.parent.parent.current = "scrn_op"

                else:
                    info.text = "[color=#FF0000]Invalid username or password![/color]"


class SigninApp(App):
    def build(self):
        return SigninWindow()


if __name__ == "__main__":
    Config.set('graphics', 'multisamples', '0')
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
    sa = SigninApp()
    sa.run()
