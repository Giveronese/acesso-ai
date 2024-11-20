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
from kivy.uix.widget import Widget


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

    def add_back_button(self):
        back_button = ImageButton(source='assets/imagens/left_arrow.png', on_press=self.go_to_previous_screen)
        back_button.size_hint = (None, None)
        back_button.size = (50, 50)
        back_button.pos_hint = {'right': 1, 'bottom': 1}
        self.layout.add_widget(back_button)

    def go_to_previous_screen(self, instance):
        if self.manager and hasattr(self.manager, 'go_to_previous_screen'):
            self.manager.go_to_previous_screen()
        else:
            print("No previous screen to go back to.")

    def go_to_screen(self, screen_name):
        if self.manager:
            self.manager.current = screen_name
        else:
            print("ScreenManager not yet assigned to this screen.")

    def create_title(self, title_text, font_size=constants.TITLE_FONT_SIZE, hex_color='#000000'):
        # Cria o layout vertical principal
        title_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        
        # Cria o título como um Label
        title = Label(
            text=title_text,
            font_size=font_size,
            size_hint=(1, None),
            halign='center',
            valign='middle',
            color=get_color_from_hex(hex_color),
            bold=True,
            font_name='Roboto'  # Use a bold font for the title
        )
        # Other font options could include:
        # font_name='Roboto-Italic'  # Use an italic font for the title
        # font_name='Roboto-Black'  # Use a black (heavier) font for the title
        # font_name='Roboto-Light'  # Use a light font for the title
        title.bind(
            texture_size=lambda instance, size: setattr(instance, 'height', instance.texture_size[1] + 20)  # Altura dinâmica
        )
        title.text_size = (Window.width * 0.6, None)  # Limita a largura do texto para centralização

        # Adiciona espaçamento proporcional
        spacer_top = Widget(size_hint=(1, None), height=Window.height * 0.02)  # Espaço de 2% da altura
        spacer_bottom = Widget(size_hint=(1, None), height=Window.height * 0.05) # Espaço de 20% da altura

        # Adiciona elementos ao layout
        title_layout.add_widget(spacer_top)
        title_layout.add_widget(title)
        title_layout.add_widget(spacer_bottom)

        # Define a altura total do layout com base nos componentes
        title_layout.height = spacer_top.height + title.height + spacer_bottom.height

        # Adiciona o layout de título ao conteúdo principal
        self.content_layout.add_widget(title_layout)

    def create_image_popup_handler(self, image_source, text_info, image_description):
        # This function returns a lambda that will call show_image_popup with the correct arguments
        return lambda instance: self.show_image_popup(image_source, text_info, image_description)

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
        close_button = Button(
            text='FECHAR', 
            size_hint_y=None, height=40,                 
            background_color=get_color_from_hex(constants.BUTTON_BACKGROUND_COLOR),
            background_normal='',
            font_name='Roboto',
            bold=True
        )
        close_button.bind(on_press=lambda instance: popup.dismiss())
        content.add_widget(close_button)

        # Configure Popup with white background
        popup = Popup(
            title=image_description.capitalize(),
            title_color=get_color_from_hex('#000000'),
            title_size=constants.TITLE_FONT_SIZE,
            content=content,
            size_hint=(1, 1),
            background='',  # Remove background image
            #background_color=(1, 1, 1, 1)  # RGBA for white background
        )
        popup.open()
    
    def create_buttons(self, button_texts):
        # Define o layout em grade para os botões
        grid_layout = GridLayout(
            cols=1, 
            spacing=constants.BUTTON_HEIGHT/2, 
            size_hint_y=None, 
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for text, screen_name in button_texts:
            btn = Button(
                text=text,
                font_size=constants.BUTTON_FONT_SIZE,
                size_hint=(None, None),
                size=(constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT),  # Tamanho inicial
                halign='center',
                valign='middle',
                background_color=get_color_from_hex(constants.BUTTON_BACKGROUND_COLOR),
                background_normal='',
                font_name='Roboto',
                bold=True
            )
            btn.text_size = (btn.width - constants.BUTTON_MARGIN, None)

            # Ajuste dinâmico da altura
            btn.bind(
                texture_size=lambda instance, size: setattr(instance, 'height', instance.texture_size[1] + constants.BUTTON_MARGIN)
            )
            btn.pos_hint = {'center_x': 0.5}

            # Ações dos botões
            if screen_name in constants.RELACAO_IMAGENS_TEXTOS.keys():
                question_text = constants.RELACAO_IMAGENS_TEXTOS[screen_name][0]
                btn.bind(on_press=self.create_image_popup_handler(f'assets/imagens/{screen_name}.jpg', '', question_text))
            else:
                btn.bind(on_press=lambda instance, sn=screen_name: self.go_to_screen(sn))

            grid_layout.add_widget(btn)

        # Calcula a largura do `ScrollView` considerando a barra de rolagem
        scrollbar_width = 20  # Tamanho médio da barra de rolagem
        scroll_view = ScrollView(
            size_hint=(None, None),
            size=(constants.BUTTON_WIDTH + scrollbar_width, Window.height * 0.7),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        scroll_view.add_widget(grid_layout)

        # Layout principal para o conjunto de botões
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(constants.BUTTON_WIDTH + scrollbar_width + 20, Window.height * 0.7),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        # Adiciona elementos ao layout
        main_layout.add_widget(scroll_view)

        # Adiciona o layout de botões ao conteúdo da tela
        self.content_layout.add_widget(main_layout)

# Define your screens
class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__('assets/imagens/background.png', **kwargs)

        self.create_title('ACESSO')

        button_texts = [
            ('INICIAR', 'starting_screen'),
            ('SOBRE O APP', 'about_screen'),
        ]

        self.create_buttons(button_texts)

# Level 1 Screens
class StartingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(StartingScreen, self).__init__('assets/imagens/background.png', **kwargs)
        
        self.create_title('SELECIONE A ETAPA DA ENTREVISTA')

        button_texts = [
            ('IDENTIFICAÇÃO', 'identificacao'),
            ('QUEIXA PRINCIPAL', 'queixa_principal'),
            ('HMA', 'HMA'),
            ('HISTÓRIA PREGRESSA', 'HPP'),
            ('HISTÓRIA FISIOLÓGICA', 'Hfisio'),
            ('HISTÓRIA FAMILIAL', 'Hfamilial'),
            ('HISTÓRIA FAMILIAR', 'Hfamiliar'),
            ('HISTÓRIA PSICOSSOCIAL', 'Hpsico'),
            ('USO DE SUBSTÂNCIAS', 'subst'),
            ('HÁBITOS DE VIDA', 'habitos'),
            ('REVISÃO DE SISTEMAS', 'revisao_sistemas'),
        ]

        self.create_buttons(button_texts)
        self.add_back_button()

class AboutScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__('assets/imagens/background.png', **kwargs)

        self.create_title('SOBRE O APP')

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
        self.add_back_button()

# Level 2 Screens
class IdentificacaoScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(IdentificacaoScreen, self).__init__('assets/imagens/background.png', **kwargs)

        self.create_title('IDENTIFICAÇÃO')

        button_texts = [
            ('NOME', 'identificacao_nome'),
            ('IDADE', 'identificacao_idade'),
            ('NATURALIDADE', 'identificacao_naturalidade'),
            ('ESTADO CIVIL', 'identificacao_estado_civil'),
            ('PROFISSÃO', 'identificacao_profissao'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class QueixaPrincipalScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(QueixaPrincipalScreen, self).__init__('assets/imagens/background.png', **kwargs)

        self.create_title('QUEIXA PRINCIPAL')

        button_texts = [
            ('PERGUNTA ABERTA', 'queixa_principal_pergunta_aberta'),
            ('IMAGENS AUXILIARES', 'queixa_principal_imagens_auxiliares'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HMAScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HMAScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HMA')

        button_texts = [
            ('INÍCIO DOS SINTOMAS', 'HMA_inicio'),
            ('LOCAL DOS SINTOMAS', 'HMA_local'),
            ('EVOLUÇÃO DOS SINTOMAS', 'HMA_evolucao'),
            ('IRRADIAÇÃO DOS SINTOMAS', 'HMA_irradiacao'),
            ('SINTOMAS ASSOCIADOS', 'HMA_sintomas'),
            ('FATOR DESENCADEANTE', 'HMA_desencadeante'),
            ('FATOR AGRAVANTE', 'HMA_agravante'),
            ('FATOR ATENUANTE', 'HMA_atenuante'),
            ('MEDICAMENTOS NÃO CRÔNICOS', 'HMA_medicamentos_nao_cronicos'),
            ('DECÁLOGO DA DOR', 'HMA_decalogo'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HPPScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HPPScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HPP')

        button_texts = [
            ('CIRURGIAS', 'HPP_cirurgias'),
            ('ALERGIAS', 'HPP_alergias'),
            ('DCNT', 'HPP_DCNT'),
            ('MEDICAMENTOS CRÔNICOS', 'HPP_medicamentos_cronicos'),
            ('CALENDÁRIO VACINAL', 'HPP_vacinacao'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaFisiologicaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFisiologicaScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HISTÓRIA FISIOLÓGICA')

        button_texts = [
            ('DUM', 'Hfisio_DUM'),
            ('RELAÇÃO SEXUAL', 'Hfisio_relacao_sexual'),
            ('GESTAÇÃO', 'Hfisio_gestacao'),
            ('EXAMES PREVENTIVOS', 'Hfisio_exames_preventivos'),
            ('MENOPAUSA', 'Hfisio_menopausa'),
            ('PUBERDADE', 'Hfisio_puberdade'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaFamilialScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFamilialScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HISTÓRIA FAMILIAL')

        button_texts = [
            ('DOENÇAS NO TRABALHO', 'Hfamilial_trabalho'),
            ('DOENÇAS NA ESCOLA', 'Hfamilial_escola'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaFamiliarScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFamiliarScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HISTÓRIA FAMILIAR')

        button_texts = [
            ('DCNT', 'Hfamiliar_DCNT'),
            ('ÓBITOS', 'Hfamiliar_obitos'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaPsicossocialScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaPsicossocialScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HISTÓRIA PSICOSSOCIAL')

        button_texts = [
            ('RENDA FAMILIAR', 'Hpsico_renda'),
            ('RELIGIÃO', 'Hpsico_religiao'),
            ('ESCOLARIDADE', 'Hpsico_escolaridade'),
            ('HABITAÇÃO', 'Hpsico_habitacao'),
            ('RELAÇÕES FAMILIARES', 'Hpsico_relacoes'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class SubstanciasScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(SubstanciasScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HISTÓRIA PSICOSSOCIAL')

        button_texts = [
            ('ÁLCOOL', 'subst_alcool'),
            ('TABACO', 'subst_tabaco'),
            ('DROGAS ILÍCITAS', 'subst_drogas_ilicitas'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HabitosDeVidaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HabitosDeVidaScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HÁBITOS DE VIDA')

        button_texts = [
            ('ATIVIDADE FÍSICA', 'habitos_atividade_fisica'),
            ('SONO', 'habitos_sono'),
            ('ALIMENTAÇÃO', 'habitos_alimentacao'),
            ('HIGIENE', 'habitos_higiene'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class RevisaoDeSistemasScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(RevisaoDeSistemasScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HÁBITOS DE VIDA')

        button_texts = [
            ('CARDIOVASCULAR', 'revisao_sistemas_cardiovascular'),
            ('RESPIRAÇÃO', 'revisao_sistemas_respiratorio'),
            ('TGI', 'revisao_sistemas_TGI'),
            ('UROGENITAL', 'revisao_sistemas_urogenital'),
            ('NEUROLÓGICO', 'revisao_sistemas_neurologico'),
            ('HEMATOLÓGICO', 'revisao_sistemas_hematologico'),
            ('ENDÓCRINO', 'revisao_sistemas_endocrino'),
            ('OSTEOMUSCULAR', 'revisao_sistemas_osteomuscular'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

# Level 3 Screens
class HMAMedicamentosNaoCronicosScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HMAMedicamentosNaoCronicosScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('MEDICAMENTOS NÃO CRÔNICOS')

        button_texts = [
            ('MEDICAMENTO', 'HMA_medicamentos_nao_cronicos_tipo'),
            ('DOSE', 'HMA_medicamentos_nao_cronicos_dose'),
            ('POSOLOGIA', 'HMA_medicamentos_nao_cronicos_posologia'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HMADecalogoDaDorScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HMADecalogoDaDorScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('DECÁLOGO DA DOR')

        button_texts = [
            ('LOCALIZAÇÃO', 'HMA_decalogo_localizacao'),
            ('IRRADIAÇÃO', 'HMA_decalogo_irradiacao'),
            ('QUALIDADE', 'HMA_decalogo_qualidade'),
            ('INTENSIDADE', 'HMA_decalogo_intensidade'),
            ('DURAÇÃO', 'HMA_decalogo_duracao'),
            ('EVOLUÇÃO', 'HMA_decalogo_evolucao'),
            ('RELAÇÃO COM FUNÇÕES ORGÂNICAS', 'HMA_decalogo_relacao'),
            ('FATOR DESENCADEANTE', 'HMA_decalogo_desencadeante'),
            ('FATOR AGRAVANTE', 'HMA_decalogo_agravante'),
            ('FATOR ATENUANTE', 'HMA_decalogo_atenuante'),
            ('SINTOMAS ASSOCIADOS', 'HMA_decalogo_sintomas'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HPPCirurgiasScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HPPCirurgiasScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('CIRURGIAS')

        button_texts = [
            ('FEZ OU NÃO', 'HPP_cirurgias_sim_nao'),
            ('QUANTIDADE', 'HPP_cirurgias_quantidade'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HPPMedicamentosCronicosScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HPPMedicamentosCronicosScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('MEDICAMENTOS CRÔNICOS')

        button_texts = [
            ('MEDICAMENTO', 'HPP_medicamentos_cronicos_tipo'),
            ('DOSE', 'HPP_medicamentos_cronicos_dose'),
            ('POSOLOGIA', 'HPP_medicamentos_cronicos_posologia'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaFisiologicaRelacaoSexualScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFisiologicaRelacaoSexualScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('RELAÇÃO SEXUAL')

        button_texts = [
            ('PRATICA OU NÃO', 'Hfisio_relacao_sexual_sim_nao'),
            ('FREQUÊNCIA', 'Hfisio_relacao_sexual_frequencia'),
            ('PARCEIROS', 'Hfisio_relacao_sexual_parceiros'),
            ('CONTRACEPTIVOS', 'Hfisio_relacao_sexual_contraceptivos'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaFisiologicaGestacaoScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFisiologicaGestacaoScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('GESTAÇÃO')

        button_texts = [
            ('QUANTIDADE', 'Hfisio_gestacoes_quantidade'),
            ('TIPO DE PARTO', 'Hfisio_gestacoes_partos'),
            ('ABORTAMENTOS', 'Hfisio_gestacoes_abortos'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaFisiologicaExamesPreventivosScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFisiologicaExamesPreventivosScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('EXAMES PREVENTIVOS')

        button_texts = [
            ('CITOPATOLÓGICO', 'Hfisio_exames_preventivos_citopatologico'),
            ('MAMOGRAFIA', 'Hfisio_exames_preventivos_mamografia'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaFisiologicaMenopausaScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFisiologicaMenopausaScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('MENOPAUSA')

        button_texts = [
            ('INÍCIO', 'Hfisio_menopausa_inicio'),
            ('SINTOMAS', 'Hfisio_menopausa_sintomas'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaFisiologicaPuberdadeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaFisiologicaPuberdadeScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('PUBERDADE')

        button_texts = [
            ('MENARCA', 'Hfisio_puberdade_menarca'),
            ('TELARCA', 'Hfisio_puberdade_telarca'),
            ('PUBARCA', 'Hfisio_puberdade_pubarca'),
            ('SEXARCA', 'Hfisio_puberdade_sexarca'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class HistoriaPsicossocialHabitacaoScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HistoriaPsicossocialHabitacaoScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('HABITAÇÃO')

        button_texts = [
            ('LOCAL', 'Hpsico_habitacao_local'),
            ('CONDIÇÕES', 'Hpsico_habitacao_condicoes'),
            ('SANEAMENTO', 'Hpsico_habitacao_saneamento'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class SubstanciasAlcoolScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(SubstanciasAlcoolScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('ÁLCOOL')

        button_texts = [
            ('FAZ USO', 'subst_alcool_uso'),
            ('INÍCIO DO USO', 'subst_alcool_inicio'),
            ('DOSE', 'subst_alcool_quantidade'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class SubstanciasTabacoScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(SubstanciasTabacoScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('TABACO')

        button_texts = [
            ('FAZ USO', 'subst_tabaco_uso'),
            ('INÍCIO DO USO', 'subst_tabaco_inicio'),
            ('DOSE', 'subst_tabaco_quantidade'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()

class SubstanciasDrogasIlicitasScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(SubstanciasDrogasIlicitasScreen, self).__init__('assets/imagens/background.png', **kwargs)
        self.create_title('DROGAS ILÍCITAS')

        button_texts = [
            ('FAZ USO', 'subst_drogas_ilicitas_uso'),
            ('INÍCIO DO USO', 'subst_drogas_ilicitas_inicio'),
            ('DOSE', 'subst_drogas_ilicitas_quantidade'),
        ]

        self.create_buttons(button_texts)

        # Add home button
        self.add_back_button()