from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from collections import OrderedDict

from utils.datatable import DataTable
import mysql.connector
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from datetime import datetime
import hashlib


class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mydb = mysql.connector.connect(
            host='localhost', user='root', passwd='Mysqlpassword2022',
            database='pos'
        )
        self.mycursor = self.mydb.cursor()

        content = self.ids.scrn_contents
        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

        product_scrn = self.ids.scrn_product_content
        products = self.get_products()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)

    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name')
        crud_last = TextInput(hint_text='Last Name')
        crud_user = TextInput(hint_text='User Name')
        crud_pwd = TextInput(hint_text='Password')
        crud_des = Spinner(text="Operator", values=[
                           "Operator", "Administrator"])
        crud_submit = Button(text="Add", size_hint_x=None, width=100, on_release=lambda x: self.add_user(
            crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def update_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name')
        crud_last = TextInput(hint_text='Last Name')
        crud_user = TextInput(hint_text='User Name')
        crud_pwd = TextInput(hint_text='Password')
        crud_des = Spinner(text="Operator", values=[
                           "Operator", "Administrator"])
        crud_submit = Button(text="Update", size_hint_x=None, width=100, on_release=lambda x: self.update_user(
            crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text='User Name')
        crud_submit = Button(text="Remove", size_hint_x=None, width=100, on_release=lambda x: self.remove_user(
            crud_user.text))
        target.add_widget(crud_user)
        target.add_widget(crud_submit)

    def update_user(self, first, last, user, pwd, des):

        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()

        sql = "UPDATE users SET first_name=%s, last_name=%s, user_name=%s, password=%s, designation=%s WHERE user_name=%s"
        values = [first, last, user, pwd, des,  user]

        self.mycursor.execute(sql, values)
        self.mydb.commit()

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def add_user(self, first, last, user, pwd, des):

        content = self.ids.scrn_contents
        content.clear_widgets()
        sql = "INSERT INTO users(first_name, last_name, user_name, password, designation, date) VALUES(%s, %s,%s, %s,%s, %s)"
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        values = [first, last, user, pwd, des, datetime.now()]

        self.mycursor.execute(sql, values)
        self.mydb.commit()

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def remove_user(self, user):
        content = self.ids.scrn_contents
        content.clear_widgets()

        sql = "DELETE FROM users WHERE user_name = %s"
        values = [user]
        self.mycursor.execute(sql, values)
        self.mydb.commit()

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def get_users(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Mysqlpassword2022",
            database="pos"
        )
        mycursor = mydb.cursor()

        _users = OrderedDict()
        _users['first_names'] = {}
        _users['last_names'] = {}
        _users['user_names'] = {}
        _users['passwords'] = {}
        _users['designations'] = {}

        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []

        sql = "Select * FROM users"
        mycursor.execute(sql)
        users = mycursor.fetchall()
        for user in users:
            first_names.append(user[1])
            last_names.append(user[2])
            user_names.append(user[3])
            pwd = user[4]
            if len(pwd) > 10:
                pwd = pwd[:10] + '...'
            passwords.append(pwd)
            designations.append(user[5])
        users_length = len(first_names)
        idx = 0
        while idx < users_length:
            _users['first_names'][idx] = first_names[idx]
            _users['last_names'][idx] = last_names[idx]
            _users['user_names'][idx] = user_names[idx]
            _users['passwords'][idx] = passwords[idx]
            _users['designations'][idx] = designations[idx]
            idx += 1
        return _users

    def get_products(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Mysqlpassword2022",
            database="pos"
        )
        mycursor = mydb.cursor()

        _stocks = OrderedDict()
        _stocks['product_code'] = {}
        _stocks['product_name'] = {}
        _stocks['product_weight'] = {}
        _stocks['in_stock'] = {}
        _stocks['sold'] = {}
        _stocks['order'] = {}
        _stocks['last_purchase'] = {}

        product_code = []
        product_name = []
        product_weight = []
        in_stock = []
        sold = []
        order = []
        last_purchase = []
        sql = "Select * FROM stocks"
        mycursor.execute(sql)
        products = mycursor.fetchall()
        for product in products:
            product_code.append(product[1])
            name = product[2]
            if len(name) > 10:
                name = name[:10] + '...'
            product_name.append(name)

            product_weight.append(product[3])
            in_stock.append(product[5])
            sold.append(product[6])
            order.append(product[7])
            last_purchase.append(product[8])
        products_length = len(product_code)
        idx = 0
        while idx < products_length:
            _stocks['product_code'][idx] = product_code[idx]
            _stocks['product_name'][idx] = product_name[idx]
            _stocks['product_weight'][idx] = product_weight[idx]
            _stocks['in_stock'][idx] = in_stock[idx]
            _stocks['sold'][idx] = sold[idx]
            _stocks['order'][idx] = order[idx]
            _stocks['last_purchase'][idx] = last_purchase[idx]
            idx += 1
        return _stocks

    def change_screen(self, instance):

        if instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = "scrn_product_content"
        elif instance.text == 'Manage Users':
            self.ids.scrn_mngr.current = "scrn_content"
        else:
            self.ids.scrn_mngr.current = "scrn_analysis"


class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__ == "__main__":
    from kivy import Config
    import os
    Config.set('graphics', 'multisamples', '0')
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

    aa = AdminApp()
    aa.run()
