# main.py
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import *

# Set the window size to a typical smartphone size
Window.size = (450, 800)

class SlideApp(App):
    def build(self):
        sm = ScreenManager()
        # Home Screen
        sm.add_widget(HomeScreen(name='home_screen'))
        # Level 1 Screens
        sm.add_widget(StartingScreen(name='starting_screen'))
        sm.add_widget(AboutScreen(name='about_screen'))
        # Level 2 Screens
        sm.add_widget(IdentificacaoScreen(name='identificacao'))
        sm.add_widget(QueixaPrincipalScreen(name='queixa_principal'))
        sm.add_widget(HMAScreen(name='HMA'))
        sm.add_widget(HPPScreen(name='HPP'))
        sm.add_widget(HistoriaFisiologicaScreen(name='Hfisio'))
        sm.add_widget(HistoriaFamilialScreen(name='Hfamilial'))
        sm.add_widget(HistoriaFamiliarScreen(name='Hfamiliar'))
        sm.add_widget(HistoriaPsicossocialScreen(name='Hpsico'))
        sm.add_widget(SubstanciasScreen(name='subst'))
        sm.add_widget(HabitosDeVidaScreen(name='habitos'))
        sm.add_widget(RevisaoDeSistemasScreen(name='revisao_sistemas'))
        # Level 3 Screens
        sm.add_widget(HMAMedicamentosNaoCronicosScreen(name='HMA_medicamentos_nao_cronicos'))
        sm.add_widget(HMADecalogoDaDorScreen(name='HMA_decalogo'))
        sm.add_widget(HPPCirurgiasScreen(name='HPP_cirurgias'))
        sm.add_widget(HPPMedicamentosCronicosScreen(name='HPP_medicamentos_cronicos'))
        sm.add_widget(HistoriaFisiologicaRelacaoSexualScreen(name='Hfisio_relacao_sexual'))
        sm.add_widget(HistoriaFisiologicaGestacaoScreen(name='Hfisio_gestacao'))
        sm.add_widget(HistoriaFisiologicaExamesPreventivosScreen(name='Hfisio_exames_preventivos'))
        sm.add_widget(HistoriaFisiologicaMenopausaScreen(name='Hfisio_menopausa'))
        sm.add_widget(HistoriaFisiologicaPuberdadeScreen(name='Hfisio_puberdade'))
        sm.add_widget(HistoriaPsicossocialHabitacaoScreen(name='Hpsico_habitacao'))
        sm.add_widget(SubstanciasAlcoolScreen(name='subst_alcool'))
        sm.add_widget(SubstanciasTabacoScreen(name='subst_tabaco'))
        sm.add_widget(SubstanciasDrogasIlicitasScreen(name='subst_drogas_ilicitas'))
        return sm

if __name__ == '__main__':
    SlideApp().run()
