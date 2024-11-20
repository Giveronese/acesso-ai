# main.py
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import *

# Set the window size to a typical self.screen_managerartphone size
Window.size = (450, 800)

class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(CustomScreenManager, self).__init__(**kwargs)
        self.screen_stack = []

    def on_current(self, instance, value):
        # Se a navegação foi feita via back_button, não adiciona a tela atual à pilha
        if not getattr(self, 'navigating_back', False):
            if self.current_screen:
                current_screen_name = self.current_screen.name

                # Evita adicionar a mesma tela duas vezes seguidas ou adicionar a home_screen
                if self.screen_stack and self.screen_stack[-1] == current_screen_name:
                    return

                if current_screen_name != 'home_screen':  # Evita adicionar a tela inicial
                    self.screen_stack.append(current_screen_name)
        
        # Exibe a pilha atual
        print(f"Current stack: {self.screen_stack}")
        
        super(CustomScreenManager, self).on_current(instance, value)

    def go_to_previous_screen(self):
        # Marca que a navegação está sendo feita via back_button
        self.navigating_back = True
        
        # Verifica se há telas na pilha para voltar
        if self.screen_stack:
            previous_screen = self.screen_stack.pop()  # Remove a última tela
            self.current = previous_screen
        else:
            # Se a pilha está vazia, vá para a tela inicial
            self.current = 'home_screen'
        
        # Após navegar, desfaz a marcação da navegação via back_button
        self.navigating_back = False
    
class SlideApp(App):
    def build(self):
        self.screen_manager = CustomScreenManager()
        # Home Screen
        self.screen_manager.add_widget(HomeScreen(name='home_screen'))
        # Level 1 Screens
        self.screen_manager.add_widget(StartingScreen(name='starting_screen'))
        self.screen_manager.add_widget(AboutScreen(name='about_screen'))
        # Level 2 Screens
        self.screen_manager.add_widget(IdentificacaoScreen(name='identificacao'))
        self.screen_manager.add_widget(QueixaPrincipalScreen(name='queixa_principal'))
        self.screen_manager.add_widget(HMAScreen(name='HMA'))
        self.screen_manager.add_widget(HPPScreen(name='HPP'))
        self.screen_manager.add_widget(HistoriaFisiologicaScreen(name='Hfisio'))
        self.screen_manager.add_widget(HistoriaFamilialScreen(name='Hfamilial'))
        self.screen_manager.add_widget(HistoriaFamiliarScreen(name='Hfamiliar'))
        self.screen_manager.add_widget(HistoriaPsicossocialScreen(name='Hpsico'))
        self.screen_manager.add_widget(SubstanciasScreen(name='subst'))
        self.screen_manager.add_widget(HabitosDeVidaScreen(name='habitos'))
        self.screen_manager.add_widget(RevisaoDeSistemasScreen(name='revisao_sistemas'))
        # Level 3 Screens
        self.screen_manager.add_widget(HMAMedicamentosNaoCronicosScreen(name='HMA_medicamentos_nao_cronicos'))
        self.screen_manager.add_widget(HMADecalogoDaDorScreen(name='HMA_decalogo'))
        self.screen_manager.add_widget(HPPCirurgiasScreen(name='HPP_cirurgias'))
        self.screen_manager.add_widget(HPPMedicamentosCronicosScreen(name='HPP_medicamentos_cronicos'))
        self.screen_manager.add_widget(HistoriaFisiologicaRelacaoSexualScreen(name='Hfisio_relacao_sexual'))
        self.screen_manager.add_widget(HistoriaFisiologicaGestacaoScreen(name='Hfisio_gestacao'))
        self.screen_manager.add_widget(HistoriaFisiologicaExamesPreventivosScreen(name='Hfisio_exames_preventivos'))
        self.screen_manager.add_widget(HistoriaFisiologicaMenopausaScreen(name='Hfisio_menopausa'))
        self.screen_manager.add_widget(HistoriaFisiologicaPuberdadeScreen(name='Hfisio_puberdade'))
        self.screen_manager.add_widget(HistoriaPsicossocialHabitacaoScreen(name='Hpsico_habitacao'))
        self.screen_manager.add_widget(SubstanciasAlcoolScreen(name='subst_alcool'))
        self.screen_manager.add_widget(SubstanciasTabacoScreen(name='subst_tabaco'))
        self.screen_manager.add_widget(SubstanciasDrogasIlicitasScreen(name='subst_drogas_ilicitas'))
        return self.screen_manager

if __name__ == '__main__':
    SlideApp().run()
