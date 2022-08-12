import os
from kivy import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
Config.set('graphics', 'multisamples', '0')
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

Builder.load_string('''
<DataTable>:
    id: main_win
    RecycleView:
        id: table_floor
        viewclass: "CustLabel"
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None, 250)
            default_size_hint: (1, None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5

<CustLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos
''')


class DataTable(BoxLayout):
    def __init__(self, table='', **kwargs):
        super().__init__(**kwargs)
        products = table

        col_titles = [k for k in products.keys()]
        rows_len = len(products[col_titles[0]])
        self.columns = len(col_titles)
        print(col_titles)
        print(len(col_titles))
        print(rows_len)
        table_data = []
        for t in col_titles:
            table_data.append({'text': str(t), 'size_hint_y': None,
                              'height': 50, 'bcolor': (.06, .45, .45, 1)})
        for r in range(rows_len):
            for t in col_titles:
                table_data.append({'text': str(
                    products[t][r]), "size_hint_y": None, "height": 30, "bcolor": (.06, .25, .25, 1)})

        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data
