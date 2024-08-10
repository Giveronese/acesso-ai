# main.py
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import (
    HomeScreen, StartingScreen, AboutScreen, IdentificacaoScreen, 
    QueixaPrincipalScreen, HmaScreen, HistoriaPregressaScreen,
    HabitosDeVidaScreen, UsoDeSubstanciasScreen, HistoriaFisiologicaScreen,
    HistoriaFamilialScreen, HistoriaFamiliarScreen, HistoriaPsicossocialScreen,
    RevisaoDeSistemasScreen
)

# Set the window size to a typical smartphone size
Window.size = (450, 800)

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
        return sm

if __name__ == '__main__':
    SlideApp().run()
