from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.carousel import Carousel
from kivy.uix.scrollview import ScrollView  # Add this line
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Set the window size to a typical mobile screen size
Window.size = (360, 640)

# Define a custom image button
class ImageButton(ButtonBehavior, Image):
    pass

# Define a base screen class to handle the background image
class BaseScreen(Screen):
    def __init__(self, background_source, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.background = Image(source=background_source, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background)

        self.content_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 400))
        self.content_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.layout.add_widget(self.content_layout)

        self.add_widget(self.layout)

    def add_home_button(self):
        home_button = ImageButton(source='imagens/left_arrow.png', on_press=self.go_to_home_screen)
        home_button.size_hint = (None, None)
        home_button.size = (50, 50)
        home_button.pos_hint = {'right': 1, 'bottom': 1}
        self.layout.add_widget(home_button)

    def go_to_home_screen(self, instance):
        self.manager.current = 'home_screen'

    def add_return_button(self):
        return_button = ImageButton(source='imagens/left_arrow.png', on_press=self.go_to_starting_screen)
        return_button.size_hint = (None, None)
        return_button.size = (50, 50)
        return_button.pos_hint = {'x': 0, 'y': 0}
        self.layout.add_widget(return_button)

    def add_buttons_with_spacing(self, button_texts):
        scroll_view = ScrollView(size_hint=(1, 1))
        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for text, screen_name in button_texts:
            btn = Button(text=text, size_hint_y=None, height=40)
            if screen_name == 'show_image':
                btn.bind(on_press=lambda instance: self.show_image_popup('imagens/identificacao_nome.jpg', 'Informação da Imagem'))
            else:
                btn.bind(on_press=lambda instance, sn=screen_name: setattr(self.manager, 'current', sn))
            grid_layout.add_widget(btn)

        scroll_view.add_widget(grid_layout)
        self.content_layout.add_widget(scroll_view)

    def show_image_popup(self, image_source, text_info):
        content = BoxLayout(orientation='vertical', padding=10)
        
        # Add image
        img = Image(source=image_source)
        content.add_widget(img)
        
        # Add text info
        info_label = Label(
            text=text_info,
            size_hint=(1, None),
            height=40,
            halign='center',
            valign='middle',
            color=get_color_from_hex('#000000')
        )
        info_label.bind(
            size=lambda s, w: setattr(s, 'text_size', (s.width, None))  # Update text size for wrapping
        )
        content.add_widget(info_label)

        # Add close button
        close_button = Button(text='FECHAR', size_hint_y=None, height=40)
        close_button.bind(on_press=lambda instance: popup.dismiss())
        content.add_widget(close_button)

        popup = Popup(title='QUAL É O SEU NOME?', content=content, size_hint=(1, 1))
        popup.open()

# Define your screens
class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__('imagens/home_screen_background.png', **kwargs)
        
        title = Label(text='Acesso', font_size=32, size_hint_y=None, height=50)
        self.content_layout.add_widget(title)

        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 150))
        button_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        start_button = Button(text='INICIAR', size_hint_y=None, height=50)
        start_button.bind(on_press=self.go_to_starting_screen)
        button_layout.add_widget(start_button)

        about_button = Button(text='SOBRE O APP', size_hint_y=None, height=50)
        about_button.bind(on_press=self.go_to_about_screen)
        button_layout.add_widget(about_button)

        self.layout.add_widget(button_layout)

    def go_to_starting_screen(self, instance):
        self.manager.current = 'starting_screen'

    def go_to_about_screen(self, instance):
        self.manager.current = 'about_screen'

class StartingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(StartingScreen, self).__init__('imagens/background.png', **kwargs)
        
        title = Label(
            text='Selecione a etapa da entrevista',
            font_size=18,
            size_hint_y=None,
            height=40,
            color=get_color_from_hex('#4E5D5A')
        )
        title.pos_hint = {'center_x': 0.5, 'top': 1}
        self.content_layout.add_widget(title)

        button_texts = [
            ('IDENTIFICAÇÃO', 'identificacao'),
            ('QUEIXA PRINCIPAL', 'queixaprincipal'),
            ('HMA', 'hma'),
            ('HISTÓRIA PREGRESSA', 'historiapregressa'),
            ('HÁBITOS DE VIDA', 'habitosdevida'),
            ('USO DE SUBSTÂNCIAS', 'usodesubstancias'),
            ('HISTÓRIA FISIOLÓGICA', 'historiafisiologica'),
            ('HISTÓRIA FAMILIAL', 'historiafamilial'),
            ('HISTÓRIA FAMILIAR', 'historiafamiliar'),
            ('HISTÓRIA PSICOSSOCIAL', 'historiapsicossocial'),
            ('REVISÃO DE SISTEMAS', 'revisaodesistemas'),
            ('MOSTRAR IMAGEM', 'show_image')
        ]

        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        
        for text, screen_name in button_texts:
            btn = Button(text=text, size_hint_y=None, height=30)
            if screen_name == 'show_image':
                btn.bind(on_press=lambda instance: self.show_image_popup('imagens/identificacao_nome.jpg', ""))
            else:
                btn.bind(on_press=lambda instance, sn=screen_name: setattr(self.manager, 'current', sn))
            grid_layout.add_widget(btn)

        scroll_layout = BoxLayout(size_hint=(None, None), size=(300, 500))
        scroll_layout.add_widget(grid_layout)
        
        main_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 400))
        main_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        main_layout.add_widget(scroll_layout)
        
        self.content_layout.add_widget(main_layout)
        self.add_home_button()

class IdentificacaoScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(IdentificacaoScreen, self).__init__('imagens/background.png', **kwargs)
        
        title = Label(
            text='Identificação',
            font_size=18,
            size_hint_y=None,
            height=40,
            color=get_color_from_hex('#4E5D5A')
        )
        title.pos_hint = {'center_x': 0.5, 'top': 1}
        self.content_layout.add_widget(title)

        button_texts = [
            ('NOME', 'show_image'),  # Replace 'show_image' with appropriate screen or action
            ('IDADE', 'show_image'),  # Replace 'show_image' with appropriate screen or action
            ('NATURALIDADE', 'show_image'),  # Replace 'show_image' with appropriate screen or action
            ('ESTADO CIVIL', 'show_image'),  # Replace 'show_image' with appropriate screen or action
            ('PROFISSÃO', 'show_image')  # Replace 'show_image' with appropriate screen or action
        ]

        self.add_buttons_with_spacing(button_texts)
        self.add_home_button()


class AboutScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__('imagens/background.png', **kwargs)

        about_text = "Este é um aplicativo desenvolvido para um projeto de iniciação científica do curso de Medicina do Centro Universitário de Patos de Minas - UNIPAM. Seu objetivo é auxiliar as consultas médicas de pacientes com deficiência. Ele foi pensado e elaborado pela estudante Giovana Garbim Veronese, sua orientadora Laís Moreira Borges e seu coorientador Bruno de Paulo Almeida."

        about_label = Label(
            text=about_text,
            font_size=16,
            size_hint=(None, None),
            height=300,
            width=280,
            text_size=(280, None),  # Wrap text within a certain width
            halign='center',
            valign='middle',
            color=get_color_from_hex('#4E5D5A')  # Set the text color
        )
        about_label.bind(
            size=lambda s, w: setattr(s, 'text_size', (s.width, None))  # Update text size for wrapping
        )
        
        # Center the label
        self.content_layout.add_widget(about_label)

        # Add home button
        self.add_home_button()

# Define other screens
class IdentificacaoScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(IdentificacaoScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Identificação Screen'))
        self.add_home_button()

class QueixaPrincipalScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(QueixaPrincipalScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Queixa Principal Screen'))
        self.add_home_button()

class HmaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HmaScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='HMA Screen'))
        self.add_home_button()

class HistoriaPregressaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaPregressaScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Pregressa Screen'))
        self.add_home_button()

class HabitosDeVidaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HabitosDeVidaScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Hábitos de Vida Screen'))
        self.add_home_button()

class UsoDeSubstanciasScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(UsoDeSubstanciasScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Uso de Substâncias Screen'))
        self.add_home_button()

class HistoriaFisiologicaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFisiologicaScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Fisiológica Screen'))
        self.add_home_button()

class HistoriaFamilialScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFamilialScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Familial Screen'))
        self.add_home_button()

class HistoriaFamiliarScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFamiliarScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Familiar Screen'))
        self.add_home_button()

class HistoriaPsicossocialScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaPsicossocialScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Psicossocial Screen'))
        self.add_home_button()

class RevisaoDeSistemasScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(RevisaoDeSistemasScreen, self).__init__('imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Revisão de Sistemas Screen'))
        self.add_home_button()

# Define the TextCarouselScreen
class TextCarouselScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(TextCarouselScreen, self).__init__('imagens/background.png', **kwargs)
        
        carousel = Carousel(direction='right', size_hint=(1, 1))

        texts = [
            "This is the first text",
            "Here is the second text",
            "And this is the third text",
            "Finally, the fourth text"
        ]

        for text in texts:
            content = BoxLayout(orientation='vertical', padding=10, size_hint=(1, 1))
            label = Label(text=text, text_size=(280, None), halign='center', valign='middle', size_hint=(1, 1))
            content.add_widget(label)
            carousel.add_widget(content)

        self.content_layout.add_widget(carousel)
        self.add_home_button()

# Create the screen manager
class SlideApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home_screen'))
        sm.add_widget(StartingScreen(name='starting_screen'))
        sm.add_widget(AboutScreen(name='about_screen'))
        sm.add_widget(IdentificacaoScreen(name='identificacao'))
        sm.add_widget(QueixaPrincipalScreen(name='queixaprincipal'))
        sm.add_widget(HmaScreen(name='hma'))
        sm.add_widget(HistoriaPregressaScreen(name='historiapregressa'))
        sm.add_widget(HabitosDeVidaScreen(name='habitosdevida'))
        sm.add_widget(UsoDeSubstanciasScreen(name='usodesubstancias'))
        sm.add_widget(HistoriaFisiologicaScreen(name='historiafisiologica'))
        sm.add_widget(HistoriaFamilialScreen(name='historiafamilial'))
        sm.add_widget(HistoriaFamiliarScreen(name='historiafamiliar'))
        sm.add_widget(HistoriaPsicossocialScreen(name='historiapsicossocial'))
        sm.add_widget(RevisaoDeSistemasScreen(name='revisaodesistemas'))
        sm.add_widget(TextCarouselScreen(name='text_carousel_screen'))
        return sm

# Run the app
if __name__ == '__main__':
    SlideApp().run()
