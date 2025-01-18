from kivy.app import App


from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

resource_add_path('D:\\New folder (2)\debug-font')
LabelBase.register(DEFAULT_FONT, 'DebugF.otf')

class PageoneApp(App) :
    pass

if __name__ =='__main__':
    PageoneApp().run()

