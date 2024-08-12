# screens.py
import os.path

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.carousel import Carousel
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from widgets import ImageButton

import constants


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
        home_button = ImageButton(source='assets/imagens/left_arrow.png', on_press=self.go_to_home_screen)
        home_button.size_hint = (None, None)
        home_button.size = (50, 50)
        home_button.pos_hint = {'right': 1, 'bottom': 1}
        self.layout.add_widget(home_button)

    def go_to_home_screen(self, instance):
        self.manager.current = 'home_screen'

    def add_return_button(self):
        return_button = ImageButton(source='assets/imagens/left_arrow.png', on_press=self.go_to_starting_screen)
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

            # Define the action based on whether the file exists or not
            if os.path.isfile(f'assets/imagens/{screen_name}.jpg'):
                btn.bind(on_press=self.create_image_popup_handler(f'assets/imagens/{screen_name}.jpg', 'Informação da Imagem', text))
            else:
                btn.bind(on_press=self.create_screen_transition_handler(screen_name))
            
            grid_layout.add_widget(btn)

        scroll_view.add_widget(grid_layout)
        self.content_layout.add_widget(scroll_view)

    def create_image_popup_handler(self, image_source, text_info, image_description):
        # This function returns a lambda that will call show_image_popup with the correct arguments
        return lambda instance: self.show_image_popup(image_source, text_info, image_description)

    def create_screen_transition_handler(self, screen_name):
        # This function returns a lambda that will change the screen
        return lambda instance: setattr(self.manager, 'current', screen_name)

    def show_image_popup(self, image_source, text_info, image_description):
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

        popup = Popup(title=image_description.upper(), content=content, size_hint=(1, 1))
        popup.open()
    
    def create_buttons(self, button_texts):
        # Define the grid layout with fixed column width
        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for text, screen_name in button_texts:
            btn = Button(text=text, size_hint=(None, None), size=(constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT))
            btn.pos_hint = {'center_x': 0.5}
            if screen_name in constants.RELACAO_IMAGENS_TEXTOS.keys():
                btn.bind(on_press=self.create_image_popup_handler(f'assets/imagens/{screen_name}.jpg', 'Informação da Imagem', text))
            else:
                print(f"Screen name: {screen_name}")
                btn.bind(on_press=lambda instance, sn=screen_name: self.go_to_screen(sn))
            grid_layout.add_widget(btn)

        # Get the actual screen dimensions
        screen_width = Window.size[0]
        screen_height = Window.size[1]
        print(screen_width, screen_height)
        padding_width = screen_width * 0.1  # 10% padding
        padding_height = screen_height * 0.2  # 20% padding

        # Create a scroll view with adjusted height to include padding
        scroll_view = ScrollView(size_hint=(None, None), size=(constants.BUTTON_WIDTH + 20, screen_height * 0.6))  # 60% of the screen height
        scroll_view.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Centered vertically and horizontally
        scroll_view.add_widget(grid_layout)

        # Create the main layout and add the scroll view to it
        main_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(constants.BUTTON_WIDTH + 40, screen_height - padding_height))
        main_layout.pos_hint = {'center_x': 0.5, 'y': 0}  # Adjusted to fit under the title
        main_layout.add_widget(scroll_view)

        # Add the main layout to the screen's content layout
        self.content_layout.add_widget(main_layout)

        # Print the screen height for debugging
        print("Screen Height:", screen_height)

    def go_to_screen(self, screen_name):
        if self.manager:
            self.manager.current = screen_name
        else:
            print("ScreenManager not yet assigned to this screen.")
    
    def create_title(self, title_text, font_size=constants.TITLE_FONT_SIZE, hex_color='#4E5D5A'):
        # Get the actual screen height
        screen_height = Window.height
        padding_height = screen_height * 0.2  # 20% padding

        # Create a layout for the title with the specified padding at the top
        title_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(Window.width, padding_height))
        title_layout.pos_hint = {'center_x': 0.5, 'top': 1}  # Position at the top of the screen

        # Add the title label to the title layout
        title = Label(text=title_text, font_size=font_size, size_hint_y=None, height=constants.TITLE_HEIGHT, color=get_color_from_hex(hex_color))
        title_layout.add_widget(title)
        self.content_layout.add_widget(title_layout)

# Define your screens
class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__('assets/imagens/background.png', **kwargs)

        self.create_title('Acesso', font_size=32)

        button_texts = [
            ('INICIAR', 'starting_screen'),
            ('SOBRE O APP', 'about_screen'),
        ]

        self.create_buttons(button_texts)

class StartingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(StartingScreen, self).__init__('assets/imagens/background.png', **kwargs)
        
        self.create_title('Selecione a etapa da entrevista')

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
            ('MOSTRAR IMAGEM', 'identificacao_nome'),
        ]

        # grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # scroll_layout = BoxLayout(size_hint=(None, None), size=(300, 500))
        # scroll_layout.add_widget(grid_layout)
        
        # for text, screen_name in button_texts:
        #     btn = Button(text=text, size_hint_y=None, height=30)
        #     if screen_name == 'show_image':
        #         btn.bind(on_press=lambda instance: self.show_image_popup('assets/imagens/identificacao_nome.jpg', "", "teste teste 123"))
        #     else:
        #         btn.bind(on_press=lambda instance, sn=screen_name: setattr(self.manager, 'current', sn))
        #     grid_layout.add_widget(btn)

        # scroll_layout = BoxLayout(size_hint=(None, None), size=(300, 500))
        # scroll_layout.add_widget(grid_layout)
        
        # main_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 400))
        # main_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        # main_layout.add_widget(scroll_layout)
        
        # self.content_layout.add_widget(main_layout)

        self.create_buttons(button_texts)
        self.add_home_button()

class IdentificacaoScreen(BaseScreen):
    # def __init__(self, **kwargs):
    #     super(IdentificacaoScreen, self).__init__('assets/imagens/background.png', **kwargs)
        
    #     self.create_title('Identificação')

    #     button_texts = [
    #         ('INICIAR', 'starting_screen'),
    #         ('SOBRE O APP', 'about_screen'),
    #     ]

    #     self.create_buttons(button_texts)
    #     self.add_home_button()
    def __init__(self, **kwargs):
        super(IdentificacaoScreen, self).__init__('assets/imagens/background.png', **kwargs)

        self.create_title('Acesso', font_size=32)

        button_texts = [
            ('INICIAR', 'starting_screen'),
            ('SOBRE O APP', 'about_screen'),
        ]

        self.create_buttons(button_texts)

class AboutScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__('assets/imagens/background.png', **kwargs)

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
        super(IdentificacaoScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Identificação Screen'))
        self.add_home_button()

class QueixaPrincipalScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(QueixaPrincipalScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Queixa Principal Screen'))
        self.add_home_button()

class HmaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HmaScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='HMA Screen'))
        self.add_home_button()

class HistoriaPregressaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaPregressaScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Pregressa Screen'))
        self.add_home_button()

class HabitosDeVidaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HabitosDeVidaScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Hábitos de Vida Screen'))
        self.add_home_button()

class UsoDeSubstanciasScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(UsoDeSubstanciasScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Uso de Substâncias Screen'))
        self.add_home_button()

class HistoriaFisiologicaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFisiologicaScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Fisiológica Screen'))
        self.add_home_button()

class HistoriaFamilialScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFamilialScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Familial Screen'))
        self.add_home_button()

class HistoriaFamiliarScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFamiliarScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Familiar Screen'))
        self.add_home_button()

class HistoriaPsicossocialScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaPsicossocialScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='História Psicossocial Screen'))
        self.add_home_button()

class RevisaoDeSistemasScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(RevisaoDeSistemasScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.content_layout.add_widget(Label(text='Revisão de Sistemas Screen'))
        self.add_home_button()