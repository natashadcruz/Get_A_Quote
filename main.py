from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def change_pwd(self):
        self.manager.current = "change_password"
        
    def login(self, uname, pwd):
        with open("user.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pwd:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password!"
        

class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    def addUser(self, uname, pwd):
        with open("user.json") as file:
            users = json.load(file);
        
        users[uname] = {"username": uname, "password":pwd,
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        with open("user.json", "w") as file:
            json.dump(users, file)        
        self.manager.current = "sign_up_screen_success"
        
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        
        
class SignUpScreenSuccess(Screen):
    def redirect_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"   

class ChangePassword(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
		
    def change_pwd(self, uname, pwd):
        with open("user.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['username'] == uname:
            users[uname]['password'] = pwd
            # update json file
            with open("user.json", "w") as file:
                json.dump(users, file)            
            self.manager.current = "change_password_success"
        else:
            self.ids.message.text = "Wrong username provided!"

class ChangePasswordSuccess(Screen):
    def redirect_login(self):
        self.manager.current = "login_screen"

        
class LoginScreenSuccess(Screen):
    def logout(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    
    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")
        
        available_feelings = [Path(filename).stem for filename in 
                               available_feelings]
        
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
                self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass
    

class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()