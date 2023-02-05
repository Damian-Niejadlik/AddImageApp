import imghdr
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class AsyncImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = False
        self.background_color = [1, 1, 1, 1]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selected = not self.selected
            if self.selected:
                self.background_color = [0, 1, 0, 0.5]
            return True
        self.background_color = [1, 1, 1, 1]
        return super().on_touch_down(touch)


class PhotoViewer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.nav_bar = BoxLayout(size_hint=(1, 0.1), pos_hint={'top': 1})
        self.add_widget(self.nav_bar)
        self.nav_bar.add_widget(
            Button(text="Dodaj zdjęcie", on_press=self.open_file_chooser, size_hint=(None, 1), width=150,
                   pos_hint={'right': 1}))
        self.nav_bar.add_widget(
            Button(text="Usuń", on_press=self.remove_images, size_hint=(None, 1), width=150,
                   pos_hint={'right': 1}))

        self.scroll_view = ScrollView(size_hint=(1, 0.9), pos_hint={'top': 0.9})
        self.add_widget(self.scroll_view)
        self.images_container = GridLayout(cols=3, size_hint_y=None)
        self.images_container.bind(minimum_height=self.images_container.setter('height'))
        self.scroll_view.add_widget(self.images_container)

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserIconView(multiselect=True)
        exit_button = Button(text="X", size_hint=(0.1, 0.1), pos_hint={'top': 1, 'right': 1})
        exit_button.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(exit_button)
        content.add_widget(file_chooser)
        confirm_button = Button(text="Zatwierdź", size_hint=(1, 0.1), pos_hint={'bottom': 1})
        confirm_button.bind(on_press=lambda x: self.load_images(file_chooser.selection))
        content.add_widget(confirm_button)
        popup = Popup(title="Wybierz zdjęcia", content=content, size_hint=(0.9, 0.9))
        popup.open()

    def load_images(self, file_chooser):
        files = file_chooser
        for file in files:
            full_path = file
            if imghdr.what(full_path) is None:
                content = BoxLayout(orientation='vertical')
                content.add_widget(Label(text='Wybrany plik nie jest zdjęciem'))
                popup = Popup(title='Błąd', content=content, size_hint=(0.5, 0.5))
                popup.open()
                return
            image = AsyncImage(source=full_path, size_hint_y=None, height=self.scroll_view.height / 3)
            self.images_container.add_widget(image)

    def remove_images(self, instance):
        for child in self.images_container.children[:]:
            if child.selected:
                self.images_container.remove_widget(child)


class PhotoViewerApp(App):
    def build(self):
        return PhotoViewer()


if __name__ == "__main__":
    PhotoViewerApp().run()
