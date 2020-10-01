from kivy.uix.button import Button
from kivydnd.dragndropwidget import DragNDropWidget


class  DraggableButton(Button, DragNDropWidget):
    def __init__(self, **kw):
        super(DraggableButton, self).__init__(**kw)