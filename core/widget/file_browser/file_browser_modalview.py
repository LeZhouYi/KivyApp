from kivy.uix.modalview import ModalView


class FileBrowserModalView(ModalView):

    def __init__(self):
        super().__init__()
        self.size_hint = [0.8, 0.8]
